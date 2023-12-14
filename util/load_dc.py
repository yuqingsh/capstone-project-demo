# Define the path to the file
import gurobipy as gp
import datetime

FILE_PATH = "data/DC.tmp"
TIME_MARGIN_COST = 0.4
DISTANCE_MARGIN_COST = 0.6


def load_dc_data():
    with open(FILE_PATH, "r") as file:
        lines = file.readlines()

    # Get the number of nodes and edges
    num_nodes = int(lines[0].strip())
    num_edges = int(lines[num_nodes + 1].strip())

    # Extract node data
    nodes = []
    for i in range(1, num_nodes + 1):
        node_id, longitude, latitude = map(float, lines[i].split())
        node_id = int(node_id)
        nodes.append({"id": node_id, "longitude": longitude, "latitude": latitude})

    # Extract edge data
    edges = {
        (int(lines[i].split()[0]), int(lines[i].split()[1])): TIME_MARGIN_COST
        * float(lines[i + 1].split()[0])
        + DISTANCE_MARGIN_COST * float(lines[i + 1].split()[1])
        for i in range(num_nodes + 2, num_nodes + 2 + num_edges * 2, 2)
    }

    return nodes, edges


if __name__ == "__main__":
    nodes, edges = load_dc_data()
    print(edges)
