import aidesign as ai

core = ai.Core()

core.load_config_file(
    ("./examples",
    "xml_files",
    'crystalDesign_v2.xml'))

core.run()