Dotmagic
========

Dotmagic is a config file provisioner for unix systems.

Usage
=====

Synopsis
--------

    $ dotmagic <action> [options]

Actions
-------

* ``init``

    Initialize the state of the application by creating the ~/.dotmagic folder
    Asks you a few questions to get started.
    Questions include username and rctypes whitelist.

* ``config``

* ``fetch <username>``

    ``<username>`` is optional. Uses the current username unless specified.
    Downloads all snapshots into the repo.

* ``checkout <username> <version>``

    Does a cleanup, followed by a copy and paste of the current version in the repo.

* ``backup``

    Saves a snapshot in the ``~/.dotmagic/repo/<username>/`` directory

* ``push``

    Uploads all snapshots to the server.

* ``pull``

    Combination of fetch and checkout.

* ``try <username> <appname> <cmd>``

    Backup configuration for the program to ``~/.dotmagic/tmp/``
    and starts the application.

* ``cleanup``

    Removes all available config files based on preferences.

*  ``add <appname>``
    
    Track the config files for that app.

*  ``remove <appname>`` -r

    Untracks the config files for that app.

    -r removes the files as well.

*  ``update-rctypes``
    
    Updates supported rctypes by syncing with the server.

*   ``help``

    Displays the help.


Architecture
============

Static Layout
-------------

* ``rctypes``

    Contains the available configuration types

* ``~/.dotmagic/dotmagic.yaml``

* ``~/.dotmagic/tmp/<appname>/``

* ``~/.dotmagic/repo/<username>/``



