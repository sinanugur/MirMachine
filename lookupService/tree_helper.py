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
    print(edge_pool)
    node_pool, edge_pool = prune_tree(node_pool, edge_pool)
    return node_pool, edge_pool


def assign_parent_and_flush(parent, children, node_pool, edge_pool, last=False):
    parents = parent.split('_')
    parents = [x for x in parents if x != '' and x[0].isupper()]
    for child in children:
        if len(child) == 1:
            continue
        node_pool.append({"id": child, "text": child})
        for p in parents:
            if p == child or len(p) == 1:
                continue
            new_edge = {
                "id": p + child,
                "from_node": p,
                "to_node": child
            }
            if new_edge not in edge_pool:
                edge_pool.append(new_edge)
    if last:
        node_pool.append({"id": parent, "text": parent})
    return parents


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
                last_node = "Artificial-node" + str(i)
            if find_parent_mode:
                nodes = nodes + assign_parent_and_flush(last_node, sub_tree, node_pool, edge_pool)
            else:
                nodes.append(last_node)

            return nodes, i
        elif _next == ',':
            if start_of_last_node == (i-1):  # assuming no 1 char labels
                last_node = "Artificial-node" + str(i)

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


def prune_tree(nodes, edges):
    nodes_to_remove = []
    filtered_nodes = []
    for node in nodes:
        # outgoing edges from each node
        outgoing = [e for e in edges if e.get('from_node') == node.get('id')]
        # if it is not already selected and is not a leaf, add it
        if node not in filtered_nodes and len(outgoing) != 0:
            filtered_nodes.append(node)
        # if it is a leaf, mark it for removal
        if len(outgoing) == 0:
            nodes_to_remove.append(node.get('id'))
    # remove edges to leaf nodes
    filtered_edges = [x for x in edges if x.get('to_node') not in nodes_to_remove]

    # second pass to remove artificial nodes that now are leaf nodes
    nodes_to_remove = []
    artificial_nodes = [x for x in filtered_nodes if x.get('id').startswith('Artificial-node')]
    for node in artificial_nodes:
        outgoing = [e for e in filtered_edges if e.get('from_node') == node.get('id')]
        if len(outgoing) == 0:
            nodes_to_remove.append(node.get('id'))
    filtered_edges = [x for x in filtered_edges if x.get('to_node') not in nodes_to_remove]
    filtered_nodes = [x for x in filtered_nodes if x not in nodes_to_remove]
    return filtered_nodes, filtered_edges

