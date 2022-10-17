import aidesign as ai

core = ai.Core()

# core.load_config_file(
#     ("./examples",
#     "xml_files",
#     'crystalDesign_v0.xml'))
core.load_config_file("\\home.org.aalto.fi\sevillc1\data\Desktop\TEst.xml")

core.run()