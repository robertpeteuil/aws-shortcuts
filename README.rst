AWS Shortcuts for Command-Line Instance Control
===============================================

List, start, stop and ssh to AWS instances using Name, ID and Wilcards
----------------------------------------------------------------------


|TRAVIS| |AppVeyor| |Codacy Grade| |Codacy Cov| |PyPi release| |Py ver| |license sm|

--------------

AWS Shortcuts (awss) allows listing, starting, stopping and connecting to instances by name, instance-id, and supports wilcards.  The ``awss list`` command displays every tag & value for each instances along with their status and core info.  In the near future you will also be able to use any combination of ``Tag`` :  ``Value`` combinations when specifying instances.


Overview
--------

``awss`` has the following sub-commands: ``list``, ``start``, ``stop``, and ``ssh``.

- SSH to an Instance: ``awss ssh NAME`` or ``awss ssh -i ID``

  - Additional paramters described in  `Details`_.

- List Instances: ``awss list``

  - Additional paramters described in  `Details`_.

- Start Instance: ``awss start NAME`` or ``awss start -i ID``
- Stop Instance: ``awss stop NAME`` or ``awss stop -i ID``

Example output of ``awss list``
-------------------------------

.. image:: https://cloud.githubusercontent.com/assets/1554603/25595372/6c3bd5e2-2e79-11e7-9ebc-4730f93c2cb6.png

Details
-------

- SSH to Instance: ``awss ssh NAME`` or ``awss ssh -i ID``

  - typing ``awss ssh`` without a name or ID will display all running instances

    - this allows the user to select from the list if they can't remember the name.
    - this can be combined with wilcards, for example ``awss ssh U*``  to display
      a list of instances starting with "U" to select from.

  - the login-name is automatically calculated based on the image-type of the instance
  - override the calculated login-name ``-u USERNAME``
  - connect without PEM keys (if properly configured) ``-p``
  - command specific help ``awss ssh -h``

- List Instances: ``awss list``

  - list all instances (default), or use wilcards ``awss list D*``
  - list running instances ``-r`` or ``--running``
  - list stopped instances ``-s`` or ``--stopped``
  - list instances with specified name ``awss list NAME``
  - list instance with specified instance-id ``awss list -i ID``
  - instance-state and NAME may be combined in queries.

    - ex: list instances with NAME currently running: ``awss list NAME -r``

  - command specific help ``awss list -h``

- Start Instance: ``awss start NAME`` or ``awss start -i ID``

  - typing ``awss start`` without a name or ID will display all stopped instances

    - this allows the user to select from the list if they can't remember the name.
    - this can be combined with wilcards, for example ``awss start U*`` to display
      a list of instances starting with "U" to select from.

  - start instance by name or instance-id
  - command specific help ``awss start -h``

- Stop Instance: ``awss stop NAME`` or ``awss stop -i ID``

  - typing ``awss stop`` without a name or ID will display all running instances

    - this allows the user to select from the list if they can't remember the name.
    - this can be combined with wilcards, for example ``awss stop U*`` to display
      a list of instances starting with "U" to select from.

  - start instance by name or instance-id
  - command specific help ``awss stop -h``

Target Instance Determination
-----------------------------

The ``start``, ``stop``, and ``ssh`` commands check if multiple instances match the parameters. 
If so, the the matching instances are listed, and the user selects the intended target.

Example screenshot of selecting instance from list:

.. image:: https://cloud.githubusercontent.com/assets/1554603/25595396/84b4ef64-2e79-11e7-922f-d645b007af57.png


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

.. |Py ver| image:: https://img.shields.io/pypi/pyversions/awss.svg
   :target: https://pypi.python.org/pypi/bandit/
   :alt: Python Versions

.. |license sm| image:: https://img.shields.io/badge/license-MIT-1c64bf.svg?style=flat-square
   :target: https://github.com/robertpeteuil/aws-shortcuts


.. |GitHub issues| image:: https://img.shields.io/github/issues/robertpeteuil/aws-shortcuts.svg
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |GitHub release| image:: https://img.shields.io/github/release/robertpeteuil/aws-shortcuts.svg?colorB=1c64bf
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |Code Climate| image:: https://codeclimate.com/github/robertpeteuil/aws-shortcuts/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/robertpeteuil/aws-shortcuts
.. |lang| image:: https://img.shields.io/badge/language-python-3572A5.svg?style=flat-square
   :target: https://github.com/robertpeteuil/aws-shortcuts
.. |license| image:: https://img.shields.io/github/license/robertpeteuil/aws-shortcuts.svg?colorB=1c64bf
   :target: https://github.com/robertpeteuil/aws-shortcuts
