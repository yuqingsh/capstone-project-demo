import pandas as pd
import time
import gurobipy as gp
from gurobipy import GRB
import random

from util.load_dc import load_dc_data

# Import the data
nodes, edges = load_dc_data()

# Select a subset of nodes
nodes = random.sample(nodes, 60)  # Replace 1000 with the number of nodes you want

# Randomly assign nodes to be factories, ports, or customers
factories = random.sample(nodes, 20)  # Replace 20 with the number of factories you want
ports = random.sample(
    [node for node in nodes if node not in factories], 20
)  # Replace 50 with the number of ports you want
customers = [node for node in nodes if node not in factories and node not in ports]

# Assign random supply values to factories
supply = {factory["id"]: random.randint(10000, 200000) for factory in factories}

# Assign random throughput values to ports
through = {port["id"]: random.randint(50000, 100000) for port in ports}

# Assign random demand values to customers
demand = {customer["id"]: random.randint(10000, 50000) for customer in customers}

# Create a dictionary to capture shipping costs.
cost = {(edge["source"], edge["target"]): edge["distance"] for edge in edges}

# Create a new model
model = gp.Model("SupplyNetworkDesign")

# Convert edges to a list of tuples
edges = list(set((edge["source"], edge["target"]) for edge in edges))

# Create variables
flow = model.addVars(edges, obj=cost, name="flow")

# Add supply constraints
factories = supply.keys()
model.addConstrs(
    (
        gp.quicksum(flow.select(factory, "*")) <= supply[factory]
        for factory in factories
    ),
    name="factory",
)

# Add throughput constraints
ports = through.keys()
model.addConstrs(
    (gp.quicksum(flow.select(port, "*")) <= through[port] for port in ports),
    name="port",
)

# Add demand constraints
customers = demand.keys()
model.addConstrs(
    (
        gp.quicksum(flow.select("*", customer)) >= demand[customer]
        for customer in customers
    ),
    name="customer",
)

# Optimize model
model.optimize()

# Print solution
if model.status == GRB.OPTIMAL:
    for v in model.getVars():
        print("%s: %g" % (v.varName, v.x))
