# Travelling Salesman Problem
This program solves the Traveling Salesman Problem (TSP), where the goal is to find the shortest possible route that visits a given set of cities exactly once and returns to the starting point.

<b>Algorithm:</b> Ant Colony Optimization (ACO)

<b>Graphic:</b> PyGame

## How to run (Windows)
```
git clone https://github.com/Cezary-Androsiuk/travelling-salesman-problem.git
cd travelling-salesman-problem
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Data
<b>File:</b> ```city.data.txt```\
<b>Structure:</b>\
```1721 615 Białystok 296958```\
```xPos yPos cityName population```

## Selection
In the file ```Selection.txt```, place the names of the cities you want to use, or a single number specifying how many cities the algorithm should randomly select. Leave the file empty or delete it if you don't want any selection and wish to use all cities.