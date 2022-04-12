import aidesign as ai

test_cases = {
    "manual": {
                "class_list": ['Atelectasis',
                                'Cardiomelagy',
                                'Effusion',
                                'Infiltration',
                                'Mass',
                                'Nodule',
                                'Pneumonia',
                                'Pneumothorax'
                                ]
                },
    "canvas": {
                "class_list":[['State_a', 'Action_a',], 
                            ['State_x', 'State_y', 'Action_x', 'Action_y'], 
                           ['State_x', 'State_y', 'Action_x', 'Action_y']]

                },
    "startpage": {
                "class_list":[] # This is currently set by default in GUI_core.py (need to find a better method)
                }
}

test_name = "canvas"

ui_app = ai.GUI()
ui_app.plugin_name(test_name)
ui_app.set_class_list(test_cases[test_name]["class_list"])

ui_app.launch()

