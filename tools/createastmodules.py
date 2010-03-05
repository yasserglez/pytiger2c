# -*- coding: utf-8 -*-

"""
Genera los módulos con las declaraciones de las clases de los nodos del AST a
partir del grafo de la jerarquía de las clases del AST en formato DOT de Graphviz.
"""

import os
import sys
import re


EXIT_SUCCESS, EXIT_FAILURE = 0, 1


def create_ast_modules(dot_file, output_dir):
    nodes = _parse_dot_file(dot_file)
    for parent_class, node_class in nodes:
        _create_node_module(output_dir, node_class, parent_class)
    _create_init_module(output_dir, [node_class for parent_class, node_class in nodes])
    

def _parse_dot_file(dot_file):
    node_re = re.compile(r'^(?P<parent_class>[A-Za-z0-9_]+)\s+--\s+(?P<node_class>[A-Za-z0-9_]+);$')
    nodes = []
    with open(dot_file, 'r') as fd:
        for line in fd.xreadlines():
            line = line.strip()
            # Check for the beginning of a state declaration.
            node_match = node_re.match(line)
            if node_match:
                node_classes = (node_match.group('parent_class'), node_match.group('node_class'))
                nodes.append(node_classes)
    return nodes


def _create_node_module(output_dir, node_class, parent_class):
    module_file = os.path.join(output_dir, node_class.lower() + '.py')
    module_content = _MODULE_TEMPLATE.format(parent_module=parent_class.lower(),
                                             parent_class=parent_class,
                                             node_class=node_class)
    with open(module_file, 'w') as fd:
        fd.write(module_content)
        fd.write('\n')


def _create_init_module(output_dir, node_classes):
    init_file  = os.path.join(output_dir, '__init__.py')
    IMPORT = 'from pytiger2c.ast.{module} import {node_class}'
    imports = '\n'.join([IMPORT.format(module=node_class.lower(), node_class=node_class) for node_class in node_classes])
    classes = '\n'.join(["'{class_name}',".format(class_name=class_name) for class_name in node_classes])
    init_content = _INIT_TEMPLATE.format(class_import=imports, class_list=classes)
    with open(init_file, 'w') as fd:
        fd.write(init_content)
        fd.write('\n')    
    

_INIT_TEMPLATE = \
"""
# -*- coding: utf-8 -*-

{class_import}

__all__ = [
{class_list}
]
""".lstrip()


_MODULE_TEMPLATE = \
"""
# -*- coding: utf-8 -*-

\"\"\"
Clase {node_class} del árbol de sintáxis abstracta.
\"\"\"

from pytiger2c.ast.{parent_module} import {parent_class}


class {node_class}({parent_class}):
    \"\"\"
    Clase {node_class} del árbol de sintáxis abstracta.
    \"\"\"
    
    def __init__(self):
        \"\"\"
        Inicializa la clase {node_class}.
        \"\"\"
        super({node_class}, self).__init__()
""".lstrip()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        dot_file = os.path.abspath(sys.argv[1])
        output_dir = os.path.abspath(sys.argv[2])
        create_ast_modules(dot_file, output_dir)
        sys.exit(EXIT_SUCCESS)
    else:
        print >> sys.stderr, 'Usage: {prog} <dot-file> <output-dir>'.format(prog=os.path.basename(sys.argv[0]))
        sys.exit(EXIT_FAILURE)
