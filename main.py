import yaml
import os
import re

def parse_arazzo(file_path):
    with open(file_path, 'r') as file:
        arazzo_data = yaml.safe_load(file)
    return arazzo_data['workflows']

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
                endpointPermalink: "{operation_path}",
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

def generate_step_code(step, steps):
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

    return step_template.format(
        step_id=step.get('stepId', 'No stepId'),
        step_name=step.get('description', 'No description'),
        step_state_declaration=f"const previousStepState = stepState?.[\"{previous_step_id}\"];" if previous_step_id else "",
        description=step.get('description', 'No description'),
        operation_path=step.get('operationPath', 'Not provided'),
        args_code=args_code,
        config_code=f"config: {{ ...defaultConfig.config, {headers_code} }}" if headers_code else ""
    )

def generate_steps(steps):
    steps_code = ""
    for step in steps:
        step_code = generate_step_code(step, steps)
        steps_code += step_code
    return steps_code

def generate_function(workflow):
    steps_code = generate_steps(workflow['steps'])
    return function_template.format(workflow_id=workflow['workflowId'], steps=steps_code)

def save_js_function(js_code, file_name):
    with open(file_name, 'w') as file:
        file.write(js_code)

def main():
    arazzo_file = 'arazzo_spec.yaml'
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    workflows = parse_arazzo(arazzo_file)
    
    for workflow in workflows:
        js_code = generate_function(workflow)
        file_name = os.path.join(output_dir, f"{workflow['workflowId']}.js")
        save_js_function(js_code, file_name)
        print(js_code)

if __name__ == "__main__":
    main()
