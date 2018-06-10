AWS CLI Shortcuts - Simplified Instance Management
==================================================

Easily List, Control and Connect to Instances directly from the Shell
---------------------------------------------------------------------


|TRAVIS| |AppVeyor| |Codacy Grade| |Codecov Cov| |PyPi release| |lang|

--------------

Identify, control and connect-to instances directly from the command line with AWSS.  It requires no parameters and allows the use of wildcards when specifying instances, making it ideal when minimal instance details are known or multiple instances match known parameters.  In these scenarios, a pick-list is displayed of instances that match the command and parameters specified.

This enables easy identification and selection of desired target instances, and eliminates the need to leave the shell to retrieve information from the Web Portal - preventing workflow disruption and retaining your focus.

AWSS is extremely useful in many scenarios, including:

- Connecting to on-demand instances that frequently change state, and thus IP address as well.
- Connecting to instances where the required login-user is unknown.
- Connecting to instances where the required key associated with the login-user is unknown.
- Connecting to instances where the instance-id is unknown.
- Connecting to instances where 'name' is not set or unique.


Screenshots
-------------------

**"awss ssh" without any parameters - allowing selection from a list of possible 'ssh' targets**

.. image:: https://cloud.githubusercontent.com/assets/1554603/26036941/363b9bf2-389d-11e7-88ab-3ab0e1d52f30.jpg

**"awss list" - presents a list of all instances, details and all tags**

.. image:: https://cloud.githubusercontent.com/assets/1554603/25595372/6c3bd5e2-2e79-11e7-9ebc-4730f93c2cb6.png

**"awss start" with partial Name and wildcard supplied - allowing selection from a list of possible targets**

.. image:: https://cloud.githubusercontent.com/assets/1554603/25595396/84b4ef64-2e79-11e7-922f-d645b007af57.png


Tested Platforms & Python Versions
----------------------------------

Python 2.7, 3.4, 3.5, 3.6

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
Windows does not have a built-in ssh command, so using the **awss ssh** command on windows requires:

- Installation of `PuTTY Suite <http://www.putty.org/>`_

  - use the "Windows Installer", install all options, and include it on your path

- Converting ssh keys from Amazon's ".pem" format to ".ppk" format

  - keys can be converted using the `puttygen utility <http://stackoverflow.com/questions/3190667/convert-pem-to-ppk-file-format>`_ (installed with PuTTY Suite)

- Powershell (native in of Windows since Windows XP Service Pack 3)

Configuration
-------------

**SSH Access Keys** (.pem or .ppk files)

- Keys should be stored in the **.aws** folder in your home directory
- Unix-type systems must set permission on files with a command such as ``sudo chmod 400 ~/.aws/*.pem``
- Windows systems must convert files to ".ppk" format, as described in `Windows Prereqs`_

**AWS Credentials** can be stored using *either one of these two methods*:

- Environment variables "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY" and "AWS_DEFAULT_REGION"
- Files named "credentials" and "config" in the **.aws** folder in your home directory

  - The Windows home directory is referred to by the environment variable %UserProfile%

  **{HOME}/.aws/credentials**

  .. code:: ini

    [default]
    aws_access_key_id=AKIAIOSFODNN7EXAMPLE
    aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

  **{HOME}/.aws/config**

  .. code:: ini

    [default]
    region=us-west-2
    output=json

- Information on AWS Credentials is in the `AWS Getting Setup guide. <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html>`_
- Information on configuration files in is the `AWS Getting Started guide. <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>`_

Command Details
---------------

- SSH to Instance: **awss ssh**, **awss ssh NAME** or **awss ssh -i ID**

  - typing **awss ssh** without a name or ID will display all running instances

    - this allows the user to select from the list if they can't remember the name
    - this can be combined with wilcards, for example **awss ssh U\***  to display
      a list of instances starting with "U" to select from

  - the login-name is automatically calculated based on the image-type of the instance
  - override the calculated login-name **-u USERNAME**
  - connect without PEM keys (if properly configured) **-p**
  - command specific help **awss ssh -h**

- List Instances: **awss list** (other variations listed below)

  - list all instances (default), or use wilcards **awss list D***
  - list running instances **-r** or **--running**
  - list stopped instances **-s** or **--stopped**
  - list instances with specified name **awss list NAME**
  - list instance with specified instance-id **awss list -i ID**
  - instance-state and NAME may be combined in queries

    - ex: list instances with NAME currently running: **awss list NAME -r**

  - command specific help **awss list -h**

- Start Instance: **awss start**, **awss start NAME** or **awss start -i ID**

  - typing **awss start** without a name or ID will display all stopped instances

    - this allows the user to select from the list if they can't remember the name
    - this can be combined with wilcards, for example **awss start U\*** to display
      a list of instances starting with "U" to select from

  - start instance by name or instance-id
  - command specific help **awss start -h**

- Stop Instance: **awss stop**, **awss stop NAME** or **awss stop -i ID**

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

.. |Py ver| image:: https://img.shields.io/pypi/pyversions/awss.svg
   :target: https://pypi.python.org/pypi/awss/

.. |Codacy Grade| image:: https://api.codacy.com/project/badge/Grade/477279a80d31407a99fb3c3551e066cb
   :target: https://www.codacy.com/app/robertpeteuil/aws-shortcuts?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=robertpeteuil/aws-shortcuts&amp;utm_campaign=Badge_Grade

.. |Codacy Cov| image:: https://api.codacy.com/project/badge/Coverage/477279a80d31407a99fb3c3551e066cb
   :target: https://www.codacy.com/app/robertpeteuil/aws-shortcuts?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=robertpeteuil/aws-shortcuts&amp;utm_campaign=Badge_Coverage

.. |Codecov Cov| image:: https://codecov.io/gh/robertpeteuil/aws-shortcuts/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/robertpeteuil/aws-shortcuts

.. |PyL| image:: https://img.shields.io/pypi/l/awss.svg
   :target: https://pypi.python.org/pypi/awss/

.. |lang| image:: https://img.shields.io/badge/language-python-3572A5.svg
   :target: https://github.com/robertpeteuil/aws-shortcuts
