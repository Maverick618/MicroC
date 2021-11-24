import sys
import os
from microC_parser import parser, error

def print_tree(node, indent: list, final_node=True, level=0):

    # if isinstance(node[0], tuple):
    #     print_tree(node[0], indent, len(node) == 1, level)
    #     level -= 1
    # else:
    for i in range(level):
        print(indent[i], end='')

    if final_node:
        print('└──', end='')
    else:
        print('├──', end='')
    if type(node) == str:
        print(node)
        return
    elif type(node) == int:
        print(node)
        return
    else:
        print(node[0])

    cnt = len(node[1])
    if cnt:
        for i, n in enumerate(node[1]):
            if n:
                c = '      ' if final_node else '│    '
                indent.append(c)
                last_node = (i == cnt - 1)
                print_tree(n, indent, last_node, level + 1)
                del indent[-1]
    else:
        c = '      ' if final_node else '│    '
        indent.append(c)
        print_tree('<empty>', indent, True, level + 1)
        del indent[-1]

def print_T(node):
    indent = []
    print(node[0])
    print_tree(node[1][0], indent)

# print(res)
# print_T(res)

def compiler(file_path):
    file_name = os.path.basename(file_path)
    cur_path = str(file_path[:-len(file_name)])
    file_name = file_name[:-2]
    sys.stdout = open(cur_path + file_name + '_out.txt', "w")
    res = parser(open(file_path, encoding='utf-8').read())
    sys.stdout = open(cur_path + file_name + '_tree.txt', "w")
    print_T(res)
    err = error(0)
    sys.stdout = open(cur_path + file_name+'_error.txt', "w")
    for msg in err:
        print(msg)
