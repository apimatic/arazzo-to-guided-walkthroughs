import yaml
import os

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
        name: "{name}",
        stepCallback: async ({name}State) => {{
          {step_code}
        }},
      }},
"""

def generate_step_code(step):
    return f"""
        await portal.setConfig((defaultConfig) => ({{
            ...defaultConfig,
        }}));
        return workflowCtx.showEndpoint({{
            description: `{step['description']}`,
            endpointPermalink: "{step.get('operationPath', 'Not provided')}",
            verify: (response, setError) => {{
              if (response.StatusCode != 200) {{
                setError("Error text");
                return false;
              }} else {{
                return true;
              }}
            }},
          }});
    """

def generate_steps(steps):
    steps_code = ""
    for step in steps:
        step_code = generate_step_code(step)
        steps_code += step_template.format(step_id=step['stepId'], name=step['description'], step_code=step_code)
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
        print (js_code)

if __name__ == "__main__":
    main()
