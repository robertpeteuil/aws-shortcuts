AWS Shortcuts for controlling instances from the command line
=============================================================

List, start, stop and ssh to AWS instances using Name or Instance-ID
---------------------------------------------------------------------------------

|Code Climate| |GitHub issues| |GitHub release| |lang| |license|

--------------

This utility allows you to easily manage and connect to AWS instances using their name or instance-ID. It provides the ability to quickly list, start, stop and connect to instances by referencing their Name or instance-ID.

If start, stop, or ssh is specified with a NAME that occurs on multiple instances, the matching instances are listed and the user allowed to choose the intended instance. For example, if ``awss start Ubuntu`` is ran while there are multiple instance named Ubuntu, a listing of those instances would be displayed from which the user can choose which to start.

Overview:
---------

**awss** supports the four main commands of **list**, **start**, **stop**, and **ssh**.

- commands are executed by typing ``awss`` followed by the command name; for example: ``awss list``.
- Some commands require an additional paramter which specifies an instance, either by NAME or Instance-ID.
  - examples: ``awss ssh Ubuntu`` or ``awss start -i i-0c875fa80862d1b16``

Command Summary:
----------------

- SSH to an Instance: **awss ssh NAME** or **-i ID**
  -  calculates login-name based on image-type of the instance
  -  optionally override the calculated login-name
  -  optionally connect without PEM keys (if properly configured)
  -  command specific help available by typing ``awss ssh - h``
- List Instances: **awss list**
  -  list all instances
  -  list all running or stopped instances
  -  list instances with a specified name
  -  list instance with a specified instance-id
  -  command specific help available by typing ``awss list - h``
- Start Instance: **awss start NAME** or **-i ID**
  -  start an instance by name or instance-id
  -  command specific help available by typing ``awss start - h``
- Stop Instance: **awss stop NAME** or **-i ID**
  -  start an instance by name or instance-id
  -  command specific help available by typing ``awss stop - h``

Supported Platforms:
--------------------

-  Linux
-  macOS (OS X)
-  Windows 10 'Bash on Windows'

Pre-Requisites:
---------------

- Requires a python version of 2.7 or newer. Check by typing ``python -V``
- Requires Python package manager **pip**
  - can be installed with: ``sudo easy_install pip``
- Requires the following Python libraries:
  - **boto3** library (AWS Python library)
    - Installation and configuration info can be found `here <https://boto3.readthedocs.io/en/latest/guide/quickstart.html>`__
  - **future** library
    - can be installed by typing ``pip install future`` or ``pip install future --upgrade``
    - if the above command generated permission errors, use ``pip install future --upgrade --user``

.. |Code Climate| image:: https://codeclimate.com/github/robertpeteuil/aws-shortcuts/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/robertpeteuil/aws-shortcuts
.. |GitHub issues| image:: https://img.shields.io/github/issues/robertpeteuil/aws-shortcuts.svg
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |GitHub release| image:: https://img.shields.io/github/release/robertpeteuil/aws-shortcuts.svg?colorB=1c64bf
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |lang| image:: https://img.shields.io/badge/language-python-3572A5.svg?style=flat-square
   :target:
.. |license| image:: https://img.shields.io/github/license/robertpeteuil/aws-shortcuts.svg?colorB=1c64bf
   :target: https://github.com/robertpeteuil/aws-shortcuts
