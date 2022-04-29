import ast
import os

def get_plugin_specs(module, filename):
    with open(filename, "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer(module)
    analyzer.visit(tree)
    print(analyzer.stats)


class Analyzer(ast.NodeVisitor):
    def __init__(self,module):
        self.module = module
        self.stats = {module:{}}

    def visit_Assign(self, node):
        if type(node.targets[0]) == ast.Name:
            if "_PLUGIN" in node.targets[0].id:
                key = node.targets[0].id
                val = eval(compile(ast.Expression(node.value),"<ast expression>","eval"))
                self.stats[key] = val

def get_clean_module_dirs(root_dir:str=None) -> list:
    excludes = ["__init__.py","__pycache__","resources"]
    if os.path.exists(root_dir):
        mod_dirs = os.listdir(root_dir)
        for ex in excludes:
            if ex in mod_dirs:
                mod_dirs.remove(ex)
        return mod_dirs
    else:
        return []

def get_plugin_files(root_dir=None):
    if root_dir is None:
        root_dir = os.path.dirname(os.path.realpath(__file__+"/.."))
    mod_dir_store = {}
    mod_folders = get_clean_module_dirs(root_dir)
    for mf in mod_folders:
        mod_path = os.path.join(root_dir,mf,"plugins")
        plugins = get_clean_module_dirs(mod_path)
        mod_dir_store[mf] = {}
        mod_dir_store[mf]["root"] = mod_path
        mod_dir_store[mf]["files"] = [f for f in plugins if f.endswith(".py")]
    return mod_dir_store
    

if __name__ == "__main__":
    plugin_dirs = get_plugin_files()
    for m in plugin_dirs.keys():
        for p in plugin_dirs[m]["files"]:
            get_plugin_specs(m,os.path.join(plugin_dirs[m]["root"],p))
    # module = "GUI"
    # filename = "/home/chris/github/ai-assisted-design-framework/aidesign/GUI/plugins/ManualInput.py"
    # main(module,filename)