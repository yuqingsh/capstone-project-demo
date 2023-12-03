import random
import time
from gurobipy import GRB, Model, quicksum
import numpy as np


# Define the parameters
wage = 21 / 60  # wage of a delivery driver (per minute)
g = 0.65        # Gas expense per distance traveled

C = 350         # maximum number of packages truck k can hold
H = 10 * 60     # number of minutes that a truck operates in a day

# Z_{ij}: the distance travelled, in miles, from node i to node j
Z = np.loadtxt('data/stop_stop_sh_clean.csv', delimiter=',')
# T_{ij}: time it takes for a truck to drive from node i to node j (in minutes)
speed = 55
T = Z / speed

num_trucks = 15
num_nodes = Z.shape[0]

B = 100000      # arbitrarily large number


# Create a new model
model = Model("last_mile_delivery")

# OPTIGUIDE DATA CODE GOES HERE

# Decision Variables
# X_{ijk}: binary variable indicating whether or not truck k travels from node i to node j
X = {}
for i in range(num_nodes):
    for j in range(num_nodes):
        for k in range(num_trucks):
            X[i, j, k] = model.addVar(vtype=GRB.BINARY, name=f"X_{i}_{j}_{k}")

# p
p = {}
for i in range(num_nodes):
    p[i] = model.addVar(vtype=GRB.CONTINUOUS, name=f"p_{i}")

# Objective: minimize total shipping costs
obj = quicksum(X[i, j, k] * (wage * T[i][j] + g * Z[i][j]) 
               for j in range(num_nodes) 
               for k in range(num_trucks))

model.setObjective(obj, GRB.MINIMIZE)

# Constraints
# Constraint 1: Space constraints on the delivery vehicle
for k in range(num_trucks):
    model.addConstr(
        quicksum(X[i, j, k] for j in range(num_nodes)) <= C,
        f"Volume_Constraint_{k}"
    )

# Constraint 2: Trucks stop operation by the end of work hours each day
for k in range(num_trucks):
    model.addConstr(
        quicksum(X[i, j, k] * T[i][j] for j in range(num_nodes)) <= H,
        f"Stop_Operation_{k}"
    )

# Constraint 3: Each package delivered once in exactly one truck
for j in range(num_nodes):
    model.addConstr(
        quicksum(X[i, j, k] for k in range(num_trucks)) == 1,
        f"Package_{j}"
    )

# Constraint 4: Connectedness Constraint
model.addConstr(
    quicksum(X[i, j, k] for j in range(num_nodes)) == quicksum(X[i, j, k] for i in range(num_nodes)),
    "Connectedness_Constraint_1"
)
model.addConstr(
    quicksum(X[i, j, k] for j in range(num_nodes)) <= 1,
    "Connectedness_Constraint_2"
)

# Constraint 5: Subtour Elimination Constraint
model.addConstr(
    p[0] == 0
)
model.addConstr(
    p[i] <= p[j] + B * (1 - quicksum(X[i, j, k] for k in range(num_trucks))),
    "Subtour_Elimination_Constraint"
)

# Constraint 6: Arrival Timestamp Constraint
model.addConstr(
    -B * quicksum(X[i, j, k] for k in range(num_trucks)) <= p[i] + T[i, j] - p[j],
    "Arrival_Timestamp_Constraint_1"
)
model.addConstr(
    B * (1 - quicksum(X[i, j, k] for k in range(num_trucks))) >= p[j] - p[i] - T[i, j],
    "Arrival_Timestamp_Constraint_2"
)


# Optimize model
model.optimize()
m = model

# OPTIGUIDE CONSTRAINT CODE GOES HERE

# Solve
m.update()
model.optimize()

print(time.ctime())
if m.status == GRB.OPTIMAL:
    print(f'Optimal cost: {m.objVal}')

    # Extracting the optimal routes for each truck
    optimal_routes = {k: [] for k in range(num_trucks)}
    for i in range(num_nodes):
        for j in range(num_nodes):
            for k in range(num_trucks):
                if round(m.getVarByName(f'X_{i}_{j}_{k}').x) == 1:
                    optimal_routes[k].append((i, j))

    # Visualizing the routes for each truck
    import matplotlib.pyplot as plt

    def plot_route(route, title):
        plt.figure(figsize=(8, 6))
        plt.title(title)
        for i, j in route:
            plt.plot([i, j], [i, j], marker='o', linestyle='-')

    for truck, route in optimal_routes.items():
        plot_route(route, f"Truck {truck + 1} Route")
        plt.show()
else:
    print("Not solved to optimality. Optimization status:", m.status)