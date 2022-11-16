import vai_lab as ai

def test_examples():
    """
    Test launching GUI
    """
    core = ai.Core()
    core.load_config_file("./examples/xml_files/regression_demo.xml")
    core._debug = True
    core.run()

