![AIFRED](https://user-images.githubusercontent.com/22427519/168077112-840bc213-3804-45de-9174-928a203df555.png)

This framework aims to provide the means to easily build a fully operational Machine Learning pipeline across different domains. 
This allows to adapt the machine learning algorithms to the task requirements and provide the output that best adapts to the problem needs.
Furthermore, its modular nature provides a way to intuitively combine modules for specific problems.

The `Core` class in script `AI_design_core.py` inherits from the `Settings`class, loading the modules declared in the XML file, dynamically importing, instantiating and executing them. 

## Launching Core

Simple launchers were added to `Core` for easy execution. To load and execute core using the Initialisation GUI, run the following:

```python
import aidesign as ai

core = ai.Core()
core.launch_canvas()
core.run()
```

or to execute the pipeline from an existing config file, use: 

```python
import aidesign as ai

core = ai.Core()
core.load_config_file("<path_to_config_file>)
core.run()
```

# Initialisation

## Pipeline definition via canvas interaction

The AID module allows to define a pipeline and the relations within by drawing a flowchart on a canvas. This canvas always starts with an `initialiser` module and an `output` module and allows to define any number of modules between these two. To do so, the user needs to define the modules and the relations between them.

![PipelineLoop](https://user-images.githubusercontent.com/22427519/168080733-4c88d004-9ca6-486e-bd8d-cc7050e93515.PNG)

### Modules
At this moment, there are 7 possible modules for AID. `initialiser` and `output` are compulsory for the pipeline, the rest of them can be freely placed in the canvas. These are:
 - `Data processing`.
 - `Modelling`.
 - `Decision making`.
 - `User Feedback Adaptation`.
 - `Input data`.

If you click on a module and drag it you can modify its position on the canvas.
Finally, they can be deleted by clicking on the desired module and then clicking on the `Delete selection` button.

### Module joining
Each module object has a number of circles that can be used to join two modules. The initially clicked circle will be identified as the parent and the second one as the child (the output of the father is fed to the input of the child). There can be only one connection from each circle. As of this version, if you need to edit an existing connection you need to delete one of the connected modules.

### Loops
If you click on the canvas and drag, you can draw a rectangle that defines which modules are inside the loop. Upon releasing the button you are requested to input what type of loop you want and what condition should be fulfilled to end the loop.

### Editing
You can edit the module's displayed name and the loop's conditions by double-clicking on them and making any desired changes.

### Reset
Upon clicking the reset button, all objects in the canvas are deleted except for the default modules (`initialiser` and `output`).


## Pipeline uploading via XML file

The pipeline can also be defined uploading an existing XML file. The structure of the XML file is described in the Back-end section.

## UFA

The User Feedback Adaptation module provides the means to easily interact with the machine learning model to give feedback.
It allows the user to provide feedback for different domains, adapting the user's input to the corresponding input required by the model. 
At this stage there are 2 main feedback options.

### `Manual input`
Requires the user to indicate to which class the specified data corresponds to. 
In the current example, the model needs to classify images and the model requires expert knowledge for specific images.
The user needs to indicate which classes correspond to the image and save the results to send them to the model.

### `Interact with canvas`
Requires the user to give feedback to state-action pairs.
It opens a tab for each interactable object in the model and either requires adding new state-action samples or to modify the existing ones. 
In the current example, the model has two interactable objects that require feedback in two forms: (1) an _angle_ for the state and for the action or (2) a tuple of _Cartesian coordinates_ for the state and for the action. It has been adapted to be able to give feedback to any number of objects. These, at the same time, can be either `sliding` or `rotating` objects. Specifically, `sliding` refers to objects that need Cartesian feedback in a two-dimensional space, while `rotating` refers to objects that require an angle. In order to give feedback, you can choose to either move the corresponding state-action pairs on the canvas or directly edit the tree view display. This last option results in an automatic update on the canvas of the state-action location.

# Back-end

## Filetree structure and modularisation
To support modularisation and maintaining the modules as plugins, they need to be independent of the rest of the file structure. 
Each module has:
    - A root folder carrying its name (e.g. `GUI`)
    - A core script which calls the plugins (e.g. `GUI_core.py`)
    - An Abstract Class which enforces plugin structure (e.g. `UserInterfaceClass.py`)
    - A folder containing all plugins relevant to that module

```bash
├── aidesign/
│   ├── GUI/
│   │   ├── plugins/
│   │   │   ├── resources/
│   │   │   │   ├── Assets/
│   │   │   │   │   ├── back_arrow.png
│   │   │   │   │   ├── forw_arrow.png
│   │   │   │   │   ├── UFAIcon.ico
│   │   │   │   │   └── UFAIcon_name.png
│   │   │   │   └── example_radiography_images/
│   │   │   │       ├── 00028173_005.png
│   │   │   │       ├── 00028179_000.png
│   │   │   │       ├── 00028198_002.png
│   │   │   │       ├── 00028208_035.png
│   │   │   │       ├── 00028211_021.png
│   │   │   │       ├── 00028253_000.png
│   │   │   │       └── 00028279_000.png
│   │   │   ├── canvas_input.py
│   │   │   ├── __init__.py
│   │   │   ├── manual_input.py
│   │   │   └── startpage.py
│   │   ├── GUI_core.py
│   │   ├── __init__.py
│   │   └── UserInterfaceClass.py
│   ├── utils/
│   └── __init__.py
├── README.md
├── run_UI.py
└── setup.py
```

## Self-Contained Assets

As mentioned above, the assets required by individual modules are now fully contained within the modules themselves, to both keeps things clean and to avoid messy paths and confusion in future. Assets for the UI package are now in the directory: 
```bash
./ai-assisted-design-framework/modules/UI/resources/
```

## XML tags

All tags must currently be nested inside the `Settings` tag (This may be removed later):
```XML
<Settings>
    ...
</Settings>
```

## Pipeline Definition

The pipeline structure is defined between the `pipeline` tags:
```XML
<pipeline>
    ...
</pipeline>
```

### Initialise
The `Initialise` tag is the dedicated entry point to the pipeline. No other entry points can be declared. 

Current options:
 - `name`: attribute for user defined name
 - `initial_data`: element for declaring directory for initial data
 - `goal file`: element where the objective for the pipeline is declared (consider renaming)
 - `relationships`: User defined names of modules this one is connected to
```XML
<Initialise name="Init">
        <initial_data file="../resources/intial_data_test.csv" />
        <goal file="../resources/design_goals_test.csv" />&gt;
        <relationships>
            <child name="My First GUI Module" />
        </relationships>
</Initialise>
```

### Loops
Loop tags are used to iterate over a given set of modules until a condition is met. Loops can be nested and named.  See `example_config.xml` for full example.
Current options:
 - `type`: what variety of loop will this be: `for`, `while`, `manual`(user defined stopping condition on-the-fly)
 - `condition`: Termination condition for the loop. I'm not sure how to deal with the criteria for `while` loops
 - `name`: User defined name for loop 
```XML
<loop type="for" condition="10" name="For Loop 1">
    ...
</loop>
```

### Modules
Modules are declared by tags matching their names, e.g. the GUI module is loaded with the `GUI` tag:

Required:
 - `name`: Unique user defined name for module, so can be referenced later
 - `plugin`: The type of plugin to be loaded into the module, along with associated options.
 - `relationships`: User-defined names of the `parent` modules which this module receives data from and `child` modules that this module passes data to. Example:
```XML
     <GUI name="My First GUI Module">
         <plugin type="manual">
             <class_list>
                Atelectasis
                Cardiomelagy
                Effusion
                Infiltration
                Mass
                Nodule
                Pneumonia
                Pneumothorax
            </class_list>
        </plugin>
        <relationships>
            <parent name="Init" />
            <child name="Data Processing 1" />
        </relationships>
    </GUI>
```

### Output 
Dedicated exit point for the pipeline, where the save file is declared along with the data to be saved

```XML
<Output>
    <out_data>
        all
    </out_data>
    <save_to file="../resources/output_test.csv" />
    <relationships>
        <parent name="My Second GUI Module" />
    </relationships>
</Output>
```

## Data Definition
The structure of the data which will be passed through the pipeline. Currently, limited placeholder tags are declared until we have a better idea of what we want here. The structure of the data must be declared between the `datastructure` tags: 

```XML
<datastructure name="user_defined_name">
    ...
</datastructure>
```

```XML
<datastructure name="datatest">
        <data_fields>
            State_0
            State_1
            Action
            Reward
            Termination
            Goal
        </data_fields>
    </datastructure>
```

### Writing Data
Two methods are given to add data to the XML file. One for modules (`append_pipeline_module_to_file`) and one for data structures (`append_data_structure_field_to_file`).

## Plugin Option Loader

In script `utils/plugin_helpers.py`, class `PluginSpecs` scrapes options inside plugin scripts to populate a dict of plugins for each module. Additionally, other plugin options are defined in-script with the form: `_PLUGIN_<name of option>`, for example:

```python
_PLUGIN_CLASS_NAME = "ManualInput"
_PLUGIN_CLASS_DESCRIPTION = "Method of user feedback for binary or classification data"
_PLUGIN_READABLE_NAMES = {"default":"manual","aliases":["binary,classification"]}
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,
                            "required_children": None,}
_PLUGIN_REQUIRED_SETTINGS = {"class_list":"list","image_dir":"str"}
_PLUGIN_OPTIONAL_SETTINGS = {}
```

### Functionality 
`PluginSpecs` defines some convenience methods for quickly grabbing all module options, including:

```python
def names(self):
    return self.get_option_specs("_PLUGIN_READABLE_NAMES")

def class_names(self):
    return self.get_option_specs("_PLUGIN_CLASS_NAME")

def class_descriptions(self):
        return self.get_option_specs("_PLUGIN_CLASS_DESCRIPTION")

def required_settings(self):
    return self.get_option_specs("_PLUGIN_REQUIRED_SETTINGS")
```

# Contact
- Chris McGreavy, chris.mcgreavy@aalto.fi
- Carlos Sevilla-Salcedo, carlos.sevillasalcedo@aalto.fi
