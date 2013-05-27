'''
Created on Sep 25, 2012

@author: Gary
'''


class Constants( object ):

    class GlobalIndexs( object ):
        current_values = 'current_values'
        options = 'options'
        args = 'args'
        start_time = 'start time'

    class XbeeConfiguration( object ):
        """
        Contains keys used in the device configuration
        """
        xbee = 'xbee'
        source_address = 'source_address'
        network_address = 'network_address'
        name = 'name'
        steps = 'steps'
        description = 'description'
        units = 'units'
        type = 'type'

        """
        Windows constants
        """
        xbee_windows_port = 'xbee_windows_port'
        xbee_windows_baud = 'xbee_windows_baud'
        """
        Beaglebone constants

        """
        xbee_beaglebone_port = 'xbee_beaglebone_port'
        xbee_beaglebone_rx_mux = 'xbee_beaglebone_rx_mux'
        xbee_beaglebone_tx_mux = 'xbee_beaglebone_tx_mux'
        xbee_beaglebone_mux_mode = 'xbee_beaglebone_mux_mode'
        xbee_beaglebone_timeout = 'xbee_beaglebone_timeout'
        xbee_beaglebone_receive_enable = 'xbee_beaglebone_receive_enable'
        xbee_beaglebone_transmit_enable = 'xbee_beaglebone_transmit_enable'
        xbee_beaglebone_baudrate = 'xbee_beaglebone_baudrate'

    class DataPacket( object ):
        """
        Contains the keys that are included in the data packet
        that accompanies the data through the system.
        """
        arrival_time = 'at'
        device = 'device'
        port = 'port'
        name = 'name'
        steps = 'steps'
        units = 'units'
        tags = 'tags'
        current_value = 'current_value'
        max_value = 'max_value'
        min_value = 'min_value'
        listeners = 'listeners'
        scheduler_id = 'scheduler_id'

        action = 'action'
        send = 'send'
        accumulate = 'accumulate'
        email_list_name = 'email list name'
        email_message = 'email message'

    class EnvelopeTypes( object ):
        '''
        Contains definitions that describe the data that is passed in the input queue
        '''
        xbee = 'xbee'
        status = 'status'

    class XBee( object ):
        """
        Contains the keys used by the XBee driver
        """
        command = 'command'
        frame_id = 'frame_id'
        id = 'id'
        options = 'options'
        parse_as_io_samples = 'parse_as_io_samples'
        rx_io_data_long_addr = 'rx_io_data_long_addr'
        samples = 'samples'
        source_addr = 'source_addr'
        source_addr_long = 'source_addr_long'
        adc_0 = 'adc-0'
        adc_1 = 'adc-1'
        adc_2 = 'adc-2'
        adc_3 = 'adc-3'
        adc_4 = 'adc-4'
        adc_5 = 'adc-5'
        adc_6 = 'adc-6'
        adc_7 = 'adc-7'
        dio_0 = 'dio-0'
        dio_1 = 'dio-1'
        dio_2 = 'dio-2'
        dio_3 = 'dio-3'
        dio_4 = 'dio-4'
        dio_5 = 'dio-5'
        dio_6 = 'dio-6'
        dio_7 = 'dio-7'

        class api_commands( object ):
            at = 'at'
            queued_at = 'queued_at'
            remote_at = 'remote_at'
            tx = 'tx'
            tx_explicit = 'tx_explicit'

        class api_responses( object ):
            rx = 'rx'
            remote_at_response = 'remote_at_response'
            rx_explicit = 'rx_explicit'
            rx_io_data_long_addr = 'rx_io_data_long_addr'
            tx_status = 'tx_status'
            status = 'status'
            at_response = 'at_response'
            node_id_indicator = 'node_id_indicator'

    class Cosm( object ):
        """
        Contains the constants used for sending data to COSM.com
        """
        apikey = 'apikey'
        auto_feed_url = 'auto_feed_url'
        creator = 'creator'
        created = 'created'
        email = 'email'
        feed = 'feed'
        id = 'id'
        private = 'private'
        status = 'status'
        tags = 'tags'
        title = 'title'
        updated = 'updated'
        url = 'url'
        version = 'version'
        location_str = 'location'
        datastreams = 'datastreams'

        """
        Variables in the datastream fields
        """
        class datastream( object ):
            at = 'at'
            current_value = 'current_value'
            cosm_channel = 'cosm_channel'
            label = 'label'
            max_value = 'max_value'
            min_value = 'min_value'
            tags = 'tags'
            unit = 'unit'
            id = 'id'
            datapoints = 'datapoints'

        """
        Variable from the location fields
        """
        class location( object ):
            created = 'created'
            disposition = 'disposition'
            domain = 'domain'
            exposure = 'exposure'
            latitude = 'lat'
            longitude = 'lon'
            private = 'private'

        '''
        Constants for sending data to the send object
        '''
        class packet( object ):
            data = 'data'
            current_value = 'current_value'

    """
    Variouse input methods such as xbee, xmlrpc etc
    """
    class input_methods( object ):
        xbee = 'xbee'

    class process( object ):
        '''
        Constants that are used in process classes.
        '''
        format = 'format'
        number_of_samples = 'number_of_samples'

    class TopicNames( object ):
        #  steps
        SchedulerAddIntervalStep = 'step.SchedulerAddInterval'
        SchedulerAddDateStep = 'step.SchedulerAddDateStep'
        SchedulerAddCronStep = 'step.ScheduleraAddCron'
        SchedulerAddOneShotStep = 'step.SchedulerOneShot'
        SchedulerDeleteJob = 'step.SchedulerDeleteJob'
        SchedulerPrintJobs = 'step.SchedulerPrintJobs'
        SchedulerStep = 'step.Scheduler'
        CurrentValueStep = 'step.CurrentValue'
        AverageStep = 'step.Average'
        Centigrade2FahrenheitStep = 'step.Centigrade_to_Fahrenheit'
        GarageDoorStateStep = 'step.garage_door_state'
        FormatValueStep = 'step.FormatValue'
        onBooleanChangeStep = 'step.onBooleanChange'
        OneInNStep = 'step.oneInN'
        TMP36Volts2CentigradeStep = 'step.TMP_36_Volts_to_Centigrade'
        ZigbeeAnalogNumberToVoltsStep = 'step.ZigbeeAnalogNumberToVolts'
        CentigradeToFahrenheitStep = "step.Centigrade_to_Fahrenheit"
        MaxValue = "step.MaxValue"
        MinValue = "step.MinValue"
        Statistics = "step.Statistics"
        UpTime = "step.Uptime"
        ZigBeeOutput = "step.ZigBeeOutput"
        SendMailMessage = "step.SendMailMessage"
        Step = "step"

        StatusPanel_GarageDoorMonitor = 'step.GarageDoorMonitor'
        StatusPanel_ProcessDelayedAlarm = 'step.ProcessDelayedAlarm'
        StatusPanel_DisableAlarmButton = 'step.DisableAlarmButton'
        StatusPanel_SystemCheck = 'step.StatusPanel_SystemCheck'
        StatusPanel_SilenceAlarm = 'step.StatusPanel_SilenceAlarm'

        #  Configurations
        xmlDeviceConfiguration = 'configuration.xmlDeviceConfiguration'
        #  Outputs
        Outputs = 'outputs'
        COSM = 'outputs.COSM'
        #  Inputs
        ProcessInputs = 'inputs.ProcessInputs'
        #  Misc
        UnitTest = 'UnitTest'
        ALL_TOPICS = 'ALL_TOPICS'

    class LogKeys( object ):
        Scheduler = 'scheduler'
        inputs = 'inputs'
        inputsZigBee = 'inputsZigBee'
        configuration = 'configuration'
        lib = 'lib'
        HouseMonitor = 'HouseMonitor'
        steps = 'steps'
        outputsCOSM = 'outputsCOSM'
        outputsXMLRPC = 'outputsXMLRPC'
        outputsZigBee = 'outputsZigBee'
        PubSubAid = 'PubSubAid'
        StatusPanel = 'StatusPanel'
        ComputerMonitor = 'ComputerMonitor'
        SendMail = 'SendMail'
        UnitTest = 'UnitTest'

    class Queue( object ):
        high_priority = 1
        mid_priority = 5
        default_priority = mid_priority
        low_priority = 10

    class SchedulerName( object ):
        LED_Status_Update = 'LED Status Update'
        Uptime_update = 'uptime'

    class SendEMailLists( object ):
        GarageDoorOpening = 'Garage Door Opening',
        GarageDoorClosed = 'Garage Door Closed',
        GarageDoorOpenTooLong = 'Garage Door Open Too Long',


