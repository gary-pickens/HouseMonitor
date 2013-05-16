'''
Created on May 11, 2013

@author: Gary
'''

from PySide.QtGui import *
from PySide.QtCore import *
import pprint
import datetime

class MonitorModel( QAbstractTableModel ):

    proxy = None
    options = None
    values = None
    parent = None
    previous_data = None

    old_row_count = 4
    new_row_count = 11
    latest_data = [['one', 'two', 'three', '20131212T12:12:12'],
                   ['one', 'two', 'three', '20131212T12:12:12'],
                   ['one', 'two', 'three', '20131212T12:12:12']
                   ]
    monitored_data = None

    def __init__( self, monitor_data, parent=None ):
        super( MonitorModel, self ).__init__( parent )
        self.monitored_data = monitor_data
        self.parent = parent

    def read_data( self ):
        old_row_count = self.rowCount()
        self.latest_data = self.monitored_data.retreive_data()
        new_row_count = self.rowCount()
        self.parent.view.dataChanged( self.createIndex( 0, 0 ), self.createIndex( len( self.latest_data ) - 1, 4 ) )
        if old_row_count != new_row_count:
            self.parent.view.rowCountChanged( old_row_count, new_row_count )

    def rowCount( self, index=QModelIndex() ):
        """ Returns the number of rows the model holds. """
        print len( self.latest_data )
        return 11

    def columnCount( self, index=QModelIndex() ):
        """ Returns the number of columns the model holds. """
        return 4

    def data( self, index, role=Qt.DisplayRole ):
        """ Depending on the index and role given, return data. If not
            returning data, return None (PySide equivalent of QT's
            "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len( self.latest_data ):
            return None
        if role == Qt.TextAlignmentRole:
            if index.column() == 2:
                return  0x82    # Qt.AlignRight or Qt.AlignCenter

        if role == Qt.DisplayRole:
            device = self.latest_data[index.row()][0]
            port = self.latest_data[index.row()][1]
            value = self.latest_data[index.row()][2]
            dt = self.latest_data[index.row()][3]

            if index.column() == 0:
                return device
            elif index.column() == 1:
                return port
            elif index.column() == 2:
                return value
            elif index.column() == 3:
                if type( dt ) == str:
                    x = datetime.datetime.strptime( dt, '%Y%m%dT%H:%M:%S' )
                    return x.strftime( '%H:%m:%S %m/%d/%Y' )
                else:
                    return dt.strftime( '%H:%M:%S %m/%d/%Y' )

        return None

    def headerData( self, section, orientation, role=Qt.DisplayRole ):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "Device"
            elif section == 1:
                return "Port"
            elif section == 2:
                return "Value"
            elif section == 3:
                return "Date/Time"
        return None

    def flags( self, index ):
        """ Set the item flags at the given index. Seems like we're
            implementing this function just to see how it's done, as we
            manually adjust each tableView to have NoEditTriggers.
        """
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags( QAbstractTableModel.flags( self, index ) | Qt.ItemIsEnabled )

