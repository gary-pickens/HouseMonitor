'''
Created on Sep 18, 2012

@author: Gary
'''
import os


class OsWalk(object):
    '''
    A OsWalk object so that unit tests mock will work on it.  Other
    routines may need to be added as they are needed
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super(OsWalk, self).__init__()

    def walk(self, directory):
        return os.walk(directory)
