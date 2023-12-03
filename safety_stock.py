from gurobipy import Model, GRB
import pandas as pd
import time


# Calculate statistics
df = pd.read_csv("data/supply_chain_data.csv")
average_demand = df["Number of products sold"].mean()  # average demand per period
demand_std_dev = df["Number of products sold"].std()  # standard deviation of demand
lead_time = 3  # lead time in periods
service_level = 0.95  # desired service level

# Add constraint to meet service level
# This is a basic formulation and might be different based on your specific requirements
z_score = 1.96  # z-score from standard normal distribution
demand_variability = demand_std_dev * (
    lead_time**0.5
)  # demand variability over lead time

# Create a new model
model = Model("SafetyStock")

# OPTIGUIDE DATA CODE GOES HERE
# Add variable for safety stock
safety_stock = model.addVar(vtype=GRB.CONTINUOUS, name="SafetyStock")

# Set objective: Minimize safety stock
model.setObjective(safety_stock, GRB.MINIMIZE)

# Add constraint to meet service level
model.addConstr(safety_stock >= z_score * demand_variability, "ServiceLevelConstraint")

# Optimize the model
model.optimize()
m = model

# OPTIGUIDE CONSTRAINT CODE GOES HERE
m.update()
model.optimize()

print(time.ctime())

# Print the optimal safety stock
if m.status == GRB.OPTIMAL:
    print(f"Optimal Safety Stock: {safety_stock.x}")
else:
    print("No optimal solution found")
