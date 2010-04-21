# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

from gpytiger2c.xmlwidget import XMLWidget


class MainWindow(XMLWidget):
    
    def __init__(self, data_dir, pytiger2c_script):
        super(MainWindow, self).__init__(data_dir, 'main_window')
