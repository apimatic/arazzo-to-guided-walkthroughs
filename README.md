# Arazzo Walkthrough Translator

Arazzo Walkthrough Translator is a Python-based tool that automates the generation of Guided Walkthrough functions from OpenAPI's new Arazzo spec format. The tool processes the Arazzo spec, which acts as an overlay on the OpenAPI spec, defining workflows using multiple endpoints, and outputs JavaScript functions for each workflow.

## Features
- **Automated Translation**: Converts Arazzo specs into Guided Walkthrough JavaScript functions.
- **Multi-Workflow Support**: Handles multiple workflows defined in a single Arazzo spec.
- **Output Zipping**: Generates a zip file containing all the JavaScript functions for easy integration.


## Branches
This project includes two branches, each containing different application setups:

1. **`console-app`**: A command-line application for translating Arazzo specs.
2. **`flask-app`**: A Flask-based web application implementing REST API for translating Arazzo specs.

## Getting Started
Based on what type of the app you want you can have look through the branches and switch between them.

### Switching Branches
To switch between branches, use the following Git commands:

```sh
# Switch to the console-app branch
git checkout console-app

# Switch to the flask-app branch
git checkout flask-app
```

### File Structures

#### Console App Branch
```
console-app/
├── main.py             # Entry point for the console application
├── translator.py       # Contains the Arazzo spec to JavaScript function translation logic
├── parsespec.py        # Contains the code to parse the yml and fetch workflows, endpoints, source url
├── requirements.txt    # Python dependencies
└── README.md           # README file with instructions on how to setup and run the console app
```

#### Flask App Branch
```
flask-app/
├── app.py              # Entry point for the Flask web application
├── translator.py       # Contains the Arazzo spec to JavaScript function translation logic
├── parsespec.py        # Contains the code to parse the yml and fetch workflows, endpoints, source url
├── requirements.txt    # Python dependencies
└── README.md           # README file with instructions on how to setup and run the flask app
```

## Arazzo Spec

The Arazzo spec format extends OpenAPI specs to define workflows involving multiple endpoints. It provides a structured way to create step-by-step processes for API interactions. 

### Sample Arazzo Spec
```yml
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

## Guided Walkthrough 

Guided Walkthroughs are an APIMAtic docs' exclusive feature, that implement a way to render a workflow in a series of steps to help a user get a hang of the documentation.

### Sample Guided Walkthrough Javascript Function

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

