# -*- coding: utf-8 -*-

import os
import subprocess

import pygtk
pygtk.require('2.0')
import gtk
import pango
import gtksourceview2 as gtksourceview

from gpytiger2c.xmlwidget import XMLWidget
from gpytiger2c.aboutdialog import AboutDialog
from gpytiger2c.codewindow import CodeWindow
from gpytiger2c.astwindow import ASTWindow


PYTHON = '/usr/bin/python'
DOT = '/usr/bin/dot'

SRC_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
PYTIGER2C = os.path.join(SRC_DIR, 'scripts', 'pytiger2c.py')
PYTIGER2C_EXIT_SUCCESS, PYTIGER2C_EXIT_FAILURE = 0, 1


class MainWindow(XMLWidget):
    
    def __init__(self, data_dir, pytiger2c_script):
        super(MainWindow, self).__init__(data_dir, 'main_window')
        self._filename = None
        self._init_filenames()
        self._data_dir = data_dir
        self._init_accelerators()
        self._init_source_view()
        self._init_output_view()
        self._init_errors_view()
        self._source_view.grab_focus()
        self._widget.show_all()
        self.on_new()

    def _init_accelerators(self):
        accel_group = gtk.AccelGroup()
        self._widget.add_accel_group(accel_group)
        # File menu.
        menu_item = self._builder.get_object('new_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('N'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_item = self._builder.get_object('open_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('O'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_item = self._builder.get_object('save_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('S'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_item = self._builder.get_object('saveas_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('S'), 
                                  gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK, gtk.ACCEL_VISIBLE)
        menu_item = self._builder.get_object('quit_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('Q'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        # Edit menu.
        menu_item = self._builder.get_object('undo_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('Z'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_item = self._builder.get_object('redo_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('Z'), 
                                  gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK, gtk.ACCEL_VISIBLE)
        menu_item = self._builder.get_object('cut_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('X'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_item = self._builder.get_object('copy_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('C'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_item = self._builder.get_object('paste_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('V'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        # Project menu.
        menu_item = self._builder.get_object('build_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('B'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_item = self._builder.get_object('run_menuitem')
        menu_item.add_accelerator('activate', accel_group, ord('R'), 
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        
    def _init_source_view(self):
        # Creating the buffer.
        self._source_buffer = gtksourceview.Buffer()
        self._source_buffer.connect('changed', self.on_source_buffer_changed)
        self._source_buffer.connect('modified-changed', self.on_source_buffer_modified_changed)
        self._source_buffer.set_highlight_matching_brackets(True)
        manager = gtksourceview.LanguageManager()
        manager.set_search_path([os.path.join(self._data_dir, 'gtksourceview')])
        language = manager.get_language('tiger')
        self._source_buffer.set_language(language)
        self._source_buffer.set_highlight_syntax(True)
        self._update_undo_redo()
        # Creating the viewer.
        self._source_view = gtksourceview.View(self._source_buffer)
        self._source_view.modify_font(pango.FontDescription('monospace'))
        self._source_view.set_show_line_numbers(True)
        self._source_view.set_show_line_marks(False)
        self._source_view.set_show_right_margin(False)
        self._source_view.set_insert_spaces_instead_of_tabs(False)
        self._source_view.set_highlight_current_line(True)
        self._source_view.set_auto_indent(True)
        # Add the source view to the window.
        scrolledwindow = self._builder.get_object('source_scrolledwindow')
        scrolledwindow.add(self._source_view)
        
    def _init_errors_view(self):
        self._errors_buffer = gtk.TextBuffer()
        errors_view = self._builder.get_object('errors_textview')
        errors_view.set_buffer(self._errors_buffer)
        errors_view.modify_font(pango.FontDescription('monospace'))
        
    def _init_output_view(self):
        self._output_buffer = gtk.TextBuffer()
        output_view = self._builder.get_object('output_textview')
        output_view.set_buffer(self._output_buffer)
        output_view.modify_font(pango.FontDescription('monospace'))
        
    def _init_filenames(self):
        if self._filename is not None:
            last_dot = self._filename.rfind('.')
            if len(self._filename) - last_dot <= 6:
                prefix = self._filename[:last_dot]
            else:
                prefix = self._filename
            self._c_filename = prefix + '.c'
            self._bin_filename = prefix + '.bin'
            self._dot_filename = prefix + '.dot'
            self._jpg_filename = prefix + '.jpg'
        else:
            self._c_filename = None
            self._bin_filename = None
            self._dot_filename = None
            self._jpg_filename = None            
        
    def on_quit(self):
        self._losing_changes()
        return False
        
    def on_main_window_destroy(self, widget=None):
        gtk.main_quit()
        
    def on_main_window_delete_event(self, widget, event):
        return self.on_quit()
        
    def on_about_menuitem_activate(self, widget=None):
        dialog = AboutDialog(self._data_dir)
        dialog.run()
        dialog.destroy()

    def on_quit_menuitem_activate(self, widget=None):
        if not self.on_quit():
            self._widget.destroy()
            
    def on_source_buffer_undo(self, widget=None):
        if self._source_buffer.can_undo():
            self._source_buffer.undo()
            self._update_undo_redo()
        
    def on_source_buffer_redo(self, widget=None):
        if self._source_buffer.can_redo():
            self._source_buffer.redo()
            self._update_undo_redo()
            
    def on_source_buffer_changed(self, widget=None):
        self._update_undo_redo()
        
    def on_source_buffer_modified_changed(self, widget=None):
        if self._filename is None:
            self._widget.set_title('*Unsaved file - PyTiger2C')
        elif self._source_buffer.get_modified():
            self._widget.set_title('*%s - PyTiger2C' % os.path.basename(self._filename))
        else:
            self._widget.set_title('%s - PyTiger2C' % os.path.basename(self._filename))
        
    def on_cut_menuitem_activate(self, widget=None):
        clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
        self._source_buffer.cut_clipboard(clipboard, self._source_view.get_editable())
        
    def on_copy_menuitem_activate(self, widget=None):
        clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
        self._source_buffer.copy_clipboard(clipboard)
        
    def on_paste_menuitem_activate(self, widget=None):
        clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
        self._source_buffer.paste_clipboard(clipboard, None, self._source_view.get_editable())
        
    def on_code_menuitem_activate(self, widget=None):
        if not (self._filename is None or self._source_buffer.get_modified()):
            pytiger2c_cmd = [PYTHON, PYTIGER2C, self._filename, '-t', 'c', '-o', self._c_filename]
            pytiger2c_process = subprocess.Popen(pytiger2c_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pytiger2c_ret = pytiger2c_process.wait()
            if pytiger2c_ret == PYTIGER2C_EXIT_SUCCESS:
                code_window = CodeWindow(self._data_dir, self._c_filename)
                code_window.show()
            else:
                self._error_dialog('Build error', 'The program has errors.')
        else:
            self._error_dialog('Build error', 'File is not saved.')
    
    def on_ast_menuitem_activate(self, widget=None):
        if not (self._filename is None or self._source_buffer.get_modified()):
            pytiger2c_cmd = [PYTHON, PYTIGER2C, self._filename, '-t', 'ast', '-o', self._dot_filename]
            pytiger2c_process = subprocess.Popen(pytiger2c_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pytiger2c_ret = pytiger2c_process.wait()
            if pytiger2c_ret == PYTIGER2C_EXIT_SUCCESS:
                dot_cmd = [DOT, '-Tjpg', self._dot_filename, '-o', self._jpg_filename]
                dot_process = subprocess.Popen(dot_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                dot_ret = dot_process.wait()
                ast_window = ASTWindow(self._data_dir, self._jpg_filename)
                ast_window.show()
            else:
                self._error_dialog('Build error', 'The program has errors.')
        else:
            self._error_dialog('Build error', 'File is not saved.')
    
    def on_build(self, widget=None):
        if not (self._filename is None or self._source_buffer.get_modified()):
            self._builder.get_object('notebook').set_current_page(1)
            self._errors_buffer.set_text('')
            pytiger2c_cmd = [PYTHON, PYTIGER2C, self._filename, '-o', self._bin_filename]
            pytiger2c_process = subprocess.Popen(pytiger2c_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pytiger2c_ret = pytiger2c_process.wait()
            if pytiger2c_ret == PYTIGER2C_EXIT_SUCCESS:
                self._errors_buffer.set_text('Build succeeded.')
                success = True
            else:
                self._errors_buffer.set_text(pytiger2c_process.stderr.read())
                success = False
        else:
            self._error_dialog('Build error', 'File is not saved.')
            success = False
        return success
    
    def on_run(self, widget=None):
        build_success = self.on_build()
        if build_success:
            self._output_buffer.set_text('')
            self._builder.get_object('notebook').set_current_page(0)
            if self._filename is not None and os.path.isfile(self._bin_filename):
                program_cmd = [self._bin_filename]
                program_process = subprocess.Popen(program_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                program_process.wait()
                self._output_buffer.set_text(program_process.stderr.read() + program_process.stdout.read())
    
    def on_new(self, widget=None):
        self._losing_changes()
        self._filename = None
        self._source_buffer.set_text('')
        self._source_buffer.set_modified(False)
        if self._source_buffer.can_undo():
                self._source_buffer.begin_not_undoable_action()
                self._source_buffer.end_not_undoable_action()
    
    def on_open(self, widget=None):
        chooser = gtk.FileChooserDialog(title='Open...', parent=self._widget, 
                                        action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                 gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        response = chooser.run()        
        if response == gtk.RESPONSE_OK:
            self._filename = os.path.abspath(chooser.get_filename())
            self._load_source_buffer()
        chooser.destroy()
    
    def on_save(self, widget=None):
        if self._filename is None:
            self.on_saveas()
        else:
            self._save_source_buffer()
    
    def on_saveas(self, widget=None):
        chooser = gtk.FileChooserDialog(title='Save as...', parent=self._widget, 
                                        action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                 gtk.STOCK_SAVE_AS, gtk.RESPONSE_OK))
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self._filename = os.path.abspath(chooser.get_filename())
            self._save_source_buffer()
            self._load_source_buffer()
        chooser.destroy()
        
    def _update_undo_redo(self):
        menubar_undo = self._builder.get_object('undo_menuitem')
        toolbar_undo = self._builder.get_object('undo_toolbutton')
        menubar_redo = self._builder.get_object('redo_menuitem')
        toolbar_redo = self._builder.get_object('redo_toolbutton')
        can_undo = self._source_buffer.can_undo()
        menubar_undo.set_sensitive(can_undo)
        toolbar_undo.set_sensitive(can_undo)
        can_redo = self._source_buffer.can_redo()
        menubar_redo.set_sensitive(can_redo)
        toolbar_redo.set_sensitive(can_redo)
        
    def _load_source_buffer(self):
        try:
            with open(self._filename) as fd:
                text = fd.read()
        except:
            self._error_dialog('Error opening the file', 'Could not open the file.')
        else:
            self._init_filenames()
            self._source_buffer.set_text(text)
            self._source_buffer.set_modified(False)
            self._source_buffer.place_cursor(self._source_buffer.get_start_iter())
            if self._source_buffer.can_undo():
                self._source_buffer.begin_not_undoable_action()
                self._source_buffer.end_not_undoable_action()
            
    def _save_source_buffer(self):
        text = self._source_buffer.get_text(*self._source_buffer.get_bounds())
        try:
            with open(self._filename, 'w') as fd:
                fd.write(text)
        except:
            self._error_dialog('Error saving the file', 'Could not save the file.')
        else:
            self._source_buffer.set_modified(False)
            
    def _losing_changes(self):
        if self._source_buffer.get_modified():
            dialog = gtk.MessageDialog(parent=self._widget, type=gtk.MESSAGE_QUESTION,
                                       flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       buttons=gtk.BUTTONS_YES_NO)
            dialog.set_property('text', "Save changes?")
            dialog.set_property('secondary-text', "If you don't save, changes will be permanently lost.")
            response = dialog.run()
            if response == gtk.RESPONSE_YES:
                self.on_save()
            dialog.destroy()            
            
    def _error_dialog(self, text, secondary_text):        
        dialog = gtk.MessageDialog(parent=self._widget, type=gtk.MESSAGE_ERROR,
                                   flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   buttons=gtk.BUTTONS_CLOSE)
        dialog.set_property('text', text)
        dialog.set_property('secondary-text', secondary_text)
        dialog.run()
        dialog.destroy()
