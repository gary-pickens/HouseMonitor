'''
Created on Sep 18, 2012

@author: Gary
'''
from datetime import datetime


class GetDateTime( object ):
    '''
    A GetDateTime object so that unit tests mock will work on it.  Other
    routines may need to be added as they are needed
    '''
    time_format = '%Y/%m/%d %H:%M:%S'
    dt = None

    #  TODO work on documentation for function
    def __init__( self, date_time_value=None, year=None, month=None, day=None, hour=None, minute=None, second=None ):
        '''
        Constructor
        '''
        if ( date_time_value == None and
             year != None and month != None and day != None and
             hour != None and minute != None and second != None ):
            try:
                self.dt = datetime( year, month, day, hour, minute, second )
            except Exception as ex:
                print ex
        elif date_time_value == None:
            self.dt = datetime.utcnow()
        else:
            self.dt = date_time_value


    def __str__( self ):
        '''
        Return a standard datetime string

        :returns: time as formatted with time_format above
        :rtype: string in this format 1966:10:03 13:42:51

        from lib.getdatetime import GetDateTime
        utc = GetDateTime()
        print(utc)

        '''
        return self.dt.strftime( '%Y/%m/%d %H:%M:%S' )

    def toString( self ):
        '''
        Return a standard datetime string

        :returns: time as formatted with time_format above
        :rtype: string in this format 1966:10:03 13:42:51


        from lib.getdatetime import GetDateTime
        utc = GetDateTime()
        print(utc)

        '''
        return self.dt.strftime( '%Y/%m/%d %H:%M:%S' )

    def isoformat( self ):
        '''
        Return a iso 8601 formatted string of the date/time

        :returns: time as formatted with time_format above
        :rtype: string in this format YYYY-MM-DDTHH:MM:SS.mmmmmm

        from lib.getdatetime import GetDateTime
        utc = GetDateTime()
        print(utc.isoformat())

        '''
        return self.dt.isoformat()

    def datetime( self ):
        return self.dt

    def __repr__( self ):
        'GetDateTime(year={}, month={}, day={}, hour={}, minute={}, second={})'. \
            format( self.dt.year, self.dt.month, self.dt.day, self.dt.hour, self.dt.minute, self.dt.second )
