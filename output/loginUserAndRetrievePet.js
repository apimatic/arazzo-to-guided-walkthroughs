
async function loginUserAndRetrievePet(workflowCtx, portal) {
    return {

    "UpdatePetWithForm": {
        name: "This step is to update pet with form",
        stepCallback: async (stepState) => {
            
            await portal.setConfig((defaultConfig) => {
                return {
                    ...defaultConfig,
                    
                };
            });
            return workflowCtx.showEndpoint({
                description: `This step is to update pet with form`,
                endpointPermalink: "$e/pet/updatePetWithForm",
                args: {
                    petId: 10, name: "TestVal", status: "TestVal"
                },
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
            const previousStepState = stepState?.["UpdatePetWithForm"];
            await portal.setConfig((defaultConfig) => {
                return {
                    ...defaultConfig,
                    config: { ...defaultConfig.config, "api_key": "shouldWork" }
                };
            });
            return workflowCtx.showEndpoint({
                description: `retrieve a pet by status from the GET pets endpoint`,
                endpointPermalink: "$e/pet/deletePet",
                args: {
                    petId: 10
                },
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
