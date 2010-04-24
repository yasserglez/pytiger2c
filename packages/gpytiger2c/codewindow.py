# -*- coding: utf-8 -*-

import os

import pygtk
pygtk.require('2.0')
import gtk
import pango
import gtksourceview2 as gtksourceview

from gpytiger2c.xmlwidget import XMLWidget


class CodeWindow(XMLWidget):
    
    def __init__(self, data_dir, c_filename):
        super(CodeWindow, self).__init__(data_dir, 'code_window')
        self._c_filename = c_filename
        self._init_code_view()
        self._widget.show_all()
        
    def _init_code_view(self):
        # Creating the buffer.
        code_buffer = gtksourceview.Buffer()
        code_buffer.set_highlight_matching_brackets(True)
        manager = gtksourceview.LanguageManager()
        manager.set_search_path([os.path.join(self._data_dir, 'gtksourceview')])
        language = manager.get_language('c')
        code_buffer.set_language(language)
        code_buffer.set_highlight_syntax(True)
        # Creating the viewer.
        code_view = gtksourceview.View(code_buffer)
        code_view.modify_font(pango.FontDescription('monospace'))
        code_view.set_show_line_numbers(True)
        code_view.set_show_line_marks(False)
        code_view.set_show_right_margin(False)
        code_view.set_editable(False)
        code_view.set_highlight_current_line(True)
        # Add the source view to the window.
        scrolledwindow = self._builder.get_object('scrolledwindow')
        scrolledwindow.add(code_view)
        # Setting the text of the buffer.
        with open(self._c_filename) as fd:
            code_buffer.set_text(fd.read())
