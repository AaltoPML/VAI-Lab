from glob import glob

import vai_lab as ai
from vai_lab._import_helper import get_lib_parent_dir

def test_examples():
    """
    Test launching GUI
    """
    scripts = glob(get_lib_parent_dir() + "/examples/xml_files/basic_operation.xml")
    for file in scripts:
        print("example script: "+ file)
        core = ai.Core()
        core.load_config_file(file)
        core._debug = False
        core.run()

test_examples()