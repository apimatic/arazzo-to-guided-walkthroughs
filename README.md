# Arazzo Walkthrough Translator

Arazzo Walkthrough Translator is a Python-based tool that automates the generation of Guided Walkthrough functions from OpenAPI's new Arazzo spec format. The tool processes the Arazzo spec, which acts as an overlay on the OpenAPI spec, defining workflows using multiple endpoints, and outputs JavaScript functions for each workflow.

## Features
- **Automated Translation**: Converts Arazzo specs into Guided Walkthrough JavaScript functions.
- **Multi-Workflow Support**: Handles multiple workflows defined in a single Arazzo spec.
- **Output Zipping**: Generates a zip file containing all the JavaScript functions for easy integration.

## Installation

### Prerequisites
- Python 3.x
- `pip` (Python package installer)

### Clone the Repository
```sh
git clone https://github.com/yourusername/arazzo-walkthrough-translator.git
cd arazzo-walkthrough-translator
```

### Install Dependencies
```sh
pip install pyyaml
```

## Usage

1. **Prepare Your Arazzo Spec File**
   Ensure you have an Arazzo spec file (e.g., `arazzo_spec.yaml`) in the root directory of the project.

2. **Run the Translator**
   Execute the following command to run the translator:
   ```sh
   python main.py
   ```

3. **Output**
   The script will generate a directory named `output` containing:
   - JavaScript functions for each workflow defined in the Arazzo spec.
   - A text file (`workflow_ids.txt`) listing all generated walkthrough scripts.
   - A zip file (`guided-walkthrough-scripts.zip`) containing all generated files.

## Example Arazzo Spec
Here's an example of what an Arazzo spec file might look like:

```yaml
sourceDescriptions:
  - url: "https://api.yourservice.com/openapi.yaml"
workflows:
  - workflowId: "post_to_threads"
    description: "Post a message to Threads"
    steps:
      - stepId: "get_token"
        description: "Get OAuth Token"
        operationId: "getOAuthToken"
        parameters:
          - name: "client_id"
            in: "query"
            value: "your_client_id"
          - name: "client_secret"
            in: "query"
            value: "your_client_secret"
      - stepId: "post_message"
        description: "Post the message"
        operationId: "postMessage"
        parameters:
          - name: "token"
            in: "header"
            value: "$steps.get_token.outputs.token"
          - name: "message"
            in: "body"
            value: "Hello, World!"
```

## Project Structure

```
arazzo-walkthrough-translator/
├── main.py             # Main script to run the translator
├── parsespec.py        # Utility to parse OpenAPI specs
├── arazzo_spec.yaml    # Example Arazzo spec file
├── output/             # Auto-generated directory for javascript function outputs
└── README.md           # Project README file
```

## License

Add license information

