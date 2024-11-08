"""
This script retrieves the road network graph from a specified address using OSMnx,
plots the graph and saves it as an image, and exports the nodes and edges data
to CSV files for further analysis.
"""

from pathlib import Path

import osmnx

ROOT_DIR = Path(__file__).resolve().parents[2]


def collect() -> None:
    """
    Collects OpenStreetMap (OSM) data for a specified address.

    This function performs the following actions:
    - Retrieves the road network graph for "Nam Cheong Street" using osmnx without simplifying the graph.
    - Plots the graph and saves the visualization as an image.
    - Converts the graph into GeoDataFrames for nodes and edges.
    - Prints the nodes and edges GeoDataFrames.
    - Saves the nodes and edges information to CSV files.

    Returns:
        None
    """
    graph = osmnx.graph_from_address(
        address="Nam Cheong Street",
        network_type="drive_service",
        simplify=False,
    )
    osmnx.plot_graph(
        G=graph,
        save=True,
        filepath=f"{ROOT_DIR}/reports/figures/osm_network.png",
    )
    nodes, edges = osmnx.graph_to_gdfs(G=graph)
    print(nodes)
    nodes.to_csv(path_or_buf=f"{ROOT_DIR}/datasets/raw/osm_nodes_info.csv")
    print(edges)
    edges.to_csv(path_or_buf=f"{ROOT_DIR}/datasets/raw/osm_edges_info.csv")


if __name__ == "__main__":
    collect()
