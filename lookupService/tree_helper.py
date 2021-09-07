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

    while not done:
        _next = tree[i]
        last_node = tree[start_of_last_node:i]
        i += 1
        if _next == ')':
            if find_parent_mode:
                nodes = assign_parent_and_flush(last_node, nodes, node_pool, edge_pool)
            else:
                nodes.append(last_node)
            return nodes, i
        elif _next == ',':
            if start_of_last_node == (i-1): #assuming no 1 char labels
                find_parent_mode = False
                #if we just returned and find another subtree on the same level, we flatten the tree
                #we could also insert an artificial parent to maintain "irrelevant" details
            else:
                if find_parent_mode:
                    nodes = assign_parent_and_flush(last_node, nodes, node_pool, edge_pool)
                else:
                    nodes.append(last_node)
            start_of_last_node = i
        elif _next == '(':
            sub_tree, i = assemble_tree(tree, i, node_pool, edge_pool)
            nodes = nodes + sub_tree
            start_of_last_node = i
            find_parent_mode = True
        elif _next == ';':
            nodes = assign_parent_and_flush(last_node, nodes, node_pool, edge_pool, last=True)
            return nodes, i