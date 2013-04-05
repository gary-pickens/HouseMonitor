
############
Gary's Notes
############

****************
Beaglebone Notes
****************

Notes on installing HouseMonitor.py on a BeagleBone computer
============================================================

    * Create or stall HouseMonitor
    * Create or install and correct the following file called housemonitor.service::

        [Unit]
        Description=House Monitoring and Control System
        After=syslog.target

        [Service]
        WorkingDirectory=/home/gary/bin/HouseMonitor.final/HouseMonitor
        ExecStart=/usr/bin/python HouseMonitor.py
        Type=simple

        [Install]
        WantedBy=multi-user.target

    * Execute the following command to install the service::
    
        systemctl enable housemonitor.service
    
    * To start HouseMonitor excute the following command::
        
        systemctl start housemonitor.service
        
    * To check the status execute the following command::
    
        systemctl start housemonitor.service
        
    * See for the `sysemctl <http://www.dsm.fordham.edu/cgi-bin/man-cgi.pl?topic=systemctl>`_. man page.
     

Building a new system for HouseMonitor
======================================

#. Download image.
#. Description for `installing <http://circuitco.com/support/index.php?title=BeagleBone#Creating_a_SD_Card>`_. new image. Here is a summary of the web page for initializing your card using windows:

    * Download the SD card image you want to use listed below. These are the images that ship with the boards.
    * Decompress the verification image file using 7-zip.
    * Insert the SD card writer/reader into the Windows machine.
    * Insert 4GB SD card into the reader/writer.
    * Run the HPFormatter tool and format the SD card for FAT or FAT32 in order to remove the second partition from the card.
    * Close the HPFormatter tool when done.
    * Start the Win32DiskImager.
    * Select the decompressed image file and correct SD card location. **MAKE SURE YOU SELECT THE CORRECT LOCATION OF THE SD CARD.**
    * Click on 'Write'.
    * After the image writing is done, eject the SD card.

#. Insert the sd rom in the beaglebone computer.
#. Power up the beagle bone computer.
#. Connect to the beaglebone using TenTen on the serial port or with SSH.
#. Log on as root with no password
#. Create an account using:

    * ``adduser gary``

#. Install sudo with the following commands
    * ``opkg install sudo``
    * ``visudo``
    * Added the following line:
        gary ALL = (ALL) ALL

#. Log on as gary

#.  Update any packages using the following commands.

    * ``sudo opkg install python-setuptools``
    * ``sudo opkg install python-xmlrpc``
    * ``sudo opkg install python-compile``

#. Install pip by using the following command:

    * ``sudo curl -k -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py``
    * ``sudo python get-pip.py``

#. Installing HouseMonitor
    * Download HouseMonitor-3.0.2.zip to the BeagleBone.
    * Make a directory called HouseMonitor in ``~gary/bin``
    * Run the following command as root:
        ``easy_install --install-dir /home/gary/bin/HouseMonitor -Z HouseMonitor-3.0.2.zip``

Baud rate for Tera Term
=======================

115200

****************
Beaglebone Notes
****************

Setting up the Xbee

# Plug xbee into the Xbee Explorer.
# Connect the Xbee Explorer to the computer via USB cable.
# Start X-CTU
# On the modem Configuration tab select **XB24-ZB** in the **Modem XBEE** section
# select **ZIGBEE Router API** under the **Function Set**


*********
Ant Notes
*********

Arrg scp broke again!
=====================

I am hot on a project and it breaks.  Here is what I am trying to do:

::

        <sshexec host="${host}" username="${user}" password="${password}"
            command="rm -fr ~/src/${remote_directory}" />
        <sshexec host="${host}" username="${user}" password="${password}"
            command="mkdir ~/src/${remote_directory}" />
        <scp todir="${user}:${password}@${host}:src/${remote_directory}">
            <fileset file=".">
                <include name="**/*.py" />
                <include name="**/*.conf" />
                <include name="**/*.xml" />
                <exclude name="UnitTest" />
            </fileset>
        </scp>
        <scp todir="${user}:${password}@${host}:src/${remote_directory}">
            <fileset file=".">
                <include name="dist/HouseMonitor-${version}.zip" />
            </fileset>
        </scp>
        <sshexec host="${host}" username="${user}" password="${password}"
            command="chmod  777 ~/src/${remote_directory}/HouseMonitor/HouseMonitor.py" />

Here is the error message:

::

    Buildfile: C:\Users\Gary\git\HouseMonitor\HouseMonitor\build.xml
    copybb:
    
    BUILD FAILED
    C:\Users\Gary\git\HouseMonitor\HouseMonitor\build.xml:64: Problem: failed to create task or type sshexec
    Cause: Could not load a dependent class com/jcraft/jsch/Logger
           It is not enough to have Ant's optional JARs
           you need the JAR files that the optional tasks depend upon.
           Ant's optional task dependencies are listed in the manual.
    Action: Determine what extra JAR files are needed, and place them in one of:
            -C:\Program Files\eclipse Juno\plugins\org.apache.ant_1.8.3.v20120321-1730\lib
            -C:\Users\Gary\.ant\lib
            -a directory added on the command line with the -lib argument
    
    Do not panic, this is a common problem.
    The commonest cause is a missing JAR.
    
    This is not a bug; it is a configuration problem

**Fix**

1. I tried installing jsch as recommended by `a stackoverflow`_.

    .. _a stackoverflow: http://stackoverflow.com/questions/11092216/ant-scp-failure

     **That did not fix the problem.**

2. I have a new clue.  It works from the command line, most be something about the eclipse ant.  I put
jsch.jar in the eclipse directory:::

    \Program Files\eclipse Juno\plugins\org.apache.ant_1.8.3.v20120321-1730\lib

    That **did not fix** the problem also there was already a file called ant-jsch.jar there.

3. Perhaps my local ant directory:::

    \Users\Gary\.ant\lib
    
    Windows will not let me create a directory called .ant

4. Did more searching and I found this at `Eclipse Zone`_.

    .. _Eclipse Zone: http://www.eclipsezone.com/eclipse/forums/t99332.html

so I went to Window>Preferences>Ant>Runtime>Classpath>Select Global Entries and picked jsch.jar,

** Problem Fixed **


************
Python Notes
************

python path used by Eclipse
===========================

::

    C:\Program Files\eclipse Juno\plugins\org.python.pydev_2.7.1.2012100913\pysrc\pydev_sitecustomize;
    C:\Users\Gary\git\HouseMonitor\HouseMonitor\bin;
    C:\Users\Gary\git\HouseMonitor\HouseMonitor\housemonitor;
    C:\Python27\Lib\site-packages\APScheduler-2.0.3-py2.7.egg;
    C:\Users\Gary\Desktop\eclipse Indigo\plugins\org.python.pydev_2.5.0.2012040618\PySrc;
    C:\Python27\lib\site-packages\setuptools-0.6c11-py2.7.egg;
    C:\Python27\lib\site-packages\py-1.4.8-py2.7.egg;
    C:\Python27\lib\site-packages\pip-1.0-py2.7.egg;
    C:\Python27\lib\site-packages\demjson-1.6-py2.7.egg;
    C:\Python27\lib\site-packages\httplib2-0.7.4-py2.7.egg;
    C:\Python27;C:\OpenSSL-Win64\bin;
    C:\Python27\Scripts;
    C:\Python27\DLLs;
    C:\Python27\lib;
    C:\Python27\lib\plat-win;
    C:\Python27\lib\lib-tk;
    C:\Python27\lib\site-packages;
    C:\Python27\Lib\site-packages\pypubsub-3.1.2-py2.7.egg

.. note::

    Of course this is all concatenated into one line.

GIT Notes
*********

Reference
=========

1. `Pro GIT <http://git-scm.com/>`_.
2. `git man pages <http://www.kernel.org/pub/software/scm/git/docs/>`_.
3. `git concepts <http://www.kernel.org/pub/software/scm/git/docs/user-manual.html#git-concepts>`_.
4. `git user manual <http://www.kernel.org/pub/software/scm/git/docs/user-manual.html>`_.

Restoring Files
===============

1.  I used the following command to restore the file named common.py on NT:

::

        git checkout  8c853e3eb54ee5d5d357f052c8cfd0cbe3e0f07a^ -- HouseMonitor\housemonitor\lib\common.py
    
2.  Here is a suggestion from stackoverflow.com .. _a link: http://stackoverflow.com/questions/953481/restore-a-deleted-file-in-a-git-repo:

::

        git checkout $(git rev-list -n 1 HEAD -- "$file")^ -- "$file"


Info about files
================

1. `git rev-list <http://www.kernel.org/pub/software/scm/git/docs/git-rev-list.html>`_. Lists commit objects in reverse chronological order.::

    git rev-list  HEAD -- HouseMonitor/housemonitor/steps/test/onBooleanChange_UnitTest.py
    
Will show the modifications to onBooleanChange_UnitTest.py::

    c4ea95ef914992b603524eb9e58272211ce01928
    bea2d25f73b1262050148d195d2131882fbe6bb3


2. `git show <http://www.kernel.org/pub/software/scm/git/docs/git-show.html>`_. Show various types of objects.::

    git show 
    
Will show the actual modification the were made to the file.::

        commit c4ea95ef914992b603524eb9e58272211ce01928
        Author: gary-pickens <gary_pickens@yahoo.com>
        Date:   Fri Dec 14 23:00:41 2012 -0600
        
            Changed the names on a lot of files to all lower case, in an attempt to
            get nosetests working.
        
        diff --git a/HouseMonitor/housemonitor/steps/test/onBooleanChange_UnitTest.py b/HouseMonitor/housemonitor/steps/test/onBooleanChange_UnitTest.py
        deleted file mode 100644
        index 003cc14..0000000
        --- a/HouseMonitor/housemonitor/steps/test/onBooleanChange_UnitTest.py
        +++ /dev/null
        @@ -1,122 +0,0 @@
        -'''
        -Created on Nov 15, 2012
        -
        -@author: Gary
        -'''
        -import unittest
 
...


3. `git log  <http://www.kernel.org/pub/software/scm/git/docs/git-log.html>`_. Show commit logs.::

        git log -- HouseMonitor/housemonitor/steps/test/onBooleanChange_UnitTest.py
    
    Will show the log commits that were made for this file.::
    
        commit c4ea95ef914992b603524eb9e58272211ce01928
        Author: gary-pickens <gary_pickens@yahoo.com>
        Date:   Fri Dec 14 23:00:41 2012 -0600
        
            Changed the names on a lot of files to all lower case, in an attempt to
            get nosetests working.
        
        commit bea2d25f73b1262050148d195d2131882fbe6bb3
        Author: gary-pickens <gary_pickens@yahoo.com>
        Date:   Fri Nov 23 11:51:34 2012 -0600
        
            More moving
    

Listing files
=============

#. Listing all files in repository::
    
    git ls-files

#. Listing all deleted files::

    git ls-files -d
    
#.  Listing all modified files:

::

    git ls-files -m


*************************
Sphinx & reStructuredText
*************************

Web links
=========

#. `Spinx Python Documentation Generator <http://sphinx-doc.org/>`_.

#. `Spinx Tutorial <http://matplotlib.org/sampledoc/>`_.

#. `reStructuredText Primer <http://sphinx-doc.org/rest.html>`_.

Inline markup
=============
#. **one asterisk**: ``*text*`` for emphasis (italics),
#. **two asterisks**: ``**text**`` for strong emphasis (boldface), and
#. **backquotes**: ````text```` for code samples.

External Links
==============

::

    a `Sphinx <http://sphinx-doc.org/rest.html>`_. link

A `Sphinx <http://sphinx-doc.org/rest.html>`_. link

Or seperating the text and the link:

::

    A `Sphinx`_. link
     
    .. _a link: http://sphinx-doc.org/rest.html
     
A `Sphinx`_. link

.. _Sphinx: http://sphinx-doc.org/rest.html


Definition Lists
================

::

    Term
        Term definition.
        
    Next Term
        Next definition.


Term
    Term definition.

Next Term
    Next definition.

AutoNumbered list
=================

::

    #. hash tag
    #. hash tag

#. hash tag
#. hash tag


Numbered list
=============

::

    1. Numbered list
    2. Numbered list

1. Numbered list
2. Numbered list

Bulleted list
=============

::

    * Bulleted list
    * Bulleted list

* Bulleted list
* Bulleted list

Nested lists
============

::

   * this is
   * a list

     * with a nested list
     * and some subitems

   * and here the parent list continues

* this is
* a list

 * with a nested list
 * and some subitems

* and here the parent list continues

Line blocks
===========

::

    | These lines are
    | broken exactly like in
    | the source file.

| These lines are
| broken exactly like in
| the source file.

Sections
========

::

    # with overline, for parts
    * with overline, for chapters
    =, for sections
    -, for subsections
    ^, for subsubsections
    ", for paragraphs
    
Defining funcitons
==================

::

* ``param``: Description of a parameter.
* ``type``: Type of a parameter.
* ``raises``, ``raise``, ``except``, ``exception``: That (and when) a specific exception is raised.
* ``var``, ``ivar``, ``cvar``: Description of a variable.
* ``returns``, ``return``: Description of the return value.
* ``rtype``: Return type.

Example::

 .. py:function:: format(etype, value)

        :param value: the current value
        :type value: int, float, str
        :param data: the data that is pasted between steps
        :type dict:
        :returns: dict containing the above items
        :raises: KeyError


******************
Creating Packaging
******************

Web links
=========

#.  `Welcome to The Hitchhiker’s Guide to Packaging <http://guide.python-distribute.org/index.html>`_.

#.  ` < >`_.

*******
DocTest
*******

Web links
=========

#. `DocTest Test interactive Python examples <http://docs.python.org/2/library/doctest.html>`_.

How to make it work
===================

#. Add the following code at end of file:::

if __name__ == "__main__":
    import doctest
    doctest.testmod()

#. Type the following to run the code:::

python example.py

where: examble.py is the name of the module to test.

add **-v** for more output.  For example:::

python example.py -v

****
Misc
****
#. Look into Stevedore.  Here are a few URL's:
    #. `SteveDore on GITHUB <https://github.com/dreamhost/stevedore>`_.
    #. `SteveDore on PyPi <http://pypi.python.org/pypi/stevedore>`_.
    #. `Doug HellMann's Blog on Stevedore 3.0 <http://blog.doughellmann.com/2012/08/stevedore-03.html>`_.

#. `Good web page for calculating LM555 values given frequency <http://houseofjeff.com/555-timer-oscillator-frequency-calculator/>`_.

#. `Common Mistakes When Using a 555 Timer <http://www.555-timer-circuits.com/common-mistakes.html>`_.
