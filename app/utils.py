import streamlit as st
import nltk
import networkx as nx
import plotly.graph_objects as go


def update_st_state(key, val):
    st.session_state[key] = val


def create_annotated_text(
    input_string: str, word_list: list, annotation: str, color_code: str
):
    """
    Annotates the input string based on the word list provided.
    """
    tokens = nltk.word_tokenize(input_string)

    word_set = set(word_list)

    ret_annotated_text = []

    for token in tokens:
        if token in word_set:
            ret_annotated_text.append((token, annotation, color_code))
        else:
            ret_annotated_text.append(token)

    return ret_annotated_text


def create_star_graph(nodes_and_weights, title):
    """
    Create a star-shaped graph visualization.

    Args:
        nodes_and_weights (list): List of tuples containing nodes and their weights.
        title (str): Title for the graph.

    Returns:
        None
    """
    # Create an empty graph
    graph = nx.Graph()

    # Add the central node
    central_node = "resume"
    graph.add_node(central_node)

    # Add nodes and edges with weights to the graph
    for node, weight in nodes_and_weights:
        graph.add_node(node)
        graph.add_edge(central_node, node, weight=weight * 100)

    # Get position layout for nodes
    pos = nx.spring_layout(graph)

    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # Create node trace
    node_x = []
    node_y = []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="Rainbow",
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title="Node Connections",
                xanchor="left",
                titleside="right",
            ),
            line_width=2,
        ),
    )

    node_adjacencies = []
    node_text = []
    for node in graph.nodes():
        adjacencies = list(graph.adj[node])
        node_adjacencies.append(len(adjacencies))
        node_text.append(f"{node}<br># of connections: {len(adjacencies)}")

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    figure = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            titlefont=dict(size=16),
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    st.plotly_chart(figure, use_container_width=True)
