import aidesign as ai
import os

# from setup import SetupPrequisties

core = ai.Core()
core.load_config_file(os.path.join(
    ".", 
    "Data",
    'resources', 
    'xml_files', 
    'logisticregression_test.xml'))
# core.launch()
core.run()