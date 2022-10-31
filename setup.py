import sys
import subprocess
import pkg_resources

class SetupPrequisties(object):
    def __init__(self):
        self.required_packages = {
            'numpy',
            'tk', #package name of tkinter
            'pillow', #package name of PIL
            'pandas', 
            'sklearn',
            'ttkwidgets',
            'matplotlib',
            }
        self.python_version = sys.executable

    def check_installed_packages(self):
        print ("\nChecking for required packages...")
        self.installed = {pkg.key for pkg in pkg_resources.working_set}
        self.missing = self.required_packages - self.installed
    
    def install_missing(self):
        # subprocess.check_call([self.python_version, '-m', 'pip', 'install', *self.missing], stdout=subprocess.DEVNULL)
        subprocess.check_call([self.python_version, '-m', 'pip', 'install', *self.missing])

    def get_user_confirmation(self):
        print ("The following required packages are not installed: ")
        print ("   - {}".format(",\n   - ".join([*self.missing])))
        return input ("Install missing packages with pip for {}?  [Y/N] \n".format(self.python_version)).lower()

    def denied_installation(self):
        print ("No packages installed.")

    def nothing_missing(self):
        print ("\nAll required packages already installed, no action needed.\n")

    def __call__(self):
        self.check_installed_packages()
        if self.missing:
            user_input = self.get_user_confirmation()
            if user_input.lower() == 'y':
                self.install_missing()
            else:
                self.denied_installation()
        else:
            self.nothing_missing()
        
    
setup = SetupPrequisties()
setup()
# print (missing)
# print (sys.executable)
# if missing:
#     python = sys.executable
#     subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)