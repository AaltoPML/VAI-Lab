import aidesign.plugins as plug

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
                "class_list":['State_x',
                                'State_y',
                                'Action_x',
                                'Action_y']
                },
    "startpage": {
                "class_list":[] #need to find way of making multiple methods work
                }
}

test_name = "startpage"

ui_app = plug.UI.Container()
ui_app.set_UI_type(test_name)
ui_app.set_class_list(test_cases[test_name]["class_list"])

ui_app.launch()

