# -*- coding: utf-8 -*-

import os

import pygtk
pygtk.require('2.0')
import gtk

from pytiger2c import __authors__, __version__
from gpytiger2c.xmlwidget import XMLWidget


class AboutDialog(XMLWidget):
    
    def __init__(self, data_dir):
        super(AboutDialog, self).__init__(data_dir, 'about_dialog')
        logo_file = os.path.join(data_dir, 'images', 'pytiger2c.svg')
        self.set_logo(gtk.gdk.pixbuf_new_from_file_at_size(logo_file, 128, 128))
        self.set_version(__version__)
        self.set_copyright('\n'.join(['Copyright (C) 2009, 2010 %s' % a for a in __authors__]))
        self.set_comments('GUI for PyTiger2C, a Tiger compiler implemented in Python that generates C.')
