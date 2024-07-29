# Arazzo Walkthrough Translator

Arazzo Walkthrough Translator is a Python-based tool that automates the generation of Guided Walkthrough functions from OpenAPI's new Arazzo spec format. The tool processes the Arazzo spec, which acts as an overlay on the OpenAPI spec, defining workflows using multiple endpoints, and outputs JavaScript functions for each workflow.

## Features
- **Automated Translation**: Converts Arazzo specs into Guided Walkthrough JavaScript functions.
- **Multi-Workflow Support**: Handles multiple workflows defined in a single Arazzo spec.
- **Output Zipping**: Generates a zip file containing all the JavaScript functions for easy integration.


## Branches
This project includes two branches, each containing different application setups:

1. **`console-app`**: A command-line application for translating Arazzo specs.
2. **`flask-app`**: A Flask-based web application for translating Arazzo specs.

## Getting Started

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
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

#### Flask App Branch
```
flask-app/
├── app.py              # Entry point for the Flask web application
├── translator.py       # Contains the Arazzo spec to JavaScript function translation logic
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Arazzo Spec

The Arazzo spec format extends OpenAPI specs to define workflows involving multiple endpoints. It provides a structured way to create step-by-step processes for API interactions. 

### Sample Arazzo Spec
```json
{
  "workflows": [
    {
      "name": "Sample Workflow",
      "steps": [
        {
          "action": "GET",
          "endpoint": "/api/v1/resource",
          "description": "Fetch resource"
        },
        {
          "action": "POST",
          "endpoint": "/api/v1/resource",
          "description": "Create resource"
        }
      ]
    }
  ]
}
```

## Sample Guided Walkthrough JavaScript Function

Here's a sample JavaScript function generated from the Arazzo spec:

```javascript
function sampleWorkflow() {
  fetch('/api/v1/resource')
    .then(response => response.json())
    .then(data => {
      console.log('Fetched resource:', data);
      
      return fetch('/api/v1/resource', {
        method: 'POST',
        body: JSON.stringify({ /* resource data */ }),
        headers: { 'Content-Type': 'application/json' }
      });
    })
    .then(response => response.json())
    .then(data => {
      console.log('Created resource:', data);
    })
    .catch(error => console.error('Error:', error));
}
```


## License

Add license information

