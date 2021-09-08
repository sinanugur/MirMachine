import os


def parse_newick_tree():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../engine/mirmachine/meta/tree.newick')
    _file = open(file_path, 'r')
    tree = _file.readline()
    _file.close()
    node_pool = []
    edge_pool = []
    assemble_tree(tree, 0, node_pool, edge_pool)
    return node_pool, edge_pool


def assign_parent_and_flush(parent, children, node_pool, edge_pool, last=False):
    for child in children:
        node_pool.append({"id": child, "text": child})
        edge_pool.append({
            "id": child,
            "from_node": parent,
            "to_node": child
        })
    if last:
        node_pool.append({"id": parent, "text": parent})
    return [parent]


def assemble_tree(tree, index, node_pool, edge_pool):
    done = False
    i = index
    start_of_last_node = index
    nodes = []
    find_parent_mode = False
    sub_tree = []
    while not done:
        _next = tree[i]
        last_node = tree[start_of_last_node:i]
        i += 1
        if _next == ')':
            if start_of_last_node == (i-1):
                last_node = "Artificial_node" + str(i)
            if find_parent_mode:
                nodes = nodes + assign_parent_and_flush(last_node, sub_tree, node_pool, edge_pool)
            else:
                nodes.append(last_node)

            return nodes, i
        elif _next == ',':
            if start_of_last_node == (i-1):  # assuming no 1 char labels
                last_node = "Artificial_node" + str(i)

            if find_parent_mode:
                nodes = nodes + assign_parent_and_flush(last_node, sub_tree, node_pool, edge_pool)
                find_parent_mode = False
            else:
                nodes.append(last_node)
            start_of_last_node = i
        elif _next == '(':
            sub_tree, i = assemble_tree(tree, i, node_pool, edge_pool)
            start_of_last_node = i
            find_parent_mode = True
        elif _next == ';':
            nodes = assign_parent_and_flush(last_node, sub_tree, node_pool, edge_pool, last=True)
            return nodes, i