from flask import Flask, request, send_file, jsonify
import os
import yaml
import re
import zipfile
import tempfile
import parsespec

app = Flask(__name__)

def get_arazzo_workflows(file_path):
    with open(file_path, 'r') as file:
        arazzo_data = yaml.safe_load(file)
    return arazzo_data['workflows']

def get_arazzo_source_description_url(file_path):
    with open(file_path, 'r') as file:
        arazzo_data = yaml.safe_load(file)
    return arazzo_data['sourceDescriptions'][0]['url']

function_template = """
async function {workflow_id}(workflowCtx, portal) {{
    return {{
{steps}
    }};
}}
"""

step_template = """
    "{step_id}": {{
        name: "{step_name}",
        stepCallback: async (stepState) => {{
            {step_state_declaration}
            await portal.setConfig((defaultConfig) => {{
                return {{
                    ...defaultConfig,
                    {config_code}
                }};
            }});
            return workflowCtx.showEndpoint({{
                description: `{description}`,
                endpointPermalink: "{endpoint_permalink}",
                args: {{
                    {args_code}
                }},
                verify: (response, setError) => {{
                    if (response.StatusCode != 200) {{
                        setError("Error text");
                        return false;
                    }} else {{
                        return true;
                    }}
                }},
            }});
        }},
    }},
"""

def replace_dynamic_references(value, steps):
    if isinstance(value, str):
        pattern = re.compile(r'\$steps\.(\w+)\.outputs\.(\w+)')
        matches = pattern.findall(value)
        for match in matches:
            step_name, output_name = match
            step_var = f"stepState?.[\"{step_name}\"].data?.{output_name}"
            value = value.replace(f"$steps.{step_name}.outputs.{output_name}", step_var)
    return value

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def generate_step_code(step, steps, endpoints):
    parameters = step.get('parameters', [])
    args_body = {}
    args_other = {}
    headers = {}

    for param in parameters:
        in_type = param['in']
        name = param['name']
        value = replace_dynamic_references(param['value'], steps)
        
        if is_number(value):
            value_str = value
        else:
            value_str = f'"{value}"'
        
        if in_type == 'body':
            args_body[name] = value_str
        elif in_type == 'header':
            headers[name] = value_str
        else:
            args_other[name] = value_str
    
    args_code = ""
    if args_body:
        body_code = ", ".join(f"{name}: {value}" for name, value in args_body.items())
        args_code += f"body: {{ {body_code} }}, "
    if args_other:
        other_code = ", ".join(f"{name}: {value}" for name, value in args_other.items())
        args_code += f"{other_code}, "
    args_code = args_code.rstrip(', ')

    headers_code = ""
    if headers:
        headers_code = ", ".join(f'"{name}": {value}' for name, value in headers.items())

    previous_step_id = steps[steps.index(step) - 1].get('stepId', '') if steps.index(step) > 0 else ''

    endpoint_permalink = endpoints.get(step.get('operationId', 'Not provided'), 'Not provided')

    return step_template.format(
        step_id=step.get('stepId', 'No stepId'),
        step_name=step.get('description', 'No description'),
        step_state_declaration=f"const previousStepState = stepState?.[\"{previous_step_id}\"];" if previous_step_id else "",
        description=step.get('description', 'No description'),
        endpoint_permalink=endpoint_permalink,
        args_code=args_code,
        config_code=f"config: {{ ...defaultConfig.config, {headers_code} }}" if headers_code else ""
    )

def generate_steps(steps, endpoints):
    steps_code = ""
    for step in steps:
        step_code = generate_step_code(step, steps, endpoints)
        steps_code += step_code
    return steps_code

def generate_function(workflow, endpoints):
    steps_code = generate_steps(workflow['steps'], endpoints)
    return function_template.format(workflow_id=workflow['workflowId'], steps=steps_code)

def save_js_function(js_code, file_name):
    with open(file_name, 'w') as file:
        file.write(js_code)

@app.route('/generate-scripts', methods=['POST'])
def generate_scripts():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, 'arazzo_spec.yaml')
    file.save(temp_file_path)

    try:
        url = get_arazzo_source_description_url(temp_file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to extract URL from spec: {str(e)}"}), 400

    try:
        endpoints = parsespec.get_endpoints_from_openapi(url)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch OpenAPI spec: {str(e)}"}), 400

    workflow_ids = []

    try:
        workflows = get_arazzo_workflows(temp_file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to extract workflows from spec: {str(e)}"}), 400

    for workflow in workflows:
        js_code = generate_function(workflow, endpoints)
        workflow_id = workflow['workflowId']
        workflow_ids.append(workflow_id)
        file_name = os.path.join(temp_dir, f"{workflow_id}.js")
        save_js_function(js_code, file_name)

    with open(os.path.join(temp_dir, 'workflow_ids.txt'), 'w') as file:
        file.write("Generated walkthrough scripts:\n")
        for workflow_id in workflow_ids:
            file.write(f"{workflow_id}.js\n")

    zip_filename = os.path.join(temp_dir, 'generated_files.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file != 'generated_files.zip':  # Avoid zipping the zip file itself
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, temp_dir))

    return send_file(zip_filename, as_attachment=True, download_name='generated_files.zip')

if __name__ == "__main__":
    app.run(debug=True)
