'''
Created on Oct 24, 2012

@author: Gary
'''
from Tkinter import Tk, Frame, BOTH, W, E, N, S


class Display(object):
    '''
    classdocs
    '''
    TITLE = 'House Monitor'

    TIME_COLUMN = 0
    NAME_COLUMN = 1
    VALUE_COLUMN = 2

    mainframe = None
    proxy = None

    current_row = 0

    current_values = {}

    def __init__(self, current_values):
        '''
        Constructor
        '''
        self.current_values = current_values
        super(Display, self).__init__()
        self.root = Tk()
        self.root.title(self.TITLE)
#        self.mainframe = Frame(self.root, padding="3 3 12 12")

        self.mainframe = Frame(self.root)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        print(current_values)

#        self.display_header()

    def display_header(self):
        Tk.Label(self.mainframe, text='Time', width=15, background='lightblue').grid(column=self.TIME_COLUMN, row=self.current_row, sticky=W)
        Tk.Label(self.mainframe, text='Name', width=45, background='lightblue').grid(column=self.NAME_COLUMN, row=self.current_row, sticky=W)
        Tk.Label(self.mainframe, text='Value', width=15, background='lightblue').grid(column=self.VALUE_COLUMN, row=self.current_row, sticky=W)
        self.current_row = self.current_row + 1

    def update(self):
        self.current_row = 1
        for device in self.current_values.keys():
            for port in self.current_values[device].keys():

                arrival_time = self.current_values[device][port]['arrival_time']
                Tk.Label(self.mainframe, text=arrival_time).grid(column=self.TIME_COLUMN, row=self.current_row, sticky=W)

                name = self.current_values[device][port]['name']
                Tk.Label(self.mainframe, text=name).grid(column=self.NAME_COLUMN, row=self.current_row, sticky=W)

                value = self.current_values[device][port]['current_value']
                units = self.current_values[device][port]['units']
                value = '{}{}'.format(value, units)
                Tk.Label(self.mainframe, text=value).grid(column=self.VALUE_COLUMN, row=self.current_row, sticky=W)
                self.current_row = self.current_row + 1

    def run(self):
        self.root.mainloop()
