# -*- coding: utf-8 -*-

"""
Script para resaltar la sintaxis en fragmentos de código C y Tiger.
"""

import os
import sys
import codecs

from pygments import highlight
from pygments.token import *
from pygments.lexer import RegexLexer
from pygments.lexers.compiled import CLexer
from pygments.formatters import LatexFormatter


class TigerLexer(RegexLexer):
    """Pygments lexer for the Tiger language.
    """
    
    name = 'Tiger'
    aliases = ['tiger']
    filenames = ['*.tiger', '*.tig']
    
    tokens = {
        'root': [
            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text),
            (r'/\*', Comment.Multiline, 'comment'),
            (r'[,:;()\[\]{}.+\-*/=<>&|]', Punctuation),
            (r'\d+', Number.Integer),
            (r'L?"', String, 'string'),
            (r'(int|string|nil)\b', Keyword.Type),
            (r'(array|break|do|else|end|for|function|if|in|let|of|then|to|type|var|while)\b', Keyword),
            ('[a-zA-Z_][a-zA-Z0-9_]*', Name),
        ],
        'comment': [
            (r'[^*/]', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline)
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),
            (r'\\\n', String),
            (r'\\', String),
        ],        
    }


def main():
    """
    Función principal del script.
    """
    if len(sys.argv) != 2:
        print 'Usage: {0} <input-file>'.format(os.path.basename(sys.argv[0]))
    else:
        input_file = os.path.abspath(sys.argv[1])
        if input_file.endswith('.c') or input_file.endswith('.h'):
            lexer = CLexer()
        elif input_file.endswith('.tiger') or input_file.endswith('.tig'):
            lexer = TigerLexer()
        else:
            print 'Error: Invalid input file. Only C and Tiger programs accepted.'
            sys.exit()
        dot_index = - len(input_file) + input_file.rfind('.')
        output_file = '%s.tex' % input_file[:dot_index]
        with codecs.open(input_file, encoding='utf-8') as input:
            with codecs.open(output_file, mode='w', encoding='utf-8') as output:
                highlight(input.read(), lexer, LatexFormatter(), output)


if __name__ == '__main__':
    main()