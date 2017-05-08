AWS Shortcuts for Command-Line Instance Control
===============================================

List, start, stop and ssh to AWS instances using Name, ID and wildcards
-----------------------------------------------------------------------


|TRAVIS| |AppVeyor| |Codacy Grade| |Codacy Cov| |PyPi release| |lang| |PyL|

--------------

AWS Shortcuts (awss) allows listing, starting, stopping and connecting to instances by name, partial names with wilcards, or instance-id.  The instance information listed includes: all tags & values, name, current-state, instance-id and image-name.

Conecting via SSH on Windows computers is performed by using the command line version of PuTTY, called plink.  On Windows, plink serves as the ssh command, and is run within powershell, so ansi-escape sequences, and colors, are possible.


Overview
--------

**awss** has the following sub-commands: **list**, **start**, **stop**, and **ssh**.

- SSH to an Instance:  **awss ssh NAME**

  - Additional paramters described in `Command Details`_.

- List Instances:  **awss list**

  - Additional paramters described in `Command Details`_.

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
- Windows (see `Windows Prereqs`_ for ssh functionality)

Installation
------------

This utility can be installed with **pip**:

.. code:: shell

  pip install awss

Windows Prereqs
---------------
Because Wiindows does not have a built-in ssh command, using the **awss ssh** command on windows requires:

- Installation of `PuTTY suite <http://www.putty.org/>`_

  - use the "Windows Installer", install all options, and include it on your path

- Converting ssh keys from Amazon's ".pem" format to ".ppk" format

  - keys can be converted using the `puttygen utility <http://stackoverflow.com/questions/3190667/convert-pem-to-ppk-file-format>`_ (installed with PuTTY)

- Powershell must be on the system (installed by default in recent versions of Windows)

Configuration
-------------

**SSH Access Keys** (.pem files)

- Keys should be stored in the **.aws** folder in your home directory

**AWS Credentials** can be stored using *either one of these two methods*:

- Environment variables "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY" and "AWS_DEFAULT_REGION"
- Files named "credentials" and "config" in the **.aws** folder in your home directory

  - The Windows home directory is referred to by the environment variable %UserProfile%

  **{HOME}/.aws/credentials**

  .. code::

    [default]
    aws_access_key_id=AKIAIOSFODNN7EXAMPLE
    aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

  **{HOME}/.aws/config**

  .. code::

    [default]
    region=us-west-2
    output=json

- Information on AWS Credentials is in the `AWS Getting Setup guide. <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html>`_
- Information on configuration files in is the `AWS Getting Started guide. <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>`_

Command Details
---------------

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

.. |lang| image:: https://img.shields.io/badge/language-python-3572A5.svg
   :target: https://github.com/robertpeteuil/aws-shortcuts
