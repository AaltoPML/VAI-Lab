from vai_lab._plugin_templates import UI

class UserInterfaceClass(UI):
    """UserInterfaceClass directly duplicates:
        aidesign.UserInteraction.User_Interaction_template
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)