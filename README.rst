AWS Shortcuts for Command-Line Instance Control
===============================================

List, start, stop and ssh to AWS instances using Name, ID and wildcards
-----------------------------------------------------------------------


|TRAVIS| |AppVeyor| |Codacy Grade| |Codacy Cov| |PyPi release| |Py ver| |PyL|

--------------

AWS Shortcuts (awss) allows listing, starting, stopping and connecting to instances by name, partial names with wilcards, or instance-id.  The instance information listed includes: all tags & values, name, current-state, instance-id and image-name.

A coming update will add the ability to target instances with **Tag : Value** combinations.
For example: specify instance where Name starts with "Ub*", Tag "Project" = "SecretProject" and Tag "Role" = "Development".


Overview
--------

**awss** has the following sub-commands: **list**, **start**, **stop**, and **ssh**.

- SSH to an Instance:  **awss ssh NAME**

  - Additional paramters described in  `Details`_.

- List Instances:  **awss list**

  - Additional paramters described in  `Details`_.

- Start Instance:  **awss start NAME**
- Stop Instance:  **awss stop NAME**

Example screenshots
-------------------

**"awss list" - list instance details (tag keys are listed in blue)**

.. image:: https://cloud.githubusercontent.com/assets/1554603/25595372/6c3bd5e2-2e79-11e7-9ebc-4730f93c2cb6.png

**"awss start" using Name with wildcard -> duplicate results -> selecting target from list**

.. image:: https://cloud.githubusercontent.com/assets/1554603/25595396/84b4ef64-2e79-11e7-922f-d645b007af57.png


Tested Platforms & Python Versions
----------------------------------

Python 2.7, 3.3, 3.4, 3.5, 3.6

Platforms:

- Linux
- macOS (OS X)
- Windows

Installation
------------

This utility can be installed with **pip**:

.. code:: shell

  pip install awss



Details
-------

- SSH to Instance: **awss ssh NAME** or **awss ssh -i ID**

  - typing **awss ssh** without a name or ID will display all running instances

    - this allows the user to select from the list if they can't remember the name.
    - this can be combined with wilcards, for example **awss ssh U\***  to display
      a list of instances starting with "U" to select from.

  - the login-name is automatically calculated based on the image-type of the instance
  - override the calculated login-name **-u USERNAME**
  - connect without PEM keys (if properly configured) **-p**
  - command specific help **awss ssh -h**

- List Instances: **awss list**

  - list all instances (default), or use wilcards **awss list D***
  - list running instances **-r** or **--running**
  - list stopped instances **-s** or **--stopped**
  - list instances with specified name **awss list NAME**
  - list instance with specified instance-id **awss list -i ID**
  - instance-state and NAME may be combined in queries.

    - ex: list instances with NAME currently running: **awss list NAME -r**

  - command specific help **awss list -h**

- Start Instance: **awss start NAME** or **awss start -i ID**

  - typing **awss start** without a name or ID will display all stopped instances

    - this allows the user to select from the list if they can't remember the name.
    - this can be combined with wilcards, for example **awss start U\*** to display
      a list of instances starting with "U" to select from.

  - start instance by name or instance-id
  - command specific help **awss start -h**

- Stop Instance: **awss stop NAME** or **awss stop -i ID**

  - typing **awss stop** without a name or ID will display all running instances

    - this allows the user to select from the list if they can't remember the name.
    - this can be combined with wilcards, for example **awss stop U\*** to display
      a list of instances starting with "U" to select from.

  - start instance by name or instance-id
  - command specific help **awss stop -h**



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
   :target: https://pypi.python.org/pypi/awss/
   :alt: Python Versions

.. |PyL| image:: https://img.shields.io/pypi/l/awss.svg
   :target: https://pypi.python.org/pypi/awss/
