'''
Created on May 11, 2013

@author: Gary
'''

from PySide.QtGui import *
from PySide.QtCore import *
from monitormodel import MonitorModel
from monitorthread import MonitorThread
from monitordata import MonitorData


class Window( QWidget ):
    md = None
    mt = None
    model = None
    view = None

    def __init__( self, parent=None ):
        super( Window, self ).__init__( parent )

        self.md = MonitorData()
        self.model = MonitorModel( self.md, parent=self )

        self.mt = MonitorThread( self.md )
        self.mt.start()
        self.connect( self.mt, SIGNAL( 'read_data()' ), self.model.read_data, Qt.DirectConnection )

        self.view = QTableView()
        self.view.setModel( self.model )

        self.resize( 670, 800 )
        layout = QGridLayout()
        layout.addWidget( self.view, 1, 0, 1, 2 )
        self.view.horizontalHeader()
        self.view.horizontalHeader().resizeSection( 0, 300 )
        self.view.horizontalHeader().resizeSection( 3, 125 )

        self.setLayout( layout )
        self.setWindowTitle( "House Monitor Viewer" )

    def updateLog( self, number ):
        self.logViewer.append( "%d items added." % number )

if __name__ == '__main__':

    import sys

    app = QApplication( sys.argv )

    window = Window()
    window.show()

    sys.exit( app.exec_() )
