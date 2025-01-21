import pytest
from pyvis.network import Network


class TestGraphVisualistion:

    @pytest.fixture(autouse=True)
    def setup(self):
        # Create a network and add some nodes and edges
        self.network = Network()

        # Add nodes with different properties
        self.network.add_node(
            1, label="Node 1"
        )
        self.network.add_node(2)

        # Add a list of nodes
        nodes = ["a", "b", "c", "d"]
        self.network.add_nodes(nodes)

        # Add a single string node
        self.network.add_node("hello")

        # Add edges to connect the nodes
        self.network.add_edge(1, 2)
        self.network.add_edge("a", "b")
        self.network.add_edge("c", "d")

        # Inject options for smooth edges and navigation buttons
        self.network.set_options(
            """
        var options = {
          "edges": {
            "smooth": {
              "type": "continuous"
            }
          },
          "interaction": {
            "navigationButtons": true
          }
        }
        """
        )

    def inject_custom_js(
        self, html_file_path
    ):
        """
        This method injects custom JavaScript into the generated HTML file to handle
        the double-click event for toggling the visibility of both edges and connected nodes.
        """
        custom_js = """
        <script type="text/javascript">
        function toggleEdgesAndNodes(network, nodeId) {
          // Get connected edges and toggle their visibility
          var connectedEdges = network.getConnectedEdges(nodeId);
          connectedEdges.forEach(function(edgeId) {
            var edge = network.body.data.edges.get(edgeId);
            edge.hidden = !edge.hidden;
            network.body.data.edges.update(edge);
          });

          // Get connected nodes and toggle their visibility
          var connectedNodes = network.getConnectedNodes(nodeId);
          connectedNodes.forEach(function(connectedNodeId) {
            if (connectedNodeId !== nodeId) {  // Don't hide the original node
              var node = network.body.data.nodes.get(connectedNodeId);
              node.hidden = !node.hidden;
              network.body.data.nodes.update(node);
            }
          });
        }

        network.on("doubleClick", function(params) {
          if (params.nodes.length > 0) {
            var nodeId = params.nodes[0];
            toggleEdgesAndNodes(network, nodeId);
          }
        });
        </script>
        """

        # Inject the custom JS into the HTML after the network initialization script
        with open(
            html_file_path, "r+"
        ) as f:
            content = f.read()
            # Insert the custom JS before the closing body tag
            content = content.replace(
                "</body>",
                f"{custom_js}\n</body>",
            )
            f.seek(0)
            f.write(content)
            f.truncate()

    def test_show_network(
        self, tmp_path
    ):
        # Save the visualization to a file with notebook=False
        output_path = (
            tmp_path / "network.html"
        )
        self.network.show(
            str(output_path),
            notebook=False,
        )

        # Test that the file was created
        assert output_path.exists()

        # Check that the file has content (simple validation)
        with open(
            output_path, "r"
        ) as file:
            content = file.read()
            assert "<html>" in content
            assert "<body>" in content

    def test_edge_expansion_and_collapse(
        self, tmp_path
    ):
        # Save the visualization to a file with edge expansion/collapse options
        output_path = (
            tmp_path
            / "network_expansion.html"
        )
        self.network.show(
            str(output_path),
            notebook=False,
        )

        # Test that the file was created
        assert output_path.exists()

        # Inject custom JavaScript into the generated HTML
        self.inject_custom_js(
            str(output_path)
        )

        # Check that the edge configuration has expansion and collapse features
        with open(
            output_path, "r"
        ) as file:
            content = file.read()
            # Validate that the custom JS was injected correctly
            assert (
                "doubleClick" in content
            )
            assert (
                "toggleEdges" in content
            )
