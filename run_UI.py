import aidesign as ai
# from setup import SetupPrequisties

core = ai.Core()
core.load_config_file("./Data/resources/xml_files/data_passing_canvas_test.xml")
# core.launch()
core.run()

# ['State_a', 'Action_a']
# ['State_x', 'State_y', 'Action_x', 'Action_y']
# [['State_a', 'Action_a'],['State_x', 'State_y', 'Action_x', 'Action_y']]

# ['a', 'b', 'c', 'd']