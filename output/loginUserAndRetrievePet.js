
async function loginUserAndRetrievePet(workflowCtx, portal) {
    return {

      "loginStep": {
        name: "This step demonstrates the user login step",
        stepCallback: async (stepState) => {
          
        await portal.setConfig((defaultConfig) => ({
            ...defaultConfig,
        }));
        return workflowCtx.showEndpoint({
            description: `This step demonstrates the user login step`,
            endpointPermalink: "Not provided",
            verify: (response, setError) => {
              if (response.StatusCode != 200) {
                setError("Error text");
                return false;
              } else {
                return true;
              }
            },
          });
    
        },
      },

      "getPetStep": {
        name: "retrieve a pet by status from the GET pets endpoint",
        stepCallback: async (stepState) => {
          
        await portal.setConfig((defaultConfig) => ({
            ...defaultConfig,
        }));
        return workflowCtx.showEndpoint({
            description: `retrieve a pet by status from the GET pets endpoint`,
            endpointPermalink: "{$sourceDescriptions.petstoreDescription.url}#/paths/~1pet~1findByStatus/get",
            verify: (response, setError) => {
              if (response.StatusCode != 200) {
                setError("Error text");
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
