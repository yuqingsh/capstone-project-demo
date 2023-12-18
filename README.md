# Capstone Project Demo
This is a project aims at building a chatbot utlizing LLM to help with supply chain optimization decision-making.

Credit: [Optiguide](https://github.com/microsoft/OptiGuide/tree/main)

# Secret Key Setting
Before running the notebook, you should set you OpenAI secret key as a environment variable

Fill in the line with your OpenAI key before running. You can find your OpenAI API key [here](https://platform.openai.com/api-keys).
```python
openai.api_key = "YOUR_API_KEY_HERE"
```

# Examples
* Safety Stock

  This is a trivial example showing the minimal feasibility of OptiGuide. It reads from a csv file as the database and calculate use a single constraint.

* Supply Network

  This is a example found with [Gurobi](https://gurobi.github.io/modeling-examples/supply_network_design/). It describes a problem scenario where the decision maker have to make a plan for shipping between multiple factories and ports to minimize the cost.

# Project Structure
This repository contains both the code tests. The structure is as followed:

```
├── README.md
├── delivery.py
├── safety_stock.py
├── stability_test.py
├── supply_network.py
├── supply_network_scaled.py
├── util
│   ├── create_data_supply_net.py
│   ├── extract_content_from_log.py
├── log
└── data
    ├── DC.tmp
    └── supply_chain_data.csv
```

These are source codes used for in-context learning for OptiGuide agenet. Also, their outputs are used as the benchmark when testing OptiGuide's performance.
- delivery.py
- safety_stock.py
- supply_network.py
- supply_network_scaled.py

The following are used for the stability test. To use, you will have to key in your OpenAI secret key following the previous instruction.
- stability_test.py

The folder contains utility function needed both in test and source code.
- create_data_supply_net.py

  This is the file used to extract data from csv file for supply_network_scaled.py
- extract_data_supply_from_log.py

  This is the code to extract human readable content from raw log produced by stability_test.py.