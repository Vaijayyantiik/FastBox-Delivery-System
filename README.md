# FastBox Mystery Delivery System

## Project Overview
This project simulates one day of operations for a fictional logistics company called FastBox.

The system:
- Reads warehouse, agent, and package data from JSON files
- Assigns packages to the nearest delivery agent
- Simulates deliveries
- Calculates total distance traveled
- Calculates delivery efficiency
- Generates delivery reports
- Exports top performer details to CSV

---

## Features
- JSON Parsing
- Euclidean Distance Calculation
- Nearest Agent Assignment
- Delivery Simulation
- Efficiency Calculation
- Report Generation
- JSON Report Export
- CSV Export
- Random Delivery Delays
- ASCII Route Visualization
- New Agent Joining Mid-Day

---

## Assumptions Made
1. Distance is calculated using Euclidean Distance Formula.
2. Efficiency is calculated as:
   Total Distance / Packages Delivered
3. Lower efficiency value indicates better performance.
4. If multiple agents are at equal distance, the first encountered agent is selected.
5. New agent joins after processing 4 packages.
6. Random delay ranges from 1 to 10 minutes.
7. Agent returns are not considered after delivery completion.
8. Each package is delivered independently.

---

## How to Run

```bash
python main.py
```

Then enter:

base_case.json

or any test case JSON file.

---

## Output Files
- report.json
- top_performer.csv

---

## Technologies Used
- Python
- JSON
- CSV
- Math Module
- Random Module
