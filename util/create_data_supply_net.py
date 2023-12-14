import random
from util.load_dc import load_dc_data
import gurobipy as gp
import heapq


def create_graph_from_edges(edges):
    """
    Convert a set of edges into a graph representation.

    :param edges: A set of tuples (node1, node2, weight)
    :return: A dictionary representing the graph.
    """
    graph = {}
    for (node1, node2), weight in edges.items():
        if node1 not in graph:
            graph[node1] = []
        if node2 not in graph:
            graph[node2] = []
        graph[node1].append((node2, weight))
        graph[node2].append((node1, weight))
    return graph


def dijkstra_shortest_path(graph, start, target):
    """
    Find the shortest path distance from the start node to the target node in a graph using Dijkstra's algorithm.
    """
    distances = {node: float("infinity") for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == target:
            return distances[target]

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return float("infinity")


def build_model():
    # Import the data
    nodes, edges = load_dc_data()
    graph = create_graph_from_edges(edges)

    # Randomly assign nodes to be factories, ports, or customers
    factories_idx = random.sample(range(100), 60)

    ports_idx = random.sample(
        [i for i in range(100, 200) if i not in factories_idx], 100
    )

    customers_idx = random.sample(
        [i for i in range(200, 250) if i not in factories_idx and i not in ports_idx],
        20,
    )

    supply = {
        "Factory" + str(int(nodes[i]["id"])): random.randint(10000, 20000)
        for i in factories_idx
    }
    through = {
        "Port" + str(int(nodes[i]["id"])): random.randint(8000, 30000)
        for i in ports_idx
    }
    demand = {
        "Customer" + str(int(nodes[i]["id"])): random.randint(6000, 25000)
        for i in customers_idx
    }

    temp_dict = {}
    for i, j in zip(factories_idx, ports_idx):
        temp_dict[
            "Factory" + str(int(nodes[i]["id"])), "Port" + str(int(nodes[j]["id"]))
        ] = (dijkstra_shortest_path(graph, i, j) / 10000)
    for i, j in zip(ports_idx, customers_idx):
        temp_dict[
            "Port" + str(int(nodes[i]["id"])), "Customer" + str(int(nodes[j]["id"]))
        ] = (dijkstra_shortest_path(graph, i, j) / 10000)

    arc, cost = gp.multidict(temp_dict)

    return supply, through, demand, arc, cost


if __name__ == "__main__":
    supply, through, demand, arc, cost = build_model()
    print(supply)
    print(through)
    print(demand)
    print(arc)
    print(cost)
