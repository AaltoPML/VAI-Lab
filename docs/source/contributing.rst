Contributing
============

Starting to contribute to a new repo can be daunting and the architecture can be offputting. This section is meant to help you get introduced to the codebase and make your first contribution.

Where to start?
---------------

Jump in and break things!
^^^^^^^^^^^^^^^^^^^^^^^^^

If your preferred way of learning is to jump in a break things, a good starting point is to run an example file, e.g.:

.. code-block:: bash

    vai_lab --file ./examples/xml_files/user_feedback_demo.xml

which will call a module and plugin and give an example of the call stack.

Get a good grip on the code 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you prefer to learn by reading, the following sections will give you a high level overview of the codebase.

Overview
--------

The VAI-lab codebase consists of individual ``modules`` representing individual processes; for each module there are multiple ``plugins`` , which are specific methods or implementations of performing these processes. 

:: 

    For example, ``DataProcessing`` is a ``Module`` which will manipulate data in some way. The specific type of processing is determined by the ``plugin`` that is chosen. 
    
    Say we have some data and we want to change all the values to either a 0 or 1, we would use the ``binarizer`` plugin for the ``DataProcessing`` module.

While a ``plugin`` specifies the exact implementation to perform on a process, the ``core`` deals with setting up and executing the plugin. 

Each module contains a ``Core`` which dictates the required methods and attributes of a compatible ``plugin``, it also instantiates the ``plugin`` and executes it.

Supervisor ``Core``
-------------------

As well as each module having a ``Core``, there is an overarching ``Supervisor`` ``Core`` which calls each module sequentially, which in turn execute the ``plugin``.

Glossary
--------

``Module``: An container representing a generic process to manipulate or produce data - all modules are to be populated by a plugin.

``Plugin``: A specific implementation or method to carry out a process. Each plugin will be inserted into a module.

``Core``: Each module consists of a ``Core`` and a set of plugins. The core is responsible for performing the required background processes and handling the plugins
