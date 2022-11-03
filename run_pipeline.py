import vai_lab as ai

core = ai.Core()

core.load_config_file(
    ("./examples",
    "xml_files",
    'pybullet_env_example.xml'))
    
core.run()