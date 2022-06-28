Installation
====================

Install as a package
--------------------

**Note:** *Packaging is still a work in progress and may not work perfectly.*

As of now DialogueKit is not published as a package, but it is still possible to install it with pip.
The command will install the latest version from the main branch.

* On Windows you may need to run this command before pip installing
  
.. code-block:: shell

    ssh -t git github.com    

* pip install

.. code-block:: shell

    pip install git+ssh://git@github.com/iai-group/dialoguekit.git

If you want to specify a specific commit as the source of the package append the commit hash to the end of the command separated with a "@".

* Specific commit as the source of the package.

.. code-block:: shell

    pip install git+ssh://git@github.com/iai-group/dialoguekit.git@faa5c1fca37aaa275105cc1ca7698783719551c2



