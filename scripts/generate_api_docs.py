"""Generate API reference documentation from FastAPI's OpenAPI schema.

Usage:
    1. Start the backend server:
        uvicorn backend.main:app --reload

    2. Run this script:
        python scripts/generate_api_docs.py

    3. The output is written to docs/technical/api/reference.md

    4. Commit the updated file to the repository.
"""

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


OPENAPI_URL = "http://localhost:8000/openapi.json"
OUTPUT_PATH = Path(__file__).parent.parent / "docs" / "technical" / "api" / "reference.md"


def fetch_schema() -> dict:
    """Fetch OpenAPI schema from running server."""
    try:
        with urllib.request.urlopen(OPENAPI_URL) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error: Could not fetch OpenAPI schema from {OPENAPI_URL}")
        print(f"Make sure the backend server is running: uvicorn backend.main:app --reload")
        print(f"Details: {e}")
        sys.exit(1)


def format_method(method: str) -> str:
    """Format HTTP method as uppercase."""
    return method.upper()


def get_security_info(security: list | None, security_schemes: dict) -> str:
    """Describe authentication requirements."""
    if not security:
        return "None"
    parts = []
    for sec in security:
        for scheme_name in sec:
            scheme = security_schemes.get(scheme_name, {})
            scheme_type = scheme.get("type", "")
            if scheme_type == "http" and scheme.get("scheme") == "bearer":
                parts.append("Bearer token (`Authorization: Bearer <token>`)")
            else:
                parts.append(scheme_name)
    return ", ".join(parts) if parts else "Required"


def get_schema_ref(ref: str, schemas: dict) -> dict:
    """Resolve a $ref to its schema."""
    name = ref.split("/")[-1]
    return schemas.get(name, {})


def schema_to_fields(schema: dict, schemas: dict, indent: int = 0) -> list[str]:
    """Convert a schema to a list of field descriptions."""
    fields = []
    if schema.get("type") == "object":
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for prop_name, prop_schema in properties.items():
            prop_type = prop_schema.get("type", "object")
            if "$ref" in prop_schema:
                ref_name = prop_schema["$ref"].split("/")[-1]
                prop_type = ref_name
            elif prop_type == "array":
                items = prop_schema.get("items", {})
                if "$ref" in items:
                    item_type = items["$ref"].split("/")[-1]
                    prop_type = f"array[{item_type}]"
                else:
                    prop_type = f"array[{items.get('type', 'any')}]"
            elif prop_type == "string" and prop_schema.get("format"):
                prop_type = f"{prop_type} ({prop_schema['format']})"

            required_marker = " *" if prop_name in required else ""
            description = prop_schema.get("description", "")
            desc_text = f" — {description}" if description else ""
            fields.append(f"  - `{prop_name}`: {prop_type}{required_marker}{desc_text}")
    return fields


def generate_method_section(method: str, path: str, operation: dict, schemas: dict) -> str:
    """Generate markdown for a single endpoint."""
    lines = []
    summary = operation.get("summary", "")
    description = operation.get("description", "")
    operation_id = operation.get("operationId", "")
    parameters = operation.get("parameters", [])
    request_body = operation.get("requestBody", {})
    responses = operation.get("responses", {})
    security = operation.get("security")
    security_schemas = schemas.get("SecuritySchemes", {})

    # Title
    title = summary or description or operation_id or f"{format_method(method)} {path}"
    lines.append(f"#### `{format_method(method)} {path}`")
    lines.append("")

    if description and description != summary:
        lines.append(f"{description}")
        lines.append("")

    # Auth
    auth_info = get_security_info(security, security_schemas)
    lines.append(f"**Auth:** {auth_info}")
    lines.append("")

    # Path and query parameters
    if parameters:
        lines.append("**Parameters:**")
        for param in parameters:
            name = param.get("name", "")
            location = param.get("in", "")
            required = param.get("required", False)
            param_schema = param.get("schema", {})
            param_type = param_schema.get("type", "string")
            req_marker = " (required)" if required else ""
            lines.append(f"  - `{name}` ({location}){req_marker}: {param_type}")
        lines.append("")

    # Request body
    if request_body:
        content = request_body.get("content", {})
        json_content = content.get("application/json", {})
        body_schema = json_content.get("schema", {})
        if body_schema:
            lines.append("**Request body:**")
            if "$ref" in body_schema:
                ref_name = body_schema["$ref"].split("/")[-1]
                ref_schema = schemas.get(ref_name, {})
                fields = schema_to_fields(ref_schema, schemas)
                lines.append(f"  Schema: `{ref_name}`")
                for field in fields:
                    lines.append(field)
            elif body_schema.get("type") == "array":
                items = body_schema.get("items", {})
                if "$ref" in items:
                    ref_name = items["$ref"].split("/")[-1]
                    lines.append(f"  Array of: `{ref_name}`")
            else:
                fields = schema_to_fields(body_schema, schemas)
                for field in fields:
                    lines.append(field)
            lines.append("")

    # Responses
    lines.append("**Responses:**")
    for status_code, response in sorted(responses.items()):
        resp_desc = response.get("description", "")
        resp_content = response.get("content", {})
        resp_schema = None
        if "application/json" in resp_content:
            resp_schema = resp_content["application/json"].get("schema", {})

        status_label = f"{status_code}"
        if status_code == "200":
            status_label = f"{status_code} OK"
        elif status_code == "201":
            status_label = f"{status_code} Created"
        elif status_code == "401":
            status_label = f"{status_code} Unauthorized"
        elif status_code == "403":
            status_label = f"{status_code} Forbidden"
        elif status_code == "404":
            status_label = f"{status_code} Not Found"
        elif status_code == "422":
            status_label = f"{status_code} Validation Error"

        lines.append(f"  - **{status_label}** — {resp_desc}")
        if resp_schema:
            if "$ref" in resp_schema:
                ref_name = resp_schema["$ref"].split("/")[-1]
                ref_schema = schemas.get(ref_name, {})
                fields = schema_to_fields(ref_schema, schemas)
                for field in fields:
                    lines.append(f"    {field}")
            elif resp_schema.get("type") == "array":
                items = resp_schema.get("items", {})
                if "$ref" in items:
                    ref_name = items["$ref"].split("/")[-1]
                    lines.append(f"    Array of: `{ref_name}`")
    lines.append("")

    return "\n".join(lines)


def generate_docs(schema: dict) -> str:
    """Generate full API reference markdown from OpenAPI schema."""
    info = schema.get("info", {})
    paths = schema.get("paths", {})
    components = schema.get("components", {})
    schemas = components.get("schemas", {})

    lines = []
    lines.append("# API Reference")
    lines.append("")
    lines.append("> Auto-generated from FastAPI's OpenAPI schema.")
    lines.append(f"> Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append("<!-- SCREENSHOT: swagger-ui")
    lines.append("     What to capture: Swagger UI showing interactive API docs")
    lines.append("     Suggested size: 1280x800")
    lines.append("-->")
    lines.append("")
    lines.append("![Swagger UI](../../screenshots/swagger-ui.png)")
    lines.append("")
    lines.append("Interactive docs available at: `<backend-url>/docs`")
    lines.append("")

    # Group endpoints by tag
    tagged: dict[str, list[tuple[str, str, dict]]] = {}
    untagged: list[tuple[str, str, dict]] = []

    for path, methods in sorted(paths.items()):
        for method, operation in methods.items():
            if method in ("get", "post", "put", "delete", "patch"):
                tags = operation.get("tags", [])
                if tags:
                    for tag in tags:
                        tagged.setdefault(tag, []).append((method, path, operation))
                else:
                    untagged.append((method, path, operation))

    # Generate sections by tag
    tag_order = ["Health", "Auth", "Tasks", "Developers", "Dashboard", "Presence"]
    all_tags = list(tag_order) + [t for t in tagged if t not in tag_order]

    for tag in all_tags:
        endpoints = tagged.get(tag, [])
        if not endpoints:
            continue

        lines.append(f"## {tag}")
        lines.append("")

        for method, path, operation in endpoints:
            lines.append(generate_method_section(method, path, operation, schemas))

    # Ungrouped
    if untagged:
        lines.append("## Other")
        lines.append("")
        for method, path, operation in untagged:
            lines.append(generate_method_section(method, path, operation, schemas))

    # Data models section
    model_names = [
        "UserResponse",
        "DeveloperResponse",
        "DeveloperWithAvailability",
        "TaskResponse",
        "TaskListResponse",
        "DashboardStats",
        "DashboardOverview",
    ]

    existing_models = [n for n in model_names if n in schemas]
    if existing_models:
        lines.append("## Data Models")
        lines.append("")
        for model_name in existing_models:
            model_schema = schemas[model_name]
            lines.append(f"### `{model_name}`")
            lines.append("")
            fields = schema_to_fields(model_schema, schemas)
            if fields:
                for field in fields:
                    lines.append(field)
            else:
                lines.append("  (No properties)")
            lines.append("")

    return "\n".join(lines)


def main():
    print(f"Fetching OpenAPI schema from {OPENAPI_URL}...")
    schema = fetch_schema()

    print(f"Generating documentation...")
    docs = generate_docs(schema)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(docs, encoding="utf-8")

    print(f"Written to {OUTPUT_PATH}")
    print(f"Done! {len(docs.splitlines())} lines generated.")


if __name__ == "__main__":
    main()
