import pandas as pd
import time
import gurobipy as gp
from gurobipy import GRB
import random

from util.create_data_supply_net import build_model


# Import the data
supply, through, demand, arcs, cost = build_model()
assert not any(
    value == float("inf") for value in cost.values()
), "The cost dictionary contains a cost of infinity"
print(cost)

model = gp.Model("SupplyNetworkDesign")

# OPTIGUIDE DATA CODE GOES HERE
flow = model.addVars(arcs, obj=cost, name="flow")

# Production capacity limits
factories = supply.keys()
factory_flow = model.addConstrs(
    (
        gp.quicksum(flow.select(factory, "*")) <= supply[factory]
        for factory in factories
    ),
    name="factory",
)

# Customer demand
customers = demand.keys()
customer_flow = model.addConstrs(
    (
        gp.quicksum(flow.select("*", customer)) >= demand[customer]
        for customer in customers
    ),
    name="customer",
)

# Depot flow conservation

depots = through.keys()
depot_flow = model.addConstrs(
    (
        gp.quicksum(flow.select(depot, "*")) == gp.quicksum(flow.select("*", depot))
        for depot in depots
    ),
    name="depot",
)

# Depot throughput

depot_capacity = model.addConstrs(
    (gp.quicksum(flow.select("*", depot)) <= through[depot] for depot in depots),
    name="depot_capacity",
)

model.optimize()
m = model

# OPTIGUIDE CONSTRAINT CODE GOES HERE

m.update()
model.optimize()

print(time.ctime())

if m.status == GRB.OPTIMAL:
    product_flow = pd.DataFrame(columns=["From", "To", "Flow"])
    # print a table of flows for each arc
    for arc in arcs:
        if flow[arc].x > 1e-6:
            product_flow = product_flow._append(
                {"From": arc[0], "To": arc[1], "Flow": flow[arc].x}, ignore_index=True
            )
    product_flow.index = [""] * len(product_flow)
    print(product_flow)
else:
    print("No optimal solution found")
