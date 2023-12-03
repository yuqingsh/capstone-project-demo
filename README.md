# Capstone Project Demo
This is a project aims at building a chatbot utlizing LLM to help with supply chain optimization decision-making.

Credit: [Optiguide](https://github.com/microsoft/OptiGuide/tree/main)

# Secret Key Setting
Before running the notebook, you should set you OpenAI secret key as a environment variable

Fill in the line with your OpenAI key on top of the notebooks. You can find your OpenAI API key [here](https://platform.openai.com/api-keys).
```python
%env OPENAI_API_KEY='YOUR_SECRET_KEY'
```

# Examples
* Safety Stock

  This is a trivial example showing the minimal feasibility of OptiGuide. It reads from a csv file as the database and calculate use a single constraint.

* Supply Network

  This is a example found with [Gurobi](https://gurobi.github.io/modeling-examples/supply_network_design/). It describes a problem scenario where the decision maker have to make a plan for shipping between multiple factories and ports to minimize the cost.