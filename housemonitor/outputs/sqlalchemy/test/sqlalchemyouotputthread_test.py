'''
Created on Oct 24, 2013

@author: gary
'''
import unittest
from mock import Mock, MagicMock, patch
from housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread import SqlAlchemyOutputThread
from housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread import Data
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.lib.constants import Constants


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    @patch( 'housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.HMQueue' )
    def test_connectionString(self, queue):
        connectionString = 'mysql+mysqldb://root:Helena&Patrick@ubu/housemonitor'
        t = SqlAlchemyOutputThread( queue, False )
        self.assertEqual(t.connectionString, connectionString)
        queue.assertCalledOnce()

    @patch( 'housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.HMQueue' )
    def test_logger_name(self, queue):
        log_name = Constants.LogKeys.SQL_ALCHEMY_LOG
        t = SqlAlchemyOutputThread( queue, False )
        self.assertEqual(t.logger_name, log_name)
        queue.assertCalledOnce()
        
    @patch('housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.create_engine')
    @patch( 'housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.HMQueue' )
    def test_KeyBoardInterrupt_in_connect(self, queue, create_engine):
        create_engine.side_effect=KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            sql = SqlAlchemyOutputThread(queue, False)
            sql.connect()
            self.assertFalse(sql.connectedToDatabase)

    @patch('housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.create_engine')
    @patch( 'housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.HMQueue' )
    def test_Exception_in_connect(self, queue, create_engine):
        create_engine.side_effect=Exception()
        sql = SqlAlchemyOutputThread(queue, False)
        sql.connect()
        self.assertFalse(sql.connectedToDatabase)

    def session_function(self):
        return 99
        
    @patch('housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.SqlBase.metadata.create_all')
    @patch('housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.sessionmaker')
    @patch('housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.create_engine') 
    @patch('housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.HMQueue' )
    def test_connect_function_calls(self, queue, create_engine, sessionmaker, create_all):
        create_engine.return_value = 55
        sessionmaker.return_value=self.session_function
        
        sql = SqlAlchemyOutputThread(queue, False)
        sql.connect()

        create_engine.assert_called_once_with('mysql+mysqldb://root:Helena&Patrick@ubu/housemonitor', echo=True)
        sessionmaker.assert_called_once_with( bind=55 )
        self.assertEqual(sql.session, 99)
        create_all.assert_called_once_with(55)
        
    @patch( 'housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread.HMQueue' )        
    def test_storeData(self, queue):
        packet = {Constants.DataPacket.value: 101,
                Constants.DataPacket.units: 'C',
                Constants.DataPacket.device: 'device',
                Constants.DataPacket.port: 'port',
                Constants.DataPacket.arrival_time: '9 AM'
                }        
        
        sql = SqlAlchemyOutputThread(queue, False)
        sql.session = MagicMock()
        sql.session.add = MagicMock()
        sql.session.commit = MagicMock()
        sql.storeData(packet)
        
        sql.session.add.assert_called_once()  #_with(Data(101, "C", "device", "port", "9 AM"))
        sql.session.commit.assert_called_once_with()
       

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_connectionString']
    unittest.main()