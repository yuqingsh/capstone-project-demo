import random
from load_dc import load_dc_data


def build_model():
    # Import the data
    nodes, edges = load_dc_data()

    # Randomly assign nodes to be factories, ports, or customers
    factories = random.sample(
        nodes, 30
    )  # Replace 5 with the number of factories you want

    ports = random.sample(
        [node for node in nodes if node not in factories], 100
    )  # Replace 5 with the number of ports you want

    customers = [node for node in nodes if node not in factories and node not in ports]

    # Assign random supply values to factories
    supply = {factory["id"]: random.randint(10000, 200000) for factory in factories}

    # Assign random throughput values to ports
    through = {port["id"]: random.randint(50000, 100000) for port in ports}

    # Assign random demand values to customers
    demand = {customer["id"]: random.randint(10000, 50000) for customer in customers}

    return supply, through, demand, nodes, edges


if __name__ == "__main__":
    supply, through, demand, nodes, edges = build_model()
    print(supply)
    print(through)
    print(demand)
    print(nodes)
    print(edges)
