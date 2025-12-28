import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# ------------------------------
# Struktur Node
# ------------------------------
class Node:
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None

# ------------------------------
# Generate pohon biner seimbang
# ------------------------------
def generate_balanced_tree(n):
    if n == 0:
        return None
    nodes = [Node(i) for i in range(1, n+1)]
    def build_tree(nodes_list):
        if not nodes_list:
            return None
        mid = len(nodes_list) // 2
        root = nodes_list[mid]
        root.left = build_tree(nodes_list[:mid])
        root.right = build_tree(nodes_list[mid+1:])
        return root
    return build_tree(nodes)

# ------------------------------
# Preorder Traversal Iteratif
# ------------------------------
def preorder_iteratif(root):
    if not root:
        return []
    stack = [root]
    result = []
    while stack:
        node = stack.pop()
        result.append(node.info)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result

# ------------------------------
# Preorder Traversal Rekursif
# ------------------------------
def preorder_rekursif(root):
    if root is None:
        return []
    result = [root.info] 
    result += preorder_rekursif(root.left)
    result += preorder_rekursif(root.right)
    return result

# ------------------------------
# Hitung tinggi pohon
# ------------------------------
def tree_height(root):
    if not root:
        return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))

# ------------------------------
# Convert pohon ke NetworkX graph
# ------------------------------
def tree_to_graph(root, G=None):
    if G is None:
        G = nx.DiGraph()
    if not root:
        return G
    G.add_node(root.info)
    if root.left:
        G.add_edge(root.info, root.left.info)
        tree_to_graph(root.left, G)
    if root.right:
        G.add_edge(root.info, root.right.info)
        tree_to_graph(root.right, G)
    return G

# ------------------------------
# Layout rapi untuk pohon
# ------------------------------
def hierarchy_pos_dynamic(G, root, vert_gap=0.2):
    if root is None or root not in G:
        return {}

    levels = {}
    def dfs(node, depth=0):
        if depth not in levels:
            levels[depth] = 0
        levels[depth] += 1
        for child in G.successors(node):
            dfs(child, depth+1)
    dfs(root)

    max_width = max(levels.values())

    def _hierarchy_pos(node, left, right, vert_loc):
        pos[node] = ((left + right) / 2, vert_loc)
        children = list(G.successors(node))
        if len(children) >= 1:
            _hierarchy_pos(children[0], left, (left+right)/2, vert_loc-vert_gap)
        if len(children) >= 2:
            _hierarchy_pos(children[1], (left+right)/2, right, vert_loc-vert_gap)

    pos = {}
    _hierarchy_pos(root, 0, max_width, 0)
    return pos

# ------------------------------
# Fungsi untuk ukuran node
# ------------------------------
def get_node_and_font_size(num_nodes):
    if num_nodes <= 1:
        return 4000, 40
    elif num_nodes <= 3:
        return 3500, 35
    elif num_nodes <= 7:
        return 3000, 30
    elif num_nodes <= 15:
        return 2500, 25
    elif num_nodes <= 31:
        return 800, 15
    elif num_nodes <= 63:
        return 180, 9
    else:
        return 40, 4

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("_:green[Preorder Traversal Pohon Biner]_")

# Input jumlah node
num_nodes = st.number_input("Masukkan jumlah node pohon:", min_value=1, max_value=1000000, value=1, step=1)

# Generate pohon seimbang
root = generate_balanced_tree(num_nodes)
st.write(f"Tinggi pohon: {tree_height(root)}")

# Jalankan preorder iteratif
if st.button("Preorder Iteratif"):
    result_iter = preorder_iteratif(root)
    st.write(f"Urutan Preorder Traversal Iteratif: {result_iter[:100]}{'...' if len(result_iter)>100 else ''}")
    st.write(f"Jumlah node yang dikunjungi: {len(result_iter)}")

# Jalankan preorder rekursif
if st.button("Preorder Rekursif"):
    result_recur = preorder_rekursif(root)
    st.write(f"Urutan Preorder Traversal Rekursif: {result_recur[:100]}{'...' if len(result_recur)>100 else ''}")
    st.write(f"Jumlah node yang dikunjungi: {len(result_recur)}")

# Visualisasi pohon untuk jumlah node ≤ 127
if num_nodes <= 127:
    G = tree_to_graph(root)
    plt.figure(figsize=(8,6))
    pos = hierarchy_pos_dynamic(G, root.info, vert_gap=0.5)
    if pos:
        node_size, font_size = get_node_and_font_size(num_nodes)
        nx.draw(G, pos, with_labels=True, node_size=node_size, node_color='lightblue', font_size=font_size, arrows=True)
        st.pyplot(plt)
    else:
        st.info("Node tidak ditemukan di graph, tidak ada pohon untuk divisualisasikan.")
else:
    st.info("Visualisasi pohon hanya tersedia untuk node ≤ 127.")
