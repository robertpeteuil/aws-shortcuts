"""Control and connect to AWS EC2 instances from command line.

The AWS Shortcuts (awss) library is a CLI utility allowing listing,
starting, stopping and connecting to AWS EC2 instances by Name or ID.

License:

    AWSS - Control and connect to AWS EC2 instances from command line
    Copyright (C) 2017  Robert Peteuil

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

URL:       https://github.com/robertpeteuil/aws-shortcuts
Author:    Robert Peteuil

Modules:

core    : Main module providing entry point and core code.
awsc    : Communicate with AWS EC2 to get data and interact with instances.
colors  : Determine color capability, define color vars and theme.
debg    : Debug print functions that execute if debug mode initialized.

-----------------------------------------------------------------------------
OVERVIEW:

    awss has only two top level arguments:

        -h, --help            show help message and exit
        -v, --version         show program's version number and exit

Sub-Command Usage:

    awss is used with a sub-command after: list, start, stop or ssh.

    usage:
        awss list  [ OPTIONS ]
        awss start [ OPTIONS ]
        awss stop  [ OPTIONS ]
        awss ssh   [ OPTIONS ]

-----------------------------------------------------------------------------

List Sub-Command:

    usage:
        awss list [none] [NAME] [-i ID] [-r] [-s] [OPTIONS]

    List AWS instances from the command line. Instances can be specified
    with combinations of NAME, instance-id, running-state, or left blank
    to list all instances.

    ex: 'awss list TEST -r' : will list instances named 'TEST' that are
                              currently running

    Args:
      [none]                list all instances
      NAME                  specify instance by name
      -i ID, --id ID        specify instance by id
      -r, --running         list running instances
      -s, --stopped         list stopped instances
      -h, --help            show help message and exit

-----------------------------------------------------------------------------

Start Sub-Command:

    usage:
        awss start [NAME] [-i ID] [-h]

    Start an AWS instance from the command line. If neither NAME nor
    instance-id is specified, all stopped instances are listed, and
    the user selects the instance to start.

    Args:
      NAME                  specify instance by name
      -i ID, --id ID        specify instance-id
      -h, --help            show help message and exit

-----------------------------------------------------------------------------

Stop Sub-Command:

    usage:
        awss stop [NAME] [-i ID] [-h]

    Stop an AWS instance from the command line. If neither NAME nor
    instance-id is specified, all running instances are listed, and
    the user selects the instance to stop.

    Args:
      NAME                  specify instance by name
      -i ID, --id ID        specify instance-id
      -h, --help            show help message and exit

-----------------------------------------------------------------------------

SSH Sub-Command:

    usage:
        awss ssh ( [NAME] [-i ID] ) [-u USER] [-p] [-h]

    Connect to an AWS instance via ssh. If neither NAME nor
    instance-id is specified, all running instances are listed, and
    the user selects the instance to connect to.

    Args:
      NAME                  specify instance by name
      -i ID, --id ID        specify instance-id
      -u USER, --user USER  override default username for ssh
      -p, --nopem           connect without PEM key
      -h, --help            show this help message and exit

-----------------------------------------------------------------------------
"""
