from vai_lab._plugin_templates import UI

class UserFeedbackTemplate(UI):
    """UserFeedbackTemplate directly duplicates:
        vai_lab.UserInteraction.User_Interaction_template
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)