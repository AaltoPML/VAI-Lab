import vai_lab as ai

def test_launch():
    """
    Test launching GUI
    """
    core = ai.Core()    
    core._debug = True
    core.run()
