# -*- coding: utf-8 -*-

"""
Genera la tabla LR en formato LaTeX a partir de un archivo de debug de PLY.
"""

import os
import sys
import re


EXIT_SUCCESS, EXIT_FAILURE = 0, 1


def ply2lrtable(ply_file, table_file):
    action, goto = _parse_ply_file(ply_file)
    _write_table_file(table_file, action, goto)


def _parse_ply_file(ply_file):
    state_re = re.compile(r'^state\s(?P<number>\d+)$')
    reduce_re = re.compile(r'^(?P<input_item>\S+)\s+reduce\susing\srule\s(?P<rule_number>\d+).*$')
    shift_re = re.compile(r'^(?P<input_item>\S+)\s+shift\sand\sgo\sto\sstate\s(?P<goto_state>\d+)$')
    action, goto = {}, {}
    current_state = -1
    with open(ply_file, 'r') as fd:
        for line in fd.xreadlines():
            line = line.strip()
            # Check for the beginning of a state declaration.
            state_match = state_re.match(line)
            if state_match:
                current_state = int(state_match.group('number'))
                action[current_state] = {}
                goto[current_state] = {}
                continue
            # Load information of the states.
            if current_state >= 0:
                shift_match = shift_re.match(line)
                if shift_match:
                    input_item = shift_match.group('input_item')
                    goto_state = shift_match.group('goto_state')
                    if input_item.isupper():
                        action[current_state][input_item] = 'S{state}'.format(state=goto_state)
                    else:
                        goto[current_state][input_item] = goto_state
                    continue
                reduce_match = reduce_re.match(line)                
                if reduce_match:
                    input_item = reduce_match.group('input_item')
                    rule_num = reduce_match.group('rule_number')
                    action[current_state][input_item] = 'R{rule}'.format(rule=rule_num)
                # Ignore the line if it is not the beginning of a state, reduce or shift information.
    return action, goto


def _write_table_file(table_file, action, goto):
    max_state = max(action.keys() + goto.keys())
    action_header = set()
    goto_header = set()
    for current_state in xrange(max_state + 1):
        action_header.update(action[current_state].keys())
        goto_header.update(goto[current_state].keys())
    action_header.remove('$end')
    action_header = sorted(action_header)
    goto_header = sorted(goto_header)
    # Generating the columns.
    columns = '*{{{action_columns}}}{{|c}}*{{{goto_columns}}}{{|c}}|'.format(action_columns=(2 + len(action_header)),
                                                                               goto_columns=len(goto_header))
    # Generating the header.
    header = ' '
    for column_header in action_header + ['\$'] + goto_header:
        header += r' & \texttt{{{column_header}}}'.format(column_header=column_header.replace('_', r'\_'))
    header += r' \\'
    # Generating rows.
    rows = ''
    for current_state in xrange(max_state + 1):
        state_action = action[current_state]
        state_goto = goto[current_state]
        row = '$I_{{{state}}}$'.format(state=current_state)
        for terminal in action_header + ['$end']:
            try:
                row += ' & {action}'.format(action=state_action[terminal])
            except KeyError:
                row += ' &'
#        row += ' &'
        for non_terminal in goto_header:
            try:
                row += ' & {goto}'.format(goto=state_goto[non_terminal])
            except KeyError:
                row += ' &'
        rows += row + r' \\' + '\n\\hline\n'
    latex_content = _LATEX_TEMPLATE.format(columns=columns, header=header, rows=rows)
    with open(table_file, 'w') as fd:
        fd.write(latex_content)


_LATEX_TEMPLATE = \
r"""
\begin{{tabular}}{{{columns}}}
\hline
{header}
\hline
{rows}
\end{{tabular}}
""".lstrip()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        ply_file = os.path.abspath(sys.argv[1])
        table_file = os.path.abspath(sys.argv[2])
        ply2lrtable(ply_file, table_file)
        sys.exit(EXIT_SUCCESS)
    else:
        print >> sys.stderr, 'Usage: {prog} <ply-file> <table-file>'.format(prog=os.path.basename(sys.argv[0]))
        sys.exit(EXIT_FAILURE)
