from distutils.core import setup

setup( 
    name='HouseMonitor',
    version='4.0.0',
    author='Gary Pickens',
    author_email='gary_pickens@yahoo.com',
    packages=['housemonitor',
              'housemonitor/configuration',
              'housemonitor/inputs',
              'housemonitor/inputs/zigbeeinput',
              'housemonitor/lib',
              'housemonitor/outputs',
              'housemonitor/outputs/cosm',
              'housemonitor/outputs/xmlrpc',
              'housemonitor/outputs/zigbee',
              'housemonitor/steps',
              'housemonitor/utils'
              ],
              package_data={'housemonitor': ['config/*.xml', 'house_monitor_logging.conf', "config/cacerts.txt", 'housemonitor.service']},
    scripts=['bin/HouseMonitor',
             'bin/displayXbeeStatus',
             'bin/mon',
             'bin/NodeDiscovery',
             'bin/XbeeConfig'
             ],
    url='http://pypi.python.org/pypi/HouseMonitor/',
    license='license.txt',
    description='Tools for monitoring a house with XBee\'s.',
    long_description=open( 'README.txt' ).read(),
    platforms=['NT', 'linux', 'beaglebone'],
    install_requires=[
        "XBee >= 2.0.0",
        "apscheduler>=2.0.3",
        "httplib2>=0.7.4",
        "mock>=1.0b1",
        "nose>=1.2.1",
        "run",
        "pyOpenSSL>=0.13",
        "pypubsub>=3.1.2",
        "pyserial>=2.6",
#        "txPachube>=0.0.3"
    ],
 )
