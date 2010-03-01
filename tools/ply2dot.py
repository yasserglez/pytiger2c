# -*- coding: utf-8 -*-

"""
Genera un autómata LR en formato DOT de Graphviz a partir de un archivo de debug de PLY.
"""

import os
import sys
import re


EXIT_SUCCESS, EXIT_FAILURE = 0, 1


def ply2dot(ply_file, dot_file):
    prods, shifts = _parse_ply_file(ply_file)
    _write_dot_file(dot_file, prods, shifts)


def _parse_ply_file(ply_file):
    state_re = re.compile(r'^state\s(?P<number>\d+)$')
    prod_re = re.compile(r'^\(\d+\)\s(?P<production>.*?->.*?)$')
    shift_re = re.compile(r'^(?P<input_item>\S+)\s+shift\sand\sgo\sto\sstate\s(?P<goto_state>\d+)$')
    prods, shifts = {}, {}
    current_state = -1
    with open(ply_file, 'r') as fd:
        for line in fd.xreadlines():
            line = line.strip()
            # Check for the beginning of a state declaration.
            state_match = state_re.match(line)
            if state_match:
                current_state = int(state_match.group('number'))
                prods[current_state] = []
                shifts[current_state] = {} 
                continue
            # Load information of the states.
            if current_state >= 0:
                prod_match = prod_re.match(line)
                if prod_match:
                    prod = prod_match.group('production')
                    prods[current_state].append(prod)
                shift_match = shift_re.match(line)
                if shift_match:
                    input_item = shift_match.group('input_item')
                    goto_state = int(shift_match.group('goto_state'))
                    shifts[current_state][input_item] = goto_state
                    continue
                # Ignore the line if it is not the beginning of a state, a production or shift information.
    return prods, shifts


def _write_dot_file(dot_file, prods, shifts):
    nodes_list = []
    trans_list = []
    for state in prods.iterkeys():
        state_label = r'\n'.join(prods[state])
        nodes_list.append(_NODE_TEMPLATE.format(number=state, label=state_label))
        for input_item, goto_state in shifts[state].iteritems():
            trans_list.append(_TRANS_TEMPLATE.format(origin=state, destination=goto_state, label=input_item))
    indent = ' ' * 4
    nodes = indent + ('\n' + indent).join(nodes_list)
    trans = indent + ('\n' + indent).join(trans_list)
    dot_content = _DOT_TEMPLATE.format(nodes=nodes, trans=trans)
    with open(dot_file, 'w') as fd:
        fd.write(dot_content)    


_NODE_TEMPLATE = 'state{number} [label="{label}"];'

_TRANS_TEMPLATE = 'state{origin} -> state{destination} [label="{label}"];'

_DOT_TEMPLATE = """digraph LRAutomata {{
    rankdir="LR";
    node [fontname="monospace",fontsize="10"];
    edge [fontname="monospace",fontsize="10"];

{nodes}

{trans}
}}
"""


if __name__ == '__main__':
    if len(sys.argv) == 3:
        ply_file = os.path.abspath(sys.argv[1])
        dot_file = os.path.abspath(sys.argv[2])
        ply2dot(ply_file, dot_file)
        sys.exit(EXIT_SUCCESS)
    else:
        print >> sys.stderr, 'Usage: {prog} <ply-file> <dot-file>'.format(prog=os.path.basename(sys.argv[0]))
        sys.exit(EXIT_FAILURE)
