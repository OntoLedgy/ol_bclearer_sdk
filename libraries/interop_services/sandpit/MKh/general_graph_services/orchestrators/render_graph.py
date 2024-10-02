from graphviz import Digraph
from object_model.Nodes import Node


def render_graph():
    """Render in a graph output object pdf"""
    directedSameAsGraph = Digraph(
        comment="Same As Graph",
    )

    for (
        key,
        value,
    ) in Node._registry.items():
        directedSameAsGraph.node(
            str(value.node_uuid),
        )

        for (
            connectednode
        ) in value.connected_nodes:
            directedSameAsGraph.edge(
                str(value.node_uuid),
                str(
                    connectednode.node_uuid,
                ),
            )

    print(directedSameAsGraph)

    directedSameAsGraph.view()
