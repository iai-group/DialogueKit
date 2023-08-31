Installation
============

Install as a package
--------------------

DialogueKit is published to PyPI. Install it by running:

  .. code-block:: shell
    pip install dialoguekit


Follow the commands below to install DialogueKit from a specific commit or straight from GitHub.

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
