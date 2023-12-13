# Define the path to the file
file_path = "data/DC.tmp"


def load_dc_data():
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Get the number of nodes and edges
    num_nodes = int(lines[0].strip())
    num_edges = int(lines[num_nodes + 1].strip())

    # Extract node data
    nodes = []
    for i in range(1, num_nodes + 1):
        id, longitude, latitude = map(float, lines[i].split())
        nodes.append({"id": id, "longitude": longitude, "latitude": latitude})

    # Extract edge data
    edges = []
    for i in range(num_nodes + 2, num_nodes + 2 + num_edges * 2, 2):
        source, target = map(int, lines[i].split())
        time, distance, category = map(float, lines[i + 1].split())
        edges.append(
            {
                "source": source,
                "target": target,
                "time": time,
                "distance": distance,
                "category": category,
            }
        )

    return nodes, edges


if __name__ == "__main__":
    nodes, edges = load_dc_data()
    print(nodes)
    print(edges)
