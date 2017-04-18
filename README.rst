AWS Shortcuts for controlling instances from the command line
=============================================================

List, start, stop and ssh to AWS instances using Name or Instance-ID
---------------------------------------------------------------------------------

|Code Climate| |GitHub issues| |GitHub release| |lang| |license|

--------------

AWS Shortcuts utility (awss) provides an easy method to manage and connect to AWS instances.  It allows listing, starting, stoping and connecting to instances by Name or instance-ID.  Future updates will allow specifying instances by any ``Tag`` and ``Value`` combination.


Overview:
---------

``awss`` has the following sub-commands: ``list``, ``start``, ``stop``, and ``ssh``.

- SSH to an Instance: ``awss ssh NAME`` or ``aws ssh -i ID``
- List Instances: ``awss list`` or ``awss list --running``
- Start Instance: ``awss start NAME`` or ``awss start -i ID``
- Stop Instance: ``awss stop NAME`` or ``awss stop -i ID``
- The ``ssh`` and ``list`` commands allow additional paramters which are described in the following section.

Command Summary:
----------------

- SSH to an Instance: ``awss ssh NAME`` or ``awss ssh -i ID``

  - automatically calculates login-name based on image-type  of the instance
  - optionally override the calculated login-name ``-u USERNAME``
  - optionally connect without PEM keys (if properly configured) ``-p``
  - command specific help available by typing ``awss ssh -h``

- List Instances: ``awss list`` or ``awss list --running``

  - list all instances
  - list all running instances ``-r`` or ``--running``
  - list all stopped instances ``-s`` or ``--stopped``
  - list instances with a specified name ``awss list NAME``
  - list instance with a specified instance-id ``awss list -i ID``
  - command specific help available by typing ``awss list -h``

- Start Instance: ``awss start NAME`` or ``awss start -i ID``

  - start an instance by name or instance-id
  - command specific help available by typing ``awss start -h``

- Stop Instance: ``awss stop NAME`` or ``awss stop -i ID``

  - start an instance by name or instance-id
  - command specific help available by typing ``awss stop -h``

Instance Identification:
------------------------

The ``start``, ``stop``, and ``ssh`` commands verify that the action will be performed for the intended instance by checking for multiple instances that match the NAME and running-state expected by the command.

- For example, ``awss start Ubuntu`` will check for other instances named ``Ubuntu`` that are **stopped**.
- Because the ``start`` command will have no effect on **running** instances, they are ignored in the search.  Likewise, stopped instances are ignored when running the ``stop`` command.
- If multiple instances are found that match these conditions, they are listed and the user selects the intended instance.

Supported Platforms:
--------------------

-  Linux
-  macOS (OS X)
-  Windows

Pre-Requisites:
---------------

- Python version of 2.7 or newer. Check by typing ``python -V``
- Python package manager ``pip``

  - can be installed with: ``sudo easy_install pip``

- Requires the following Python libraries:

  - ``boto3`` library (AWS Python library)

    - Installation and configuration info can be found `here  <https://boto3.readthedocs.io/en/latest/guide/quickstart.html>`__

  - ``future`` library

    - can be installed by typing ``pip install future`` or ``pip install future --upgrade``
    - if the above command generated permission errors, use ``pip install future --upgrade --user``

.. |Code Climate| image:: https://codeclimate.com/github/robertpeteuil/aws-shortcuts/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/robertpeteuil/aws-shortcuts
.. |GitHub issues| image:: https://img.shields.io/github/issues/robertpeteuil/aws-shortcuts.svg
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |GitHub release| image:: https://img.shields.io/github/release/robertpeteuil/aws-shortcuts.svg?colorB=1c64bf
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |lang| image:: https://img.shields.io/badge/language-python-3572A5.svg?style=flat-square
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |license| image:: https://img.shields.io/github/license/robertpeteuil/aws-shortcuts.svg?colorB=1c64bf
   :target: https://github.com/robertpeteuil/aws-shortcuts
