
########################
Python UnitTest Cookbook
########################

*********************
Using Patch Decorator
*********************

==========
References
==========

#. `Patch Man Page <http://www.voidspace.org.uk/python/mock/patch.html>`_.
#. `Where to Patch <http://docs.python.org/3/library/unittest.mock.html#where-to-patch>`_.
#. `Patching in the wrong place <http://alexmarandon.com/articles/python_mock_gotchas/>`_.


=======================================
A good template for creating unit tests
=======================================

Here is my current template for starters:::

    from inputs.zigbeeinput.beaglebonexbeecommunications import BeagleboneXbeeCommunications

    import unittest
    import datetime
    from lib.common import Common
    import logging.config
    from lib.constants import Constants
    import pprint
    from mock import Mock, MagicMock, patch
    from lib.getdatetime import GetDateTime
    
    
    class Test(unittest.TestCase):
        logger = logging.getLogger('UnitTest')
    
        def setUp(self):
            logging.config.fileConfig("house_monitor_logging.conf")
    
        def tearDown(self):
            pass
    
        def testName(self):
            pass
    
    if __name__ == "__main__":
        # import sys;sys.argv = ['', 'Test.testName']
        unittest.main()
        

==========================
Determining the right spot
==========================

Patching in the wrong place.  Hmmm, where did the link go?


****************************
How to patch the GetDateTime
****************************

This took several attempts to get right:

Here is a section of the code I am trying to test.

GetDateTime uses datetime and does a few things differently.  Such as the str() command,
I wanted to use my own format so I wrote my own __str__() funcion.  It looks as follows:

    def __str__(self):
        '''
        Return a standard datetime string

        :returns: time as formatted with time_format above
        :rtype: string in this format 1966:10:03 13:42:51

        :Example:

        from lib.getdatetime import GetDateTime
        utc = GetDateTime()
        print(utc)

        '''
        return self.dt.strftime('%Y/%m/%d %H:%M:%S')

But when I started testing a function that was using it, I was getting all sorts of errors.

My first attempt was using patch and __str__(). But after numerous attepts I decided to
back up and try something else. I wrote a toString function that does exactly the
same thing,  and I was able to get it to work.  So, using this, I was able to get the original
code working.

Here is some of the code I was trying to test.

::

       type = 'xbee'
        ''' THe type of data that is being passed. '''
        packet = None
        ''' The data. '''
        arrival_time = GetDateTime()
        ''' The arrival time of the data.'''
        data = {}
        ''' Additional data such as it source. '''
    
        def __init__(self, type='xbee', packet={}, arrival_time=GetDateTime(), data={}):
            ''' Store the data in the envelope.
    
            :param type: the type of data that this packet contain.
            :type type: string
            :param packet: the data
            :type packet:  dict
            :param arrival_time: The time that the packet was received by the computer system
            :type arrival_time: datatime
            :param data: Additional information about the packet. (device, port, units, etc)
            :type data: dict
    
            '''
            self.type = type
            self.packet = packet
            self.arrival_time = arrival_time
            self.data = data


#. First successful attempt:::


    def test_storing_data(self):
        test = DataEnvelope()
        test.arrival_time.toString = MagicMock()
        test.arrival_time.toString.return_value = '2012/10/03 01:02:03'
        self.assertEqual(test.arrival_time.toString(), '2012/10/03 01:02:03')


#. Second successful attempt:::

    @patch('inputs.dataenvelope.GetDateTime.toString')
    def test_storing_data_using_patch(self, str):
        test = DataEnvelope()
        str.return_value = '2012/10/03 01:02:03'
        self.assertEqual(test.arrival_time.toString(), '2012/10/03 01:02:03')

#. Third successful attempt:::

    @patch('inputs.dataenvelope.GetDateTime.__str__')
    def test_storing_data_using_patch_and___str__(self, s):
        test = DataEnvelope()
        s.return_value = '2012/10/03 01:02:03'
        self.assertEqual(test.arrival_time.__str__(), '2012/10/03 01:02:03')
 
#. Forth successful attempt:::

    @patch('inputs.dataenvelope.GetDateTime.__str__')
    def test_storing_data_using_patch_and___str__1(self, s):
        test = DataEnvelope()
        s.return_value = '2012/10/03 01:02:03'
        self.assertEqual(str(test.arrival_time), '2012/10/03 01:02:03')

The fourth attempt seems to be the best one and the one I am sticking with as my final version.

*********************************************
How to disable reading the configuration file
*********************************************

The unit test you will have to create a config data structure that contains the configuration data that would
be read by the configuration routines:::

    config_data = \
    {'device 1': {'port 1': {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: 'disposition',
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 'lat',
                                Constants.Cosm.location.longitude: 'lon',
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: 'auto_feed_url',
                                Constants.Cosm.creator: 'creator',
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: 'email',
                                Constants.Cosm.feed: 'feed',
                                Constants.Cosm.id: 'id',
                                Constants.Cosm.private: 'private',
                                Constants.Cosm.status: 'status',
                                Constants.Cosm.tags: 'tags',
                                Constants.Cosm.title: 'title',
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: 'version',
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }}}

Then patch the test module as follows:::

    @patch('outputs.cosm.send.CosmConfiguration.configure')
    def test_createDataStream(self, config):
        options = None
        cs = COSMSend(options)
        config.assert_called_once_with()
        cs.config = self.config_data
        device = 'device 1'
        port = 'port 1'
        current_value = 10
        data = {'device': device,
                'port': port,
                Constants.DataPacket.arrival_time: '12:12:12 12/12/10',
                Constants.DataPacket.current_value: current_value}
        cs.createDataStream(device, port, data)
        item = cs.datastreams.pop()
        self.assertEqual(item[Constants.Cosm.datastream.min_value], 0)
        self.assertEqual(item[Constants.Cosm.datastream.max_value], 100)
        self.assertEqual(item[Constants.Cosm.datastream.tags], 'tags')
        self.assertEqual(item[Constants.DataPacket.current_value], current_value)
        self.assertEqual(item[Constants.Cosm.datastream.cosm_channel], '1')

The worst part is getting the patch string correct.  It is broken in to two parts:

1.  The first part points to the namespace that is being tested.
2.  The second part is the Actual routine that is being called.

In the above example the patch line contains 'outputs.cosm.send' and is the first part.
The second part is 'CosmConfiguration.configure' which is the routine that we want to modify with a MagicMock.

Notice the added argument to the function.  This is the new mock object.

****************************
How to patch out Common.send
****************************

I resently moved send from a class to Common because I was needing to call it from
other places outside its former home.  I made it a static method with the following
declaration:     @staticmethod

After this all my unit tests stepped working.  This is how I got them working.

::

    @patch('steps.onbooleanchange.Common.send')
    def test_onBooleanChange_with_one_device_and_port(self, send):
        device = 'device'
        port = 'port'
        N = onBooleanChange()

        N.config = {device: {port: False}}
        data = {}
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port

        listeners = ['a', 'b', 'c']
        N.substep(True, data, listeners)
        self.assertEqual(N.current_value[device][port], True)
        send.assert_called_once_with(True, {'device': device, 'port': port}, ['a', 'b', 'c'])
        send.reset_mock()


*******************************
Instantuating a class in method
*******************************


*In patch I give the namespace then the name of the class to instuate.*

::

    @patch('inputs.zigbeeinput.xbeecommunications.ZigBee')
    def test_successful_connect(self, zigbee):
        rv = 55
        xbee = myClass()
        xbee.setup = MagicMock()
        xbee.setup.return_value = rv

        xbee.connect()
        xbee.setup.assert_called_once_with()
        zigbee.assert_called_once_with(rv)


**************************************************************
Having a class give an exception then on the next loop succeed
**************************************************************

I have a side effect function that counts the times it is called.  The first tiem it throws an exception.
The second time it returns a valid value.

::

    count = 0

    def side_effect(self):
        if self.count == 0:
            self.count += 1
            raise IOError("OhOh")
        else:
            self.count += 1
            return 55

    @patch('inputs.zigbeeinput.xbeecommunications.ZigBee')
    def test_fail_to_connect_first_time_then_succeed_second_time(self, zigbee):
        rv = 55
        xbee = myClass()
        xbee.setup = MagicMock(side_effect=self.side_effect)
        xbee.setup.return_value = rv

        xbee.connect()
        xbee.setup.assert_any_call()
        zigbee.assert_called_once_with(rv)

*********************
Testing open and read
*********************

Here is some reading:

   * `Mocking an open and read in with statement <http://stackoverflow.com/questions/1289894/how-do-i-mock-an-open-used-in-a-with-statement-using-the-mock-framework-in-pyth>`_.
      
   * `Mocking open in context manager <http://java.dzone.com/articles/mocking-open-context-manager>`_.
    