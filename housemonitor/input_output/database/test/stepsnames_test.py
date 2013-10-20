'''
Created on Oct 17, 2013

@author: gary
'''
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from housemonitor.lib.constants import Constants
from housemonitor.input_output.database.stepnames import StepNames

class Test( unittest.TestCase ):


    def test_StepNames( self ):
        sn = StepNames( 'abc' )
        self.assertEqual( '<StepNames("abc")>', sn.__repr__() )

    def test_inspect_sql( self ):

        engine = create_engine( 'sqlite:///:memory:', echo=True )
        Session = sessionmaker( bind=engine )
        session = Session()

        sn = StepNames( Constants.TopicNames.TMP36Volts2CentigradeStep )
        print( sn.__table__ )
        self.assertEqual( sn.step_name, Constants.TopicNames.TMP36Volts2CentigradeStep )

        session.add( sn )
        session.commit()

        topics = session.query( StepNames ).filter_by( step_name=Constants.TopicNames.TMP36Volts2CentigradeStep ).first()

        print( topics )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

    steps = [
        Constants.TopicNames.SchedulerAddIntervalStep,
        Constants.TopicNames.SchedulerAddDateStep,
        Constants.TopicNames.SchedulerAddCronStep,
        Constants.TopicNames.SchedulerAddOneShotStep,
        Constants.TopicNames.SchedulerDeleteJob,
        Constants.TopicNames.SchedulerPrintJobs,
        Constants.TopicNames.SchedulerStep,
        Constants.TopicNames.CurrentValueStep,
        Constants.TopicNames.AverageStep,
        Constants.TopicNames.Centigrade2FahrenheitStep,
        Constants.TopicNames.GarageDoorStateStep,
        Constants.TopicNames.FormatValueStep,
        Constants.TopicNames.onBooleanChangeStep,
        Constants.TopicNames.OneInNStep,
        Constants.TopicNames.TMP36Volts2CentigradeStep,
        Constants.TopicNames.ZigbeeAnalogNumberToVoltsStep,
        Constants.TopicNames.CentigradeToFahrenheitStep,
        Constants.TopicNames.MaxValue,
        Constants.TopicNames.MinValue,
        Constants.TopicNames.Statistics,
        Constants.TopicNames.UpTime,
        Constants.TopicNames.ZigBeeOutput,
        Constants.TopicNames.Step,
        Constants.TopicNames.StatusPanel_GarageDoorMonitor,
        Constants.TopicNames.StatusPanel_ProcessDelayedAlarm,
        Constants.TopicNames.StatusPanel_DisableAlarmButton,
        Constants.TopicNames.StatusPanel_SystemCheck,
        Constants.TopicNames.StatusPanel_SilenceAlarm,
        Constants.TopicNames.xmlDeviceConfiguration,
        Constants.TopicNames.Outputs,
        Constants.TopicNames.COSM,
        Constants.TopicNames.ProcessInputs,
        Constants.TopicNames.UnitTest,
        Constants.TopicNames.ALL_TOPICS,
    ]
