'''
Created on Oct 22, 2012

@author: Gary
'''

from housemonitor.hm.inputthead import InputThread
from housemonitor.hm.display import Display
from time import sleep


if __name__ == '__main__':

    cv = {}
    it = InputThread( cv )
    it.start()

    sleep( 15 )
    display = Display( cv )
    display.update()
    display.run()
