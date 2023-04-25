import aidesign as ai

core = ai.Core()

core.load_config_file(
    ("./examples",
    "xml_files",
    'BO_demo.xml'))

core.run()