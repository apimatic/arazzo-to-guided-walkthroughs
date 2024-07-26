import yaml
import requests

def fetch_openapi_spec(url, local_file):
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_file, 'w') as file:
            file.write(response.text)
        return local_file
    else:
        raise Exception(f"Failed to fetch OpenAPI spec from {url}, status code: {response.status_code}")

def parse_openapi_spec(file_path):
    
    with open(file_path, 'r') as file:
        try:
            openapi_spec = yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {file_path}: {e}")
            raise
    return openapi_spec

def extract_endpoints(openapi_spec):
    endpoints = {}
    paths = openapi_spec.get('paths', {})
    for path, methods in paths.items():
        for method, details in methods.items():
            operation_id = details.get('operationId')
            tags = details.get('tags', [])
            if operation_id and tags:
                tag = tags[0]
                endpoint_permalink = f"$e/{tag}/{operation_id}"
                endpoints[operation_id] = endpoint_permalink
    return endpoints

def get_endpoints_from_openapi(url, local_file='openapi_spec.yaml'):
    
    fetch_openapi_spec(url, local_file)
    openapi_spec = parse_openapi_spec(local_file)
    endpoints = extract_endpoints(openapi_spec)
    return endpoints

if __name__ == "__main__":
    source_description_url = "https://raw.githubusercontent.com/swagger-api/swagger-petstore/master/src/main/resources/openapi.yaml"
    endpoints = get_endpoints_from_openapi(source_description_url)
    for operation_id, endpoint_permalink in endpoints.items():
        print(f"{operation_id}: {endpoint_permalink}")
