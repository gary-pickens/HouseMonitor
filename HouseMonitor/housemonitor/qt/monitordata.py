'''
Created on May 13, 2013

@author: Gary
'''
from PySide import QtCore
import copy

class MonitorData( object ):
    '''
    classdocs
    '''
    previous_data = None
    data = [['one', 'two', 'three', 'four']]
    mutex = None

    rd = QtCore.Signal()

    def __init__( self ):
        '''
        Constructor
        '''
        self.mutex = QtCore.QMutex()

    def write_data( self, data ):
        try:
            self.mutex.lock()
            self.data = copy.copy( data )
        finally:
            self.mutex.unlock()

    def retreive_data( self ):
        try:
            self.mutex.lock()
            data = copy.copy( self.data )
        finally:
            self.mutex.unlock()
        return data
