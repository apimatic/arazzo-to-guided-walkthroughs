# Arazzo Walkthrough Translator

Arazzo Walkthrough Translator is a Python-based tool that automates the generation of Guided Walkthrough functions from OpenAPI's new Arazzo spec format. The tool processes the Arazzo spec, which acts as an overlay on the OpenAPI spec, defining workflows using multiple endpoints, and outputs JavaScript functions for each workflow.

## Features
- **Automated Translation**: Converts Arazzo specs into Guided Walkthrough JavaScript functions.
- **Multi-Workflow Support**: Handles multiple workflows defined in a single Arazzo spec.
- **Output Zipping**: Generates a zip file containing all the JavaScript functions for easy integration.

## File Structure
```
console-app/
├── app.py             # Entry point for the console application
├── translator.py       # Contains the Arazzo spec to JavaScript function translation logic
├── parsespec.py        # Contains the code to parse the yml and fetch workflows, endpoints, source url
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Getting Started

### Installation

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Switch to the Flask app branch:**
   ```sh
   git checkout flask-app
   ```

3. **Install Dependencies:**
   ```sh
   pip install pyyaml requests flask
   ```

4. **Add the Arazzo spec file:**
   Place your `arazzo-specfile.yml` in the root directory of the project.

5. **Set the Flask app environment variable and run the application:**
   ```sh
   export FLASK_APP=app.py
   flask run
   ```

   Alternatively, on Windows, you can use:
   ```sh
   set FLASK_APP=app.py
   flask run
   ```

   Or use `python -m flask`:
   ```sh
   python -m flask run --app app.py
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
arazzo: 1.0.0
info:
  title: A pet purchasing workflow
  summary: This Arazzo Description showcases the workflow for how to purchase a pet through a sequence of API calls
  description: |
      This Arazzo Description walks you through the workflow and steps of `searching` for, `selecting`, and `purchasing` an available pet.
  version: 1.0.1
sourceDescriptions:
- name: petStoreDescription
  url: https://github.com/swagger-api/swagger-petstore/blob/master/src/main/resources/openapi.yaml
  type: openapi

workflows:
- workflowId: loginUserAndRetrievePet
  summary: Login User and then retrieve pets
  description: This workflow lays out the steps to login a user and then retrieve pets
  inputs:
      type: object
      properties:
          username:
              type: string
          password:
              type: string
  steps:
  - stepId: loginStep
    description: This step demonstrates the user login step
    operationId: loginUser
    parameters:
      # parameters to inject into the loginUser operation (parameter name must be resolvable at the referenced operation and the value is determined using {expression} syntax)
      - name: username
        in: query
        value: $inputs.username
      - name: password
        in: query
        value: $inputs.password
    successCriteria:
      # assertions to determine step was successful
      - condition: $statusCode == 200
    outputs:
      # outputs from this step
      tokenExpires: $response.header.X-Expires-After
      rateLimit: $response.header.X-Rate-Limit
      sessionToken: $response.body
  - stepId: getPetStep
    description: retrieve a pet by status from the GET pets endpoint
    operationPath: '{$sourceDescriptions.petstoreDescription.url}#/paths/~1pet~1findByStatus/get'
    parameters:
      - name: status
        in: query
        value: 'available'
      - name: Authorization
        in: header
        value: $steps.loginUser.outputs.sessionToken
    successCriteria:
      - condition: $statusCode == 200
    outputs:
      # outputs from this step
      availablePets: $response.body
  outputs:
      available: $steps.getPetStep.availablePets
```

## Example Guided Walkthrough script
Here's an example of what your generated walkthrough will look like:

```javascript
async function SampleWorkflow(workflowCtx, portal) {
 return {
   "Step 1": {
     name: "How to Get Access Token",
     stepCallback: async () => {
       return workflowCtx.showContent(`## Introduction
This is a guided walkthrough.`);
     },
   },
   "Step 2": {
     name: "Get Session Token",
     stepCallback: async (stepState) => {
       await portal.setConfig((defaultConfig) => ({}));
       return workflowCtx.showEndpoint({
         description:
           "This endpoint initiates session management and returns an access token and client ID that is required in subsequent API requests.",
         endpointPermalink: "$e/Session%20Management/StartSession",
         verify: (response, setError) => {
           if (response.StatusCode == 401 || response.StatusCode == 400) {
             setError("Authentication Token is Required");
             return false;
           } else if (response.StatusCode == 200) {
             return true;
           } else {
             setError(
               "API Call wasn't able to get a valid response. Please try again."
             );
             return false;
           }
         },
       });
     },
   },
   "Step 3": {
     name: "Get the List of Active Customer",
     stepCallback: async (stepState) => {
       const step2State = stepState?.["Step 2"];
       await portal.setConfig((defaultConfig) => {
         return {
           ...defaultConfig,
           auth: {
             ...defaultConfig.auth,
             bearerAuth: {
               ...defaultConfig.auth.bearerAuth,
               AccessToken: step2State.data?.sessionToken,
             },
           },
           config: {
             ...defaultConfig.config,
           },
         };
       });
       return workflowCtx.showEndpoint({
         description: "This step fetches the list of active customers.",
         endpointPermalink: "$e/Management/ListActiveCustomers",
         args: {
           body: {
             ClientID: step2State.data?.clientID,
             ClientSecret: step2State.requestData?.args?.body?.clientSecret
           },
         },
         verify: (response, setError) => {
           if (response.StatusCode != 200) {
             setError("Oops your request failed");
             return false;
           } else {
             return true;
           }
         },
       });
     },
   },
 };
}
```

## License

Add license information
