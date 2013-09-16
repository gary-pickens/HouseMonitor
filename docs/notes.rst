
############
Gary's Notes
############


=================
Related web pages
=================

#. `House Monitor <http://beaglebone/index.html>`_.

#. `Modules <http://beaglebone/_modules>`_.

#. `Coverage Results <http://beaglebone/cover>`_.

#. `COSM <https://cosm.com/users/gary_pickens>`_.

#. `HouseMonitor <http://beaglebone/HouseMonitor/index.html>`_.


================
Beaglebone Notes
================

Notes from July 27, 2013 failure.
=================================

On the evening of July 26th at about midnight, we had a bad thurndorstorm storm pass through the Austin.  The next 
morning I found the main coumputer and beaglebone computers down.  The windows machine booted okay and I was able
to log into the beaglebone computer okay using the serial line.  But when I tried to log on using SSH I was not 
able to connect to the beaglebone.  

I tried all sorts of things trying to figure out the problem.  Sometimes I was able to get it to work for server hours 
but it would evenually fail again.  The main symtom was the networking would stop working.  Here is some of the things 
I learned along the way.

How to read system log.
-----------------------

The following is a good explaination of how to read the system log:
`Explorations into Angstrom syslog and systemd <http://www.mattlmassey.com/2012/07/10/explorations-into-angstrom-syslog-and-systemd>`_.
 
#. Basicly to read the system log use the following command::

   jouralctl
   
#. It accepts the following options::

      journalctl [OPTIONS...] [MATCH]
      
      Send control commands to or query the journal.
      
        -h --help              Show this help
           --version           Show package version
           --no-pager          Do not pipe output into a pager
        -a --all               Show all fields, including long and unprintable
        -f --follow            Follow journal
        -n --lines=INTEGER     Journal entries to show
           --no-tail           Show all lines, even in follow mode
        -o --output=STRING     Change journal output mode (short, short-monotonic,
                               verbose, export, json, cat)
        -q --quiet             Don't show privilege warning
        -l --local             Only local entries
        -b --this-boot         Show data only from current boot
        -D --directory=PATH    Show journal files from directory
        -p --priority=RANGE    Show only messages within the specified priority range
      
      Commands:
           --new-id128         Generate a new 128 Bit ID
           --header            Show journal header information
           --setup-keys        Generate new FSS key pair
             --interval=TIME   Time interval for changing the FSS sealing key
           --verify            Verify journal file consistency
             --verify-key=KEY  Specify FSS verification key
       
#. I have been using the following command::

   journalctl -f -n 200 -b

#. Since I am on the serial line the window does not resize nicely to I have to do it manually. I use the following commands::

   stty cols 250 rows 79

#. The journal is located at /run/log/journal.

#. The is volatile memory and will be lost with each reboot.  To move it to non-volatile memory simply create a directory called /var/log/journal.

#. More `notes on journaling <http://0pointer.de/blog/projects/journalctl.html>`_ and `here <https://wiki.archlinux.org/index.php/Systemd#Journal>`_.

#. Here is the error message::

      Jul 28 17:48:48 beaglebone systemd[1]: Reloading.
      Jul 28 17:49:28 beaglebone systemd[1]: Reloading.
      Jul 28 17:50:34 beaglebone systemd[1]: Reloading.
      Jul 28 17:52:33 beaglebone systemd[1]: Reloading.
      Jul 28 17:59:58 beaglebone dropbear[905]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 17:59:58 beaglebone dropbear[905]: Child connection from ::ffff:192.168.1.66:18608
      Jul 28 17:59:59 beaglebone dropbear[905]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18608
      Jul 28 18:00:47 beaglebone dropbear[905]: Exit (root): Exited normally
      Jul 28 18:00:47 beaglebone dropbear[907]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:00:47 beaglebone dropbear[907]: Child connection from ::ffff:192.168.1.66:18609
      Jul 28 18:00:48 beaglebone dropbear[907]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18609
      Jul 28 18:00:48 beaglebone dropbear[907]: Exit (root): Exited normally
      Jul 28 18:02:19 beaglebone dropbear[915]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:02:19 beaglebone dropbear[915]: Child connection from ::ffff:192.168.1.66:18615
      Jul 28 18:02:19 beaglebone dropbear[915]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18615
      Jul 28 18:02:54 beaglebone dropbear[915]: Exit (root): Exited normally
      Jul 28 18:02:54 beaglebone dropbear[917]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:02:54 beaglebone dropbear[917]: Child connection from ::ffff:192.168.1.66:18619
      Jul 28 18:02:54 beaglebone dropbear[917]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18619
      Jul 28 18:02:57 beaglebone dropbear[917]: Exit (root): Exited normally
      Jul 28 18:07:06 beaglebone dropbear[921]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:07:06 beaglebone dropbear[921]: Child connection from ::ffff:192.168.1.66:18741
      Jul 28 18:07:07 beaglebone dropbear[921]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18741
      Jul 28 18:07:45 beaglebone dropbear[921]: Exit (root): Exited normally
      Jul 28 18:07:45 beaglebone dropbear[923]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:07:45 beaglebone dropbear[923]: Child connection from ::ffff:192.168.1.66:18743
      Jul 28 18:07:45 beaglebone dropbear[923]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18743
      Jul 28 18:07:48 beaglebone dropbear[923]: Exit (root): Exited normally
      Jul 28 18:10:42 beaglebone dropbear[927]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:10:42 beaglebone dropbear[927]: Child connection from ::ffff:192.168.1.66:18760
      Jul 28 18:10:43 beaglebone dropbear[927]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18760
      Jul 28 18:11:23 beaglebone dropbear[927]: Exit (root): Exited normally
      Jul 28 18:11:23 beaglebone dropbear[929]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:11:23 beaglebone dropbear[929]: Child connection from ::ffff:192.168.1.66:18769
      Jul 28 18:11:24 beaglebone dropbear[929]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18769
      Jul 28 18:11:29 beaglebone dropbear[929]: Exit (root): Exited normally
      Jul 28 18:12:45 beaglebone dropbear[933]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:12:45 beaglebone dropbear[933]: Child connection from ::ffff:192.168.1.66:18774
      Jul 28 18:12:46 beaglebone dropbear[933]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18774
      Jul 28 18:13:22 beaglebone dropbear[933]: Exit (root): Exited normally
      Jul 28 18:13:22 beaglebone dropbear[935]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:13:22 beaglebone dropbear[935]: Child connection from ::ffff:192.168.1.66:18778
      Jul 28 18:13:22 beaglebone dropbear[935]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18778
      Jul 28 18:13:24 beaglebone dropbear[935]: Exit (root): Exited normally
      Jul 28 18:18:28 beaglebone dropbear[939]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:18:28 beaglebone dropbear[939]: Child connection from ::ffff:192.168.1.66:18897
      Jul 28 18:18:28 beaglebone dropbear[939]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18897
      Jul 28 18:19:03 beaglebone dropbear[939]: Exit (root): Exited normally
      Jul 28 18:19:03 beaglebone dropbear[941]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:19:03 beaglebone dropbear[941]: Child connection from ::ffff:192.168.1.66:18899
      Jul 28 18:19:03 beaglebone dropbear[941]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18899
      Jul 28 18:19:06 beaglebone dropbear[941]: Exit (root): Exited normally
      Jul 28 18:22:28 beaglebone dropbear[945]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:22:28 beaglebone dropbear[945]: Child connection from ::ffff:192.168.1.66:18917
      Jul 28 18:22:29 beaglebone dropbear[945]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18917
      Jul 28 18:23:04 beaglebone dropbear[945]: Exit (root): Exited normally
      Jul 28 18:23:04 beaglebone dropbear[948]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:23:04 beaglebone dropbear[948]: Child connection from ::ffff:192.168.1.66:18921
      Jul 28 18:23:04 beaglebone dropbear[948]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:18921
      Jul 28 18:23:07 beaglebone dropbear[948]: Exit (root): Exited normally
      Jul 28 18:28:51 beaglebone dropbear[951]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:28:51 beaglebone dropbear[951]: Child connection from ::ffff:192.168.1.66:19047
      Jul 28 18:28:52 beaglebone dropbear[951]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:19047
      Jul 28 18:29:29 beaglebone dropbear[951]: Exit (root): Exited normally
      Jul 28 18:29:29 beaglebone dropbear[953]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:29:29 beaglebone dropbear[953]: Child connection from ::ffff:192.168.1.66:19050
      Jul 28 18:29:29 beaglebone dropbear[953]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:19050
      Jul 28 18:29:31 beaglebone dropbear[953]: Exit (root): Exited normally
      Jul 28 18:30:01 beaglebone /usr/sbin/crond[957]: pam_unix(crond:session): session opened for user root by (uid=0)
      Jul 28 18:30:01 beaglebone /USR/SBIN/CROND[958]: (root) CMD (/usr/bin/ntpdate -b -s -u pool.ntp.org)
      Jul 28 18:30:10 beaglebone ntpdate[958]: step time server 198.101.234.139 offset 0.025639 sec
      Jul 28 18:30:10 beaglebone /USR/SBIN/CROND[957]: pam_unix(crond:session): session closed for user root
      Jul 28 18:33:27 beaglebone dropbear[959]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:33:27 beaglebone dropbear[959]: Child connection from ::ffff:192.168.1.66:19066
      Jul 28 18:33:28 beaglebone dropbear[959]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:19066
      Jul 28 18:34:02 beaglebone dropbear[959]: Exit (root): Exited normally
      Jul 28 18:34:02 beaglebone dropbear[961]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:34:02 beaglebone dropbear[961]: Child connection from ::ffff:192.168.1.66:19070
      Jul 28 18:34:02 beaglebone dropbear[961]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:19070
      Jul 28 18:34:05 beaglebone dropbear[961]: Exit (root): Exited normally
      Jul 28 18:35:43 beaglebone dropbear[965]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:35:43 beaglebone dropbear[965]: Child connection from ::ffff:192.168.1.66:19183
      Jul 28 18:35:44 beaglebone dropbear[965]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:19183
      Jul 28 18:36:23 beaglebone dropbear[965]: Exit (root): Exited normally
      Jul 28 18:36:23 beaglebone dropbear[968]: Failed reading '/etc/dropbear/dropbear_dss_host_key', disabling DSS
      Jul 28 18:36:23 beaglebone dropbear[968]: Child connection from ::ffff:192.168.1.66:19193
      Jul 28 18:36:23 beaglebone dropbear[968]: PAM password auth succeeded for 'root' from ::ffff:192.168.1.66:19193
      Jul 28 18:36:26 beaglebone dropbear[968]: Exit (root): Exited normally
      Jul 28 18:36:36 beaglebone connmand[90]: connmand[90]: eth0 {RX} 92855 packets 56653779 bytes
      Jul 28 18:36:36 beaglebone connmand[90]: connmand[90]: eth0 {TX} 47477 packets 10409327 bytes
      Jul 28 18:36:36 beaglebone connmand[90]: connmand[90]: eth0 {update} flags 4099 <UP>
      Jul 28 18:36:36 beaglebone connmand[90]: eth0 {RX} 92855 packets 56653779 bytes
      Jul 28 18:36:36 beaglebone connmand[90]: eth0 {TX} 47477 packets 10409327 bytes
      Jul 28 18:36:36 beaglebone connmand[90]: eth0 {update} flags 4099 <UP>
      Jul 28 18:36:39 beaglebone avahi-daemon[91]: Withdrawing address record for 192.168.1.73 on eth0.
      Jul 28 18:36:39 beaglebone avahi-daemon[91]: Leaving mDNS multicast group on interface eth0.IPv4 with address 192.168.1.73.
      Jul 28 18:36:39 beaglebone avahi-daemon[91]: Interface eth0.IPv4 no longer relevant for mDNS.
      Jul 28 18:36:39 beaglebone connmand[90]: connman_inet_clear_ipv6_address: Invalid argument
      Jul 28 18:36:39 beaglebone connmand[90]: eth0 {newlink} index 2 address 50:56:63:C8:6C:19 mtu 1500
      Jul 28 18:36:39 beaglebone connmand[90]: eth0 {newlink} index 2 operstate 2 <DOWN>
      Jul 28 18:36:39 beaglebone connmand[90]: Disabling DNS server 192.168.1.254
      Jul 28 18:36:39 beaglebone connmand[90]: Removing DNS server 192.168.1.254
      Jul 28 18:36:39 beaglebone connmand[90]: Deleting host route failed (No such process)
      Jul 28 18:36:39 beaglebone connmand[90]: Removing default gateway route failed (No such process)
      Jul 28 18:36:39 beaglebone connmand[90]: connman_inet_clear_address: Invalid argument
      Jul 28 18:36:39 beaglebone connmand[90]: connman_inet_clear_ipv6_address: Invalid argument
      Jul 28 18:36:39 beaglebone avahi-daemon[91]: Withdrawing address record for fe80::5256:63ff:fec8:6c19 on eth0.
      Jul 28 18:36:39 beaglebone connmand[90]: eth0 {del} address 192.168.1.73/24 label eth0
      Jul 28 18:36:39 beaglebone connmand[90]: eth0 {del} route 192.168.1.0 gw 0.0.0.0 scope 253 <LINK>
      Jul 28 18:36:39 beaglebone connmand[90]: eth0 {del} route fe80:: gw :: scope 0 <UNIVERSE>
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: connman_inet_clear_ipv6_address: Invalid argument
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: eth0 {newlink} index 2 address 50:56:63:C8:6C:19 mtu 1500
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: eth0 {newlink} index 2 operstate 2 <DOWN>
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: Disabling DNS server 192.168.1.254
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: Removing DNS server 192.168.1.254
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: Deleting host route failed (No such process)
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: Removing default gateway route failed (No such process)
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: connman_inet_clear_address: Invalid argument
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: connman_inet_clear_ipv6_address: Invalid argument
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: eth0 {del} address 192.168.1.73/24 label eth0
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: eth0 {del} route 192.168.1.0 gw 0.0.0.0 scope 253 <LINK>
      Jul 28 18:36:39 beaglebone connmand[90]: connmand[90]: eth0 {del} route fe80:: gw :: scope 0 <UNIVERSE>

#. It appears the first error was reading from dropbear_dss_host_key.

   * it appears to be a binary file that was last modified on Nov 22 2012.

#. The next error is when avahi-daemon withdraws address record fe80::5256:63ff:fec8:6c19 on eth0.

#. The next significate error is when connmand deletes address 192.168.1.73 on eth0.

#. To enable debug on journaling, add a -d to the line that starts with ExecStrart in file /lib/systemd/system/connman.service.  The new file should look as follows::

   [Unit]
   Description=Connection service
   After=syslog.target
   [Service]
   Type=dbus
   BusName=net.connman
   ExecStart=/usr/sbin/connmand -n -d
   [Install]
   WantedBy=multi-user.target


Notes on installing HouseMonitor.py on a BeagleBone computer
============================================================

* Create or stall HouseMonitor
* Create or install and correct the following file called housemonitor.service in
/lib/systemd/system::

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

      systemctl status housemonitor.service
  
* See for the `sysemctl <http://www.dsm.fordham.edu/cgi-bin/man-cgi.pl?topic=systemctl>`_. man page.
     

Building a new system for HouseMonitor
======================================

**See next section about experinces installing new system in May.**

Windows
-------

#. `Download image <http://downloads.angstrom-distribution.org/demo/beaglebone/>`_.
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

Linux
-----
   * `This page describles writing the SD memory code with Linux. <http://downloads.angstrom-distribution.org/demo/beaglebone/>`_.

for gz file::
 
  $ sudo -s
   (type in your password)
  # zcat Angstrom-Cloud9-IDE-eglibc-ipk-v2011.10-core-beaglebone-r0.img.gz > /dev/sdX
  # exit

Or for the img.xz::


  $ sudo -s
   (type in your password)
  # xz -dkc Angstrom-Cloud9-IDE-eglibc-ipk-v2011.10-core-beaglebone-r0.img.xz > /dev/sdX
  # exit

   the correct /dev/sdX device can be determined by putting the device in the Linux machine 
   and issuing a df command.  Mine was /dev/sdb. fdisk my help also.

#. Insert the sd rom in the beaglebone computer.
#. Power up the beagle bone computer.
#. Connect to the beaglebone using TenTen on the serial port or with SSH.
#. Log on as root with no password

#. Update and Upgrade the packages.

   * ``opkg --tmp-dir ~ update``
   * ``opkg --tmp-dir ~ upgrade``
   
#. Create an account using:

   * ``adduser gary``

#. Install sudo with the following commands.

   * ``opkg install sudo``
   * ``visudo``
   * Added the following line::
   
     gary ALL = (ALL) ALL

#. Log on as gary

#.  Update any packages using the following commands.

   * ``sudo opkg install python-setuptools``
   * ``sudo opkg install python-xmlrpc``
   * ``sudo opkg install python-compile``

#. Install pip by using the following command:

   * ``sudo curl -k -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py``
   * ``sudo python get-pip.py``

#. Use the following command to change the host name::
   
   hostnamectl set-hostname HouseMonitor


#. Installing HouseMonitor
   * Download HouseMonitor-3.0.2.zip to the BeagleBone.
   * Make a directory called HouseMonitor in ``~gary/bin``
   * Run the following command as root::
    
      easy_install --install-dir /home/gary/bin/HouseMonitor -Z HouseMonitor-3.0.2.zip
        
#. After trying the web server cloud9 for some time I decided it was not for me so I decided to 
remove it and install lightthp.

   * Remove cloud9 with the following command::

         opkg remove - -force-removal-of-dependent-packages cloud9


   * It gave some warnings that not all had been removed so I tried::
      
         opkg remove  bonescript

   * Finally I installed lighttpd with the following command:: 
         
         opkg install lightpd

   * I then went to multi-user.target.wants found the following files::

         cloud9.service
         bone101.service
         lighttpd.service
         
   * So I disabled and enabled the ones I want with the following command::
   
         systemctl disable cloud9.service
         systemctl disable bone101.service

   * Chect the status of lighttpd.service the the following command::

         systemctl status lighttpd.service

   *  Then I reboot::
   
         reboot

   * Once it comes up I do the following commands and it seems to be operating the was I want::
   
        cd /etc/systemd/system/multi-user.target.wants/
        systemctl status lighttpd.service
        systemctl status cloud9.service
        systemctl status bone101.service
        netstat -r

   * Now the question is, can I remove cloud9.service and bone101.service files from the system?
     It appears to be working just fine.  I uploaded numerous html files to /www/pages and subdirectories 
     and I can brows to them with no problem.  **Perhaps I should leave well enough alone.**   
   
Note found several months later: `A blog that discusses removing cloud 9, etc and installing lighttpd <http://blog.ippe.biz/2013/03/lighttpd-and-php-on-beaglebone.html>`_.
   
Setting up ssh
==============

Linux
-----

#. Figure out a pass phrase.

#. Change to the .ssh directory.  Create one if it is not in your home directory.

#. On the Linux development machine generate a key with the following command::

      ssh-keygen -b 2048 -f lbeaglebone
   
#. Log on to the beaglebone computer and append the public file (the lbeaglebone.pub) to the file
named 'authorized_keys'

Windows with Eclipse
--------------------

#. Go to Window > Preferences the open Open General > Network Connections > SSH2

#. Then open the tab called 'Key Management'

#. Press the Generate RSA Key...

#. Fill out the Passphrase and the confirm passphrase.

#. Press Save Private Key to save the public and private key.  You will have to specify a name for  the key.

#. Exit eclipse

#. Copy to public key to the beaglebone computer.

#. Append the public key file to 'authorized_keys' in .ssh.  The following command will do the job::

      cat finename.pub >> authorized_keys


Building a new system for HouseMonitor **May 21st update**
==========================================================

Yesterday I noticed that the system was not working so I did some investigating.  After several hours 
I decided to install a new SD rom with the latest software.  This is my journey:

# I tried to use the image I got earlier this year and it kept giving me trouble.  Mainly, I could not load the
top three things from the list above. After much work I thought I would try the latest package, I was hoping
the missing packages would be on the new release.  I was wrong but I could install:
    
    * ``python-setuptools``
    * ``python-xmlrpc``
    * ``python-compile``

The only thing I could not install was:

   * ``sudo``

This means I will have to do everything as root.  Not the way I like to work, and exstive modifications to my ant script/

# Getting jsch working again.  When I tried to upload my files to the beaglebone jsch would not work.  I required
numerous attempts to get it working.

   * I had updated my java version while working trying to recover from the virus. As a result jsch stopped working.  After searching on the Internet I found that other people were having the same problem and there was a new version of jsch. So I downloaded and installed it.
   
   * So I tried again and this time it complained that I was not known on the remote system.  So I copied my pub file to my account on the beaglebone computer.
   
   * The next attempt it complained about was the computer identity had changed.  So I deleted the beaglebone line from known_hose in the .ssh directory.  
   
   * I was still having problems and studing on the Internet, I read adding 'trust="true"' to the scp and sshexec lines would fix the problem.
   
   * Finally, I can copy files to the beaglebone!  I need to go back and study what the above changes mean.  

Baud rate for Tera Term
=======================

To talk to the Beagle Bone over the USB serial link set the baud rate to **115200**.

================================
Setting up the XBees as a router
================================

#. Plug xbee into the Xbee Explorer.
#. Connect the Xbee Explorer to the computer via USB cable.
#. The power led (PWR) should come on.
#. Start X-CTU.
#. Press the Test/Query button on the X-CTU GUI. You should get a dialog box that comes up simular to this:

   .. image:: ComTestQueryModem.png

#. Select the Modem Configuration Tab. It should look as follows:

   .. image:: X-CTUwithModemConfig.png
 
#. Press the *Read* button in the *Modem Parameters*.
#. Press the Download new versions.  This will check if there is new version of the software available.
#. On the modem Configuration tab select **XB24-ZB** in the **Modem XBEE** section
#. Select **ZIGBEE Router API** under the **Function Set** 
#. Press the *Write* button in the *Modem Parameters* section.
#. When X-CTU has finish writing to the XBee close the X-CTU program down.
#. In Eclipse ant window double click Build Backroom XBee.

===================================
Setting up the XBees as an endpoint
===================================

#. Plug xbee into the Xbee Explorer.
#. Connect the Xbee Explorer to the computer via USB cable.
#. The power led (PWR) should come on.
#. Start X-CTU.
#. Press the Test/Query button on the X-CTU GUI. You should get a dialog box that comes up simular to this:

   .. image:: OutsideModem.phg

#. Select the Modem Configuration Tab. It should look as follows:

   .. image:: ZIGBEE end device at.png
 
#. Press the *Read* button in the *Modem Parameters*.
#. Press the Download new versions.  This will check if there is new version of the software available.
#. On the modem Configuration tab select **XB24-ZB** in the **Modem XBEE** section
#. Select **ZIGBEE End Device AT** under the **Function Set** 
#. Press the *Write* button in the *Modem Parameters* section.
#. When X-CTU has finish writing to the XBee close the X-CTU program down.
#. In Eclipse ant window double click Build Backroom XBee.

=========
Ant Notes
=========

Reading base directory
======================

To read the base directory use:

::
   <property name="base" value="${basedir}" />

I tried and tried the following:

::
   <property name="base" value="directory::get-current-directory()" />
    

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
     
** Arggg It's broke again **

1. I installed the latest version of juno and the problems is back.  So I found my old version
of com.jcraft.jsch_0.1.46.v201205102330.jar in the previous install and added that to my Global
section of the Ant properties.  That seemed to fix the problem.
   
   
   

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


============
Python Notes
============

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

=========
GIT Notes
=========

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


=========================
Sphinx & reStructuredText
=========================

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

See the `Reference Manual <http://sphinx-doc.org/domains.html>`_. for more information.

==================
Creating Packaging
==================

Web links
=========

#.  `Welcome to The Hitchhiker’s Guide to Packaging <http://guide.python-distribute.org/index.html>`_.

#.  ` < >`_.

=======
DocTest
=======

Web links
=========

#. `DocTest Test interactive Python examples <http://docs.python.org/2/library/doctest.html>`_.

How to make DocTest work
========================

#. Add the following code at end of file::

      if __name__ == "__main__":
          import doctest
          doctest.testmod()

#. Type the following to run the code:::

      python example.py

where: examble.py is the name of the module to test.

add **-v** for more output.  For example:::

   python example.py -v


==================
A Good COSM Report
==================

::

       {
           "status": "frozen",
           "datastreams": 
             [
               {
                   "tags": "Door",
                   "max_value": "1",
                   "min_value": "0",
                   "units": {
                       "label": "closed"
                   },
                   "at": "2013-05-10T13:43:10.460207",
                   "datapoints": [
                       {
                           "at": "2013-05-10T13:33:52.229189",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:34:21.615878",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:34:50.993990",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:35:20.370394",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:35:49.753481",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:36:19.134127",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:36:48.516787",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:37:17.894411",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:37:47.276919",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:38:16.679934",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:38:46.051974",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:39:15.415072",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:39:44.796084",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:40:14.177309",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:40:43.557040",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:41:12.936861",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:41:42.322634",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:42:11.698000",
                           "value": "1"
                       },
                       {
                           "at": "2013-05-10T13:42:41.078097",
                           "value": "1"
                       }
                   ],
                   "current_value": "1",
                   "id": "0"
               }
           ],
           "updated": "2013-05-10T13:43:10.496188",
           "creator": "https://cosm.com/users/64451",
           "title": "House Monitor",
           "email": "gary_pickens@yahoo.com",
           "version": "1.0.0",
           "location": {
               "domain": "physical",
               "private": "false",
               "disposition": "fixed",
               "exposure": "indoor"
           },
           "id": "64451"
       }

=========
PCB notes
=========

Here are some things to add on the next Power Controler.

#. Two eylets to add power wire.
#. One of the ADC to monitor battery voltage.
#. More status leds
#. Three connector for controling relays.  The third pin will contain power.
#. Better heat managment.  A larger pad under the voltage regulator and more
isolation arond the heat sensor.

====
Misc
====
#. Look into Stevedore.  Here are a few URL's:
    #. `SteveDore on GITHUB <https://github.com/dreamhost/stevedore>`_.
    #. `SteveDore on PyPi <http://pypi.python.org/pypi/stevedore>`_.
    #. `Doug HellMann's Blog on Stevedore 3.0 <http://blog.doughellmann.com/2012/08/stevedore-03.html>`_.

#. `Good web page for calculating LM555 values given frequency <http://houseofjeff.com/555-timer-oscillator-frequency-calculator/>`_.

#. `Common Mistakes When Using a 555 Timer <http://www.555-timer-circuits.com/common-mistakes.html>`_.

#. `systemctl <https://wiki.archlinux.org/index.php/Systemd>`_. the command for starting and stopping 
    deamons in some Unix's.
    
#.  `Informatiion about sending back notifications to systemd <http://www.freedesktop.org/software/systemd/man/systemd-notify.html>`_.

#.  `A python version of sd_notify <https://github.com/kirelagin/pysystemd-daemon>`_.

#.  `The definitive guide <http://0pointer.de/blog/projects/systemd-docs.html>`_.

#.   `Explorations into Angstrom syslog and systemd <http://www.mattlmassey.com/2012/07/10/explorations-into-angstrom-syslog-and-systemd>`_.

#.  `Memory monitor software <http://pythonhosted.org/Pympler/>`_.

#.  'Pico -- A light weight web server <https://github.com/fergalwalsh/pico/wiki>`_.

#.  `Super Easy Python JSON Client & Server <http://cpiekarski.com/2011/05/09/super-easy-python-json-client-server>`_.

#.  `Python simple JSON TCP server and client <http://thomasfischer.biz/?p=622>`_.

#.  There was a good article in DrDobb's Journal about 
    `Quantities and Units <http://www.drdobbs.com/jvm/quantities-and-units-in-python/240161101>`_.

#. A good article about using `enums <http://tech.zarmory.com/2013/08/python-enum-on-steroids.html>`_ in python.
 
#. An article on using `structure logs <https://structlog.readthedocs.org/en/latest/>`_.

#. Rules on `building python packages <http://axialcorps.com/2013/08/29/5-simple-rules-for-building-great-python-packages/?goback=.gde_101591_member_270039332#!>`_.



