AWS Shortcuts for Command-Line Instance Control
===============================================

List, start, stop and ssh to AWS instances using Name or Instance-ID
---------------------------------------------------------------------------------


|TRAVIS| |AppVeyor| |Codacy Grade| |Codacy Cov| |PyPi release| |lang| |license|

--------------

AWS Shortcuts (awss) allows listing, starting, stopping and connecting to instances by name or instance-id.  Future versions will also allow referencing instances with any ``Tag`` :  ``Value`` combination.


Overview
--------

``awss`` has the following sub-commands: ``list``, ``start``, ``stop``, and ``ssh``.

- SSH to an Instance: ``awss ssh NAME`` or ``aws ssh -i ID``

  - Additional paramters described in  `Details`_.

- List Instances: ``awss list``

  - Additional paramters described in  `Details`_.

- Start Instance: ``awss start NAME`` or ``awss start -i ID``
- Stop Instance: ``awss stop NAME`` or ``awss stop -i ID``

Details
-------

- SSH to Instance: ``awss ssh NAME`` or ``awss ssh -i ID``

  - automatically calculates login-name based on the image-type of the instance
  - override the calculated login-name ``-u USERNAME``
  - connect without PEM keys (if properly configured) ``-p``
  - command specific help ``awss ssh -h``

- List Instances: ``awss list``

  - list all instances (default).
  - list running instances ``-r`` or ``--running``
  - list stopped instances ``-s`` or ``--stopped``
  - list instances with specified name ``awss list NAME``
  - list instance with specified instance-id ``awss list -i ID``
  - instance-state and NAME may be combined in queries.

    - ex: list instances with NAME currently running: ``awss list NAME -r``

  - command specific help ``awss list -h``

- Start Instance: ``awss start NAME`` or ``awss start -i ID``

  - start instance by name or instance-id
  - command specific help ``awss start -h``

- Stop Instance: ``awss stop NAME`` or ``awss stop -i ID``

  - start instance by name or instance-id
  - command specific help ``awss stop -h``

Target Instance Verification
----------------------------

The ``start``, ``stop``, and ``ssh`` commands verify that their action will apply to only one instance.

- This check is performed by looking for other instances that match:

  - the instance-specification given (name or ID).
  - the running-state appropriate for the command.

- If multiple instances match these conditions, they are listed and the user selects the intended target.

The **running-state** appropriate for each command is as follows:

- The ``ssh`` command looks for **running** instances (it cannot connect to stopped instanced).
- The ``stop`` command looks for **running** instances (it cannot stop instances that are already stopped).
- The ``start`` command looks for **stopped** instances (it cannot start instances that are already started).
- The ``list`` command looks at all instances, unless optional parameters have been specified to narrow its search to **running**, **stopped** instances.


Platforms & Python Versions Tested
----------------------------------

Python 2.7, 3.3, 3.4, 3.5, 3.6

Platforms:

- Linux
- macOS (OS X)
- Windows

Installation
------------

This utility can be installed with ``pip``:

.. code:: shell

  pip install awss


.. |PyPi release| image:: https://img.shields.io/pypi/v/awss.svg
   :target: https://pypi.python.org/pypi/awss

.. |Travis| image:: https://travis-ci.org/robertpeteuil/aws-shortcuts.svg?branch=master
   :target: https://travis-ci.org/robertpeteuil/aws-shortcuts

.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/1meclb632h49sik7/branch/master?svg=true
   :target: https://ci.appveyor.com/project/robertpeteuil/aws-shortcuts/branch/master

.. |Codacy Grade| image:: https://api.codacy.com/project/badge/Grade/477279a80d31407a99fb3c3551e066cb
   :target: https://www.codacy.com/app/robertpeteuil/aws-shortcuts?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=robertpeteuil/aws-shortcuts&amp;utm_campaign=Badge_Grade
.. |Codacy Cov| image:: https://api.codacy.com/project/badge/Coverage/477279a80d31407a99fb3c3551e066cb
   :target: https://www.codacy.com/app/robertpeteuil/aws-shortcuts?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=robertpeteuil/aws-shortcuts&amp;utm_campaign=Badge_Coverage
.. |license| image:: https://img.shields.io/github/license/robertpeteuil/aws-shortcuts.svg?colorB=1c64bf
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |lang| image:: https://img.shields.io/badge/language-python-3572A5.svg?style=flat-square
   :target: https://github.com/robertpeteuil/aws-shortcuts

.. |GitHub issues| image:: https://img.shields.io/github/issues/robertpeteuil/aws-shortcuts.svg
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |GitHub release| image:: https://img.shields.io/github/release/robertpeteuil/aws-shortcuts.svg?colorB=1c64bf
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |Code Climate| image:: https://codeclimate.com/github/robertpeteuil/aws-shortcuts/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/robertpeteuil/aws-shortcuts
