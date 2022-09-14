import aidesign as ai
import os

# from setup import SetupPrequisties

core = ai.Core()
core.load_config_file(os.path.join(
    "./examples",
    "xml_files",
    'basic_operation.xml'))
core.run()