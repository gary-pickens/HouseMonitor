####################
Beaglebone Build Log
####################

August 24, 2013
===============

I have been having a lot of trouble over the last 6 months keeping 
the Beaglebone computer running.  The last two failures, I believe have
been with the SDE momory cards.  I am about ready to create a new 
SD memory card for the system.  Here is the error message while the 
beaglebone is booting::

The computer died on the second day of my vacation. I had added several
new xbees to monitor the outdoor and the ketchen temperature, and
I was really wanting to get some history on these temperatures.

Tried the new Beaglebone Black
------------------------------

I tried the new beaglebone black.  It has a lot of features I really like. However, I was not able to 
get HouseMonitor working on it.  I think I could get it working but it would take much more time.  The
last thing I was having trouble with was pip.  It was not able to read secure web sites.  I updated
/etc/ca-certificates but that did not help.

Back to the original Beaglebone
-------------------------------

I was thinking, I had updated the OS in June and that was when the problems seemd to start.

1.  I installed Angstrom-Cloud9-IDE-GNOME-eglibc-ipk-v2012.12-beaglebone-2012.11.22.img.xz.
   *. It booted up but the network would not start.
   *. I tried rebooting several times but that did not help.
   *. Here is the output from dmesg::
   
      [    4.400360] ip_tables: (C) 2000-2006 Netfilter Core Team
      [    4.746887] PHY 0:01 not found
      [    4.780670] ADDRCONF(NETDEV_UP): eth0: link is not ready

2. Next I will try Angstrom-Cloud9-IDE-GNOME-eglibc-ipk-v2012.12-beaglebone-2013.4.13.img.xz.
   I know I have had good results with one of these images.
   

 