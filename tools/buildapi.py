# -*- coding: utf-8 -*-

"""Script para generar documentación del API.
"""

import os
import sys
import shutil
import textwrap
import subprocess

from epydoc import cli, log
from epydoc.util import plaintext_to_latex
from epydoc.docwriter.latex import LatexWriter
from epydoc.apidoc import *


SRC_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

DOCS_DIR = os.path.abspath(os.path.join(SRC_DIR, 'docs'))

OUTPUT_DIR = os.path.abspath(os.path.join(DOCS_DIR, 'api'))

EPYDOC_CONF = os.path.abspath(os.path.join(SRC_DIR, 'tools', 'epydoc.conf'))

TIGER2C_PACKAGE = os.path.abspath(os.path.join(SRC_DIR, 'packages', 'tiger2c'))

EPYDOC_CMD = ['epydoc', '--debug', '--conf', EPYDOC_CONF, '-o', OUTPUT_DIR, TIGER2C_PACKAGE]

LATEX_CMD = ['pdflatex', os.path.join(OUTPUT_DIR, 'api.tex')]


class Tiger2CLatexWriter(LatexWriter):
    """LatexWriter personalizado para generar documentación de Tiger2C.
    """

    PREAMBLE = [
        "\\documentclass{article}",
        "\\usepackage{alltt, parskip, fancyhdr, boxedminipage}",
        "\\usepackage{makeidx, multirow, longtable, tocbibind, amssymb}",
        "\\usepackage{fullpage}",
        "\\usepackage[usenames]{color}",
        "\\usepackage[spanish]{babel}",
        # By default, do not indent paragraphs.
        "\\setlength{\\parindent}{0ex}",
        "\\setlength{\\parskip}{2ex}",
        # Double the standard size boxedminipage outlines.
        "\\setlength{\\fboxrule}{2\\fboxrule}",
        # Create a 'base class' length named BCL for use in base trees.
        "\\newlength{\\BCL} % base class length, for base trees.",
        # Colorization for python source code
        "\\definecolor{py@keywordcolour}{rgb}{1,0.45882,0}",
        "\\definecolor{py@stringcolour}{rgb}{0,0.666666,0}",
        "\\definecolor{py@commentcolour}{rgb}{1,0,0}",
        "\\definecolor{py@ps1colour}{rgb}{0.60784,0,0}",
        "\\definecolor{py@ps2colour}{rgb}{0.60784,0,1}",
        "\\definecolor{py@inputcolour}{rgb}{0,0,0}",
        "\\definecolor{py@outputcolour}{rgb}{0,0,1}",
        "\\definecolor{py@exceptcolour}{rgb}{1,0,0}",
        "\\definecolor{py@defnamecolour}{rgb}{1,0.5,0.5}",
        "\\definecolor{py@builtincolour}{rgb}{0.58039,0,0.58039}",
        "\\definecolor{py@identifiercolour}{rgb}{0,0,0}",
        "\\definecolor{py@linenumcolour}{rgb}{0.4,0.4,0.4}",
        "\\definecolor{py@inputcolour}{rgb}{0,0,0}",
        "% Prompt",
        "\\newcommand{\\pysrcprompt}[1]{\\textcolor{py@ps1colour}"
            "{\\small\\textbf{#1}}}",
        "\\newcommand{\\pysrcmore}[1]{\\textcolor{py@ps2colour}"
            "{\\small\\textbf{#1}}}",
        "% Source code",
        "\\newcommand{\\pysrckeyword}[1]{\\textcolor{py@keywordcolour}"
            "{\\small\\textbf{#1}}}",
        "\\newcommand{\\pysrcbuiltin}[1]{\\textcolor{py@builtincolour}"
            "{\\small\\textbf{#1}}}",
        "\\newcommand{\\pysrcstring}[1]{\\textcolor{py@stringcolour}"
            "{\\small\\textbf{#1}}}",
        "\\newcommand{\\pysrcdefname}[1]{\\textcolor{py@defnamecolour}"
            "{\\small\\textbf{#1}}}",
        "\\newcommand{\\pysrcother}[1]{\\small\\textbf{#1}}",
        "% Comments",
        "\\newcommand{\\pysrccomment}[1]{\\textcolor{py@commentcolour}"
            "{\\small\\textbf{#1}}}",
        "% Output",
        "\\newcommand{\\pysrcoutput}[1]{\\textcolor{py@outputcolour}"
            "{\\small\\textbf{#1}}}",
        "% Exceptions",
        "\\newcommand{\\pysrcexcept}[1]{\\textcolor{py@exceptcolour}"
            "{\\small\\textbf{#1}}}",
        # Size of the function description boxes.
        "\\newlength{\\funcindent}",
        "\\newlength{\\funcwidth}",
        "\\setlength{\\funcindent}{1cm}",
        "\\setlength{\\funcwidth}{\\textwidth}",
        "\\addtolength{\\funcwidth}{-2\\funcindent}",
        # Size of the var description tables.
        "\\newlength{\\varindent}",
        "\\newlength{\\varnamewidth}",
        "\\newlength{\\vardescrwidth}",
        "\\newlength{\\varwidth}",
        "\\setlength{\\varindent}{1cm}",
        "\\setlength{\\varnamewidth}{.3\\textwidth}",
        "\\setlength{\\varwidth}{\\textwidth}",
        "\\addtolength{\\varwidth}{-4\\tabcolsep}",
        "\\addtolength{\\varwidth}{-3\\arrayrulewidth}",
        "\\addtolength{\\varwidth}{-2\\varindent}",
        "\\setlength{\\vardescrwidth}{\\varwidth}",
        "\\addtolength{\\vardescrwidth}{-\\varnamewidth}",
        # Define new environment for displaying parameter lists.
        textwrap.dedent("""\
        \\newenvironment{Ventry}[1]%
         {\\begin{list}{}{%
           \\renewcommand{\\makelabel}[1]{\\texttt{##1:}\\hfil}%
           \\settowidth{\\labelwidth}{\\texttt{#1:}}%
           \\setlength{\\leftmargin}{\\labelsep}%
           \\addtolength{\\leftmargin}{\\labelwidth}}}%
         {\\end{list}}"""),
        ]
    
    def write_topfile(self, out):
        self.write_header(out, 'Include File')
        self.write_preamble(out)
        out('\n\\begin{document}\n')
        self.write_start_of(out, 'Header')
        # Write the title.
        self.write_start_of(out, 'Title')
        out('\\title{\LARGE{Tiger2C} \\\\ \\Large{Documentación del API}}\n')
        out('\\author{\n')
        out('Yasser González Fernández \\\\ \\small{yglez@uh.cu}\n\\and\n')
        out('Ariel Hernández Amador \\\\ \\small{gnuaha7@uh.cu}\n}\n')
        out('\\date{}\n')        
        out('\\maketitle\n')
        # Add a table of contents.
        self.write_start_of(out, 'Table of Contents')
        out('\\newpage\n')
        out('\\tableofcontents\n')
        # Include documentation files.
        self.write_start_of(out, 'Includes')
        for val_doc in self.valdocs:
            if isinstance(val_doc, ModuleDoc):
                out('\\include{%s-module}\n' % val_doc.canonical_name)
        # Add the index, if requested.
        if self._index:
            self.write_start_of(out, 'Index')
            out('\\printindex\n\n')
        # Add the footer.
        self.write_start_of(out, 'Footer')
        out('\\end{document}\n')

    def write_module(self, out, doc):
        self.write_header(out, doc)
        self.write_start_of(out, 'Module Description')
        # Add this module to the index.
        out(self.indexterm(doc, 'start'))
        # Add a section marker.
        out(self.section('%s %s' % (self.doc_kind(doc), doc.canonical_name)))
        # Label our current location.
        out('\\label{%s}\n' % self.label(doc))
        # Add the module's description.
        if doc.descr not in (None, UNKNOWN):
            out(self.docstring_to_latex(doc.descr))
        # If it's a package, list the sub-modules.
        if doc.submodules != UNKNOWN and doc.submodules:
            self.write_module_list(out, doc)
        # Contents.
        if self._list_classes_separately:
            self.write_class_list(out, doc)
        self.write_func_list(out, 'Funciones', doc, 'function')
        self.write_var_list(out, 'Variables', doc, 'other')
        # Class list.
        if not self._list_classes_separately:
            classes = doc.select_variables(imported=False, value_type='class',
                                           public=self._public_filter)
            for var_doc in classes:
                self.write_class(out, var_doc.value)
        # Mark the end of the module (for the index)
        out(self.indexterm(doc, 'end'))
        
    def write_module_list(self, out, doc):
        if len(doc.submodules) == 0: return
        self.write_start_of(out, 'Modules')
        
        out(self.section('Módulos', 1))
        out('\\begin{itemize}\n')
        for group_name in doc.group_names():
            if not doc.submodule_groups[group_name]: continue
            if group_name:
                out('\\item \\textbf{%s}\n' % group_name)
                out('\\begin{itemize}\n')
            for submodule in doc.submodule_groups[group_name]:
                self.write_module_tree_item(out, submodule)
            if group_name:
                out('\end{itemize}\n')
        out('\\end{itemize}\n\n')        

    def write_module_tree_item(self, out, doc, depth=0):
        out(' ' * depth + '\\item \\textbf{')
        out(plaintext_to_latex(doc.canonical_name[-1]) +'}')
        if doc.summary not in (None, UNKNOWN):
            out(': %s\n' % self.docstring_to_latex(doc.summary))
        if self._crossref:
            out('\n  \\textit{(Sección~\\ref{%s}' % self.label(doc))
            out(', página~\\pageref{%s})}\n\n' % self.label(doc))
        if doc.submodules != UNKNOWN and doc.submodules:
            out(' ' * depth + '  \\begin{itemize}\n')
            for submodule in doc.submodules:
                self.write_module_tree_item(out, submodule, depth+4)
            out(' ' * depth + '  \\end{itemize}\n')     
               
    def write_class(self, out, doc):
        if self._list_classes_separately:
            self.write_header(out, doc)
        self.write_start_of(out, 'Class Description')
        # Add this class to the index.
        out(self.indexterm(doc, 'start'))
        # Add a section marker.
        if self._list_classes_separately:
            seclevel = 0
            out(self.section('%s %s' % (self.doc_kind(doc),
                                        doc.canonical_name), seclevel))
        else:
            seclevel = 1
            out(self.section('%s %s' % (self.doc_kind(doc),
                                        doc.canonical_name[-1]), seclevel))
        # Label our current location.
        out('\\label{%s}\n' % self.label(doc))
        # Add our base list.
        if doc.bases not in (UNKNOWN, None) and len(doc.bases) > 0:
            out(self.base_tree(doc))
        # The class's known subclasses
        if doc.subclasses not in (UNKNOWN, None) and len(doc.subclasses) > 0:
            sc_items = [plaintext_to_latex('%s' % sc.canonical_name)
                        for sc in doc.subclasses]
            out(self._descrlist(sc_items, 'Clases descendientes', short=1))
        # The class's description.
        if doc.descr not in (None, UNKNOWN):
            out(self.docstring_to_latex(doc.descr))
        # Version, author, warnings, requirements, notes, etc.
        self.write_standard_fields(out, doc)
        # Contents.
        self.write_func_list(out, 'Métodos', doc, 'method', seclevel + 1)
        self.write_var_list(out, 'Propiedades', doc, 'property', seclevel + 1)
        self.write_var_list(out, 'Variables de clase', doc, 'classvariable', seclevel+1)
        self.write_var_list(out, 'Variables de instancia', doc, 'instancevariable', seclevel+1)
        # Mark the end of the class (for the index)
        out(self.indexterm(doc, 'end'))
        
    # Also used for the property list.
    def write_var_list(self, out, heading, doc, value_type, seclevel=1):
        groups = [(plaintext_to_latex(group_name),
                   doc.select_variables(group=group_name, imported=False,
                                        value_type=value_type,
                                        public=self._public_filter))
                  for group_name in doc.group_names()]
        # Discard any empty groups; and return if they're all empty.
        groups = [(g,vars) for (g,vars) in groups if vars]
        if not groups: return
        # Write a header.
        self.write_start_of(out, heading)
        out('  '+self.section(heading, seclevel))
        # [xx] without this, there's a huge gap before the table -- why??
        out('\\vspace{-1cm}\n')
        out('\\hspace{\\varindent}')
        out('\\begin{longtable}')
        out('{|p{\\varnamewidth}|')
        out('p{\\vardescrwidth}|l}\n')
        out('\\cline{1-2}\n')
        # Set up the headers & footer (this makes the table span
        # multiple pages in a happy way).
        out('\\cline{1-2} ')
        out('\\centering \\textbf{Nombre} & ')
        out('\\centering \\textbf{Descripción}& \\\\\n')
        out('\\cline{1-2}\n')
        out('\\endhead')
        out('\\cline{1-2}')
        out('\\multicolumn{3}{r}{\\small\\textit{')
        out('continúa en la página siguiente}}\\\\')
        out('\\endfoot')
        out('\\cline{1-2}\n')
        out('\\endlastfoot')
        # Write a section for each group.
        grouped_inh_vars = {}
        for name, var_docs in groups:
            self.write_var_group(out, doc, name, var_docs, grouped_inh_vars)
        # Write a section for each inheritance pseudo-group.
        if grouped_inh_vars:
            for base in doc.mro():
                if base in grouped_inh_vars:
                    hdr = ('Heredadas de %s' %
                           plaintext_to_latex('%s' % base.canonical_name))
                    if self._crossref and base in self.class_set:
                        hdr += (' \\textit{(Section \\ref{%s})}' %
                                self.label(base))
                    out(self._VAR_GROUP_HEADER % (hdr))
                    out('\\cline{1-2}\n')
                    for var_doc in grouped_inh_vars[base]:
                        if isinstance(var_doc.value3, PropertyDoc):
                            self.write_property_list_line(out, var_doc)
                        else:
                            self.write_var_list_line(out, var_doc)
        out('\\end{longtable}\n\n')        
        
    def write_func_list(self, out, heading, doc, value_type, seclevel=1):
        # Divide all public variables of the given type into groups.
        groups = [(plaintext_to_latex(group_name),
                   doc.select_variables(group=group_name, imported=False,
                                        value_type=value_type,
                                        public=self._public_filter))
                  for group_name in doc.group_names()]
        # Discard any empty groups; and return if they're all empty.
        groups = [(g,vars) for (g,vars) in groups if vars]
        if not groups: return
        # Write a header.
        self.write_start_of(out, heading)
        out(self.section(heading, seclevel))
        # Write a section for each group.
        grouped_inh_vars = {}
        for name, var_docs in groups:
            self.write_func_group(out, doc, name, var_docs, grouped_inh_vars)
        # Write a section for each inheritance pseudo-group.
        if grouped_inh_vars:
            for base in doc.mro():
                if base in grouped_inh_vars:
                    hdr = ('Heredadas de  %s' %
                           plaintext_to_latex('%s' % base.canonical_name))
                    if self._crossref and base in self.class_set:
                        hdr += ('\\textit{(Sección \\ref{%s})}' %
                                self.label(base))
                    out(self._FUNC_GROUP_HEADER % (hdr))
                    for var_doc in grouped_inh_vars[base]:
                        self.write_func_list_box(out, var_doc)        
                        
    def write_func_inheritance_list(self, out, doc, listed_inh_vars):
        for base in doc.mro():
            if base not in listed_inh_vars: continue
            #if str(base.canonical_name) == 'object': continue
            var_docs = listed_inh_vars[base]
            if self._public_filter:
                var_docs = [v for v in var_docs if v.is_public]
            if var_docs:
                hdr = ('Heredados de %s' %
                       plaintext_to_latex('%s' % base.canonical_name))
                if self._crossref and base in self.class_set:
                    hdr += ('\\textit{(Section \\ref{%s})}' %
                            self.label(base))
                out(self._FUNC_GROUP_HEADER % hdr)
                out('\\begin{quote}\n')
                out('%s\n' % ', '.join(
                    ['%s()' % plaintext_to_latex(var_doc.name)
                     for var_doc in var_docs]))
                out('\\end{quote}\n')         
                               
    def write_var_inheritance_list(self, out, doc, listed_inh_vars):
        for base in doc.mro():
            if base not in listed_inh_vars: continue
            #if str(base.canonical_name) == 'object': continue
            var_docs = listed_inh_vars[base]
            if self._public_filter:
                var_docs = [v for v in var_docs if v.is_public]
            if var_docs:
                hdr = ('Heredadas de %s' %
                       plaintext_to_latex('%s' % base.canonical_name))
                if self._crossref and base in self.class_set:
                    hdr += (' \\textit{(Section \\ref{%s})}' %
                            self.label(base))
                out(self._VAR_GROUP_HEADER % hdr)
                out('\\multicolumn{2}{|p{\\varwidth}|}{'
                    '\\raggedright %s}\\\\\n' %
                    ', '.join(['%s' % plaintext_to_latex(var_doc.name)
                               for var_doc in var_docs]))
                out('\\cline{1-2}\n')                               
        
    def doc_kind(self, doc):
        if isinstance(doc, ModuleDoc) and doc.is_package == True:
            return 'Paquete'
        elif (isinstance(doc, ModuleDoc) and
              doc.canonical_name[0].startswith('script')):
            return 'Script'
        elif isinstance(doc, ModuleDoc):
            return 'Módulo'
        elif isinstance(doc, ClassDoc):
            return 'Clase'
        elif isinstance(doc, ClassMethodDoc):
            return 'Método de clase'
        elif isinstance(doc, StaticMethodDoc):
            return 'Método estático'
        elif isinstance(doc, RoutineDoc):
            if isinstance(self.docindex.container(doc), ClassDoc):
                return 'Método'
            else:
                return 'Función'
        else:
            return 'Variable'             
        
        
def write_latex(docindex, options, format):
    """Sustituye la función de igual nombre de Epydoc.
    
    Esta función se utiliza para sustituir la función de igual nombre de Epydoc
    que se encuentra en el módulo cli. Es una forma (bastante pobre) de
    personalizar el código LaTeX generado por Epydoc.
    """
    latex_writer = Tiger2CLatexWriter(docindex, **options.__dict__)
    log.start_progress('Writing LaTeX docs')
    latex_writer.write(options.target)
    log.end_progress()
    # It is incomplete becouse we only want to generato LaTex output.        

    
def main():
    """Función principal del script.
    """
    # Generate the documentation of the package using Epydoc.
    cli.write_latex = write_latex
    sys.argv = EPYDOC_CMD
    cli.cli()
    # Generate the PDF document.
    os.chdir(OUTPUT_DIR)
    for i in xrange(2):
        subprocess.call(LATEX_CMD)
    # Cleanup and move the PDF to the docs directory.
    pdf_file = os.path.join(DOCS_DIR, 'api.pdf')
    if os.path.isfile(pdf_file):
        os.remove(pdf_file)
    shutil.move(os.path.join(OUTPUT_DIR, 'api.pdf'), DOCS_DIR)
    shutil.rmtree(OUTPUT_DIR)

    
if __name__ == '__main__':
    main()
