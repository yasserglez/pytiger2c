# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

from gpytiger2c.xmlwidget import XMLWidget


class ASTWindow(XMLWidget):
    
    def __init__(self, data_dir, jpg_filename):
        super(ASTWindow, self).__init__(data_dir, 'ast_window')
        self._jpg_filename = jpg_filename
        image = self._builder.get_object('image')
        image.set_from_file(self._jpg_filename)
