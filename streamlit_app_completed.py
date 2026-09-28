import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Reuse the same graph, coordinates, and search algorithms from Task 3.
from searchAlgos import hospital_graph, locations, gbfs, a_star

# Streamlit GUI
# ******************* #

st.set_page_config(
    page_title="Hospital Informed Search",
    page_icon="🏥",
    layout="wide"
)

st.title("Hospital Emergency Supply Robot")
st.write(
    "Interactive visualization of Greedy Best-First Search (GBFS) and A* "
    "on the Task 3 hospital graph."
)

nodes = list(hospital_graph.keys())

col1, col2, col3 = st.columns(3)

with col1:
    start = st.selectbox(
        "Select Initial Node",
        nodes,
        index=nodes.index("Pharmacy")
    )

with col2:
    goal = st.selectbox(
        "Select Goal Node",
        nodes,
        index=nodes.index("Emergency_Ward")
    )

with col3:
    algorithm = st.selectbox(
        "Select Search Algorithm",
        ["GBFS", "A*"]
    )

if st.button("Run Search", type="primary"):

    if start == goal:
        path = [start]
        cost = 0.0
    elif algorithm == "GBFS":
        path, cost = gbfs(start, goal)
    else:
        path, cost = a_star(start, goal)

    if path is None:
        st.error("No path was found between the selected nodes.")
    else:
        st.subheader("Search Result")

        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")

        # Build NetworkX graph
        G = nx.DiGraph()

        for node, position in locations.items():
            G.add_node(node, pos=position)

        for node, neighbors in hospital_graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations

        fig, ax = plt.subplots(figsize=(10, 6))

        nx.draw_networkx_nodes(
            G, pos, ax=ax, node_size=1700
        )
        nx.draw_networkx_labels(
            G, pos, ax=ax, font_size=9
        )
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=18
        )

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            ax=ax
        )

        path_edges = list(zip(path, path[1:]))

        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edgelist=path_edges,
            width=4,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=20
        )

        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")

        st.pyplot(fig)
