# -*- coding: utf-8 -*-

import os

import pygtk
pygtk.require('2.0')
import gtk

from gpytiger2c.mainwindow import MainWindow


class UserInterface(object):
    
    def __init__(self, data_dir, pytiger2c_script):
        super(UserInterface, self).__init__()
#        icon_file = os.path.join(data_dir, 'images/pytiger2c.svg')
#        gtk.window_set_default_icon_from_file(icon_file)
        self._main_window = MainWindow(data_dir, pytiger2c_script)
        
    def start(self):
        self._main_window.show()
        gtk.main()


def main(data_dir, pytiger2c_script):
    try:
        ui = UserInterface(data_dir, pytiger2c_script)
        ui.start()
    except KeyboardInterrupt:
        pass
