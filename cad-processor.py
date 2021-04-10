import csv
from anytree import *

input_csv_filename = 'test_input.csv'
input_key_filename = 'key_input.csv'
pos_column = 0
key_column = 1
qty_column = 2


def import_part_list(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        data_lines = list(reader)
    return data_lines

def import_keys(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        keys_input = list(reader)
        keys = []
        for key in keys_input:
            keys.append(key[0])
    return keys

def remove_sub_parts(part_list, key_list):

    def find_key_pos(part_list,key_list):
        key_pos = []    
        for row in part_list[1:]:
            if row[key_column] in key_list:
                key_pos.append(row[pos_column])
        return key_pos

    def filter_values(row):
        key_pos = find_key_pos(part_list, key_list)
        for val in key_pos:
            if row[pos_column].startswith(val) and row[pos_column] != val:
                return False
        return True

    return list(filter(filter_values, part_list))


def remove_empty_pos(part_list):
    def filter_empty_pos(row):
        return row[key_column]
    
    return list(filter(filter_empty_pos, part_list))

keys = import_keys('key_input.csv')
filtered_part_list = remove_sub_parts(import_part_list('test_input.csv'), keys)
clean_list = remove_empty_pos(filtered_part_list)

root = Node('root')
udo = Node('udo', parent=root, row = [1,2,3])
print(RenderTree(root))


def list_to_tree(part_list):
    root = Node('root')
    list_of_nodes = [root]
    for row in part_list[1:]:
        hirachy = row[pos_column].split('.')
        if len(hirachy) < 2:
            node = Node(row[pos_column], parent = root, data = row)
        
        else:
            parent_name = '.'.join(hirachy[0:-1])
            tuple_of_parents = findall_by_attr(root, parent_name)
            node = Node(row[pos_column], parent = tuple_of_parents[0], data = row)
    
        list_of_nodes.append(node) # only for debug
    return root

def accumulate_quantities(root):
    for node in list(PreOrderIter(root))[1:]:
        accumulated_quantity = int(node.data[qty_column])
        ancestors = node.ancestors
        for ancestor in ancestors[1:]:
            accumulated_quantity *= int(ancestor.data[qty_column])
        node.accumulated_quantity = accumulated_quantity


def leaves(root):
    return root.leaves 

root = list_to_tree(clean_list)

print(RenderTree(root))

tup = findall_by_attr(root, '3')
accumulate_quantities(root)