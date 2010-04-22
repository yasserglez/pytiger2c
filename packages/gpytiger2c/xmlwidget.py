# -*- coding: utf-8 -*-

import os

import pygtk
pygtk.require('2.0')
import gtk


class XMLWidget(object):

    def __init__(self, data_dir, widget_name):
        self._data_dir = data_dir
        self._builder = gtk.Builder()
        xml_file = os.path.join(self._data_dir, 'glade', '%s.glade' % widget_name.replace('_', '-'))
        self._builder.add_from_file(xml_file)
        self._widget = self._builder.get_object(widget_name)
        self._builder.connect_signals(self)

    def __getattr__(self, name):
        return getattr(self._widget, name)
