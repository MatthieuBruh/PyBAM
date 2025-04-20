import re
import tempfile
import webbrowser
from pyvis.network import Network

# -----------------------------------------------------------------------------
# Helper: Generate a natural sort key from a string containing numbers.
# Useful for sorting keys like "Q2-1-1" in a human-friendly order.
# -----------------------------------------------------------------------------
def natural_sort_key(key):
    return list(map(int, re.findall(r'\d+', key)))


# -----------------------------------------------------------------------------
# Compute the hierarchical depth (level) of each node in the decision tree.
# This ensures proper placement of nodes in a hierarchical layout.
# -----------------------------------------------------------------------------
def compute_levels(data):
    levels = {}

    def _compute(node_key, level=0):
        # If the node has already been assigned a level, keep the minimum level
        if node_key in levels:
            levels[node_key] = min(levels[node_key], level)
        else:
            levels[node_key] = level

        node = data["nodes"][node_key]
        if node["type"] == "question":
            # Recursively compute levels for child nodes
            targets = sorted(node["choices"].values(), key=natural_sort_key)
            for target in targets:
                _compute(target, level + 1)

    _compute(data["start"])
    return levels


# -----------------------------------------------------------------------------
# Recursively add nodes and edges to the PyVis network graph.
# Colors and shapes are assigned based on node type (question or answer).
# -----------------------------------------------------------------------------
def add_nodes_and_edges(net, data, levels):
    nodes_added = set()

    def _add(key):
        if key in nodes_added:
            return

        node = data["nodes"][key]
        label = node["text"]
        color = "lightblue" if node["type"] == "question" else "lightgreen"
        shape = "ellipse" if node["type"] == "question" else "box"
        level = levels.get(key, 0)

        # Add the current node to the graph
        net.add_node(key, label=label, shape=shape, color=color, level=level)
        nodes_added.add(key)

        # Add edges to child nodes, if it's a question
        if node["type"] == "question":
            targets = sorted(node["choices"].values(), key=natural_sort_key)
            for target in targets:
                _add(target)
                net.add_edge(key, target)

    _add(data["start"])


# -----------------------------------------------------------------------------
# Generate the HTML representation of the network graph and open it in a browser.
# The HTML file is created in a temporary location and automatically displayed.
# -----------------------------------------------------------------------------
def generate_and_open_html(net):
    html_content = net.generate_html()

    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html", encoding="utf-8") as tmp:
        tmp.write(html_content)
        temp_file_path = tmp.name

    # Open the file in the default web browser
    webbrowser.open(f"file://{temp_file_path}")


# -----------------------------------------------------------------------------
# Main function to display the interactive decision tree from the provided data.
# -----------------------------------------------------------------------------
def display_tree(data: dict):
    # Initialize the PyVis network graph
    net = Network(height="100vh", width="100vw", bgcolor="#ffffff", directed=True)
    net.toggle_physics(False)

    # Define layout and visual styling options using Vis.js configuration
    net.set_options("""
    {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "levelSeparation": 300,
          "nodeSpacing": 350,
          "treeSpacing": 400,
          "direction": "UD",
          "sortMethod": "directed"
        }
      },
      "nodes": {
        "margin": 12,
        "widthConstraint": {
          "maximum": 350
        },
        "font": {
          "size": 16,
          "multi": "html"
        }
      },
      "edges": {
        "arrows": {
          "to": {"enabled": true}
        },
        "smooth": {
          "type": "cubicBezier",
          "forceDirection": "vertical",
          "roundness": 0.4
        }
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true
      },
      "physics": {
        "enabled": false
      }
    }
    """)

    # Compute node depth levels and add nodes/edges to the graph
    levels = compute_levels(data)
    add_nodes_and_edges(net, data, levels)

    # Generate and open the interactive visualization
    generate_and_open_html(net)
