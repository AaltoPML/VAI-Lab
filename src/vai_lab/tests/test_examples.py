from glob import glob

import vai_lab as ai
from vai_lab._import_helper import get_lib_parent_dir

def test_examples():
    """
    Test launching GUI
    """
    scripts = glob(get_lib_parent_dir() + "/examples/xml_files/" + "*")
    for file in scripts:
        """Temp removal of userfeedback test - relies too heavily on GUI for github actions"""
        if "user_feedback" not in file:
            print (file)
            core = ai.Core()
            core.load_config_file(file)
            core._debug = True
            core.run()