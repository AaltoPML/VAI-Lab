# AI assisted design

This framework aims to provide the means to easily build a fully operational Bayesian machine learning pipeline for different domains. 
This allows to adapt the machine learning algotithms to the task requirements and provide the output that best adapts to the problem needs.
Furthermore, its modular nature provides a way to intuitively combine certain modules for specific problems.

## UFA

The User Feedback Adaptation module provides the means to easily interact with the machine learning model to give feedback.
It allows to provide feedback for different domains, adapting the user's input to the corresponding input required by the model. 
At this stage there are 2 main feedback options:
- **Manual input**: Requires the user to indicate to which class the specified data corresponds to. 
In the current example, the model needs to classify images and the model requires expert knowledge for specific images.
The user needs to indicate which classes correspond to the image and save the results to send them to the model.
- **Interact with canvas**: Requires the user to give feedback to state-action pairs.
It opens a tab for each interactable object in the model and either requires adding new state-action samples or to modify the existing ones. 
In the current example, the model has two interactable objects that require feedback in two forms: (1) an _angle_ for the state and for the action or (2) a tuple of _cartesian coordinates_ for the state and for the action.

# Contact
- Chris McGreavy, chris.mcgreavy@aalto.fi
- Carlos Sevilla-Salcedo, carlos.sevillasalcedo@aalto.fi