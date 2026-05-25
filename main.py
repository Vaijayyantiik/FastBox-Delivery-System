import json
import math
import random
import csv


# -------------------------------------------------
# Calculate Euclidean Distance
# -------------------------------------------------
def calculate_distance(point1, point2):

    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


# -------------------------------------------------
# Normalize Warehouses
# -------------------------------------------------
def normalize_warehouses(warehouses):

    if isinstance(warehouses, list):

        warehouse_dict = {}

        for warehouse in warehouses:

            warehouse_dict[
                warehouse["id"]
            ] = warehouse["location"]

        return warehouse_dict

    return warehouses


# -------------------------------------------------
# Normalize Agents
# -------------------------------------------------
def normalize_agents(agents):

    if isinstance(agents, dict):

        agent_list = []

        for agent_id, location in agents.items():

            agent_list.append({
                "id": agent_id,
                "location": location
            })

        return agent_list

    return agents


# -------------------------------------------------
# Normalize Packages
# -------------------------------------------------
def normalize_packages(packages):

    normalized = []

    for package in packages:

        if "warehouse_id" in package:

            normalized.append({
                "id": package["id"],
                "warehouse": package["warehouse_id"],
                "destination": package["destination"]
            })

        else:

            normalized.append(package)

    return normalized


# -------------------------------------------------
# Find Nearest Agent
# -------------------------------------------------
def find_nearest_agent(
    warehouse_location,
    agents
):

    nearest_agent = None

    minimum_distance = float("inf")

    for agent in agents:

        agent_id = agent["id"]

        agent_location = agent["location"]

        distance = calculate_distance(
            warehouse_location,
            agent_location
        )

        if distance < minimum_distance:

            minimum_distance = distance

            nearest_agent = agent_id

    return nearest_agent, minimum_distance


# -------------------------------------------------
# Read JSON File
# -------------------------------------------------
filename = input(
    "Enter JSON file name: "
)

with open(filename, "r") as file:

    data = json.load(file)


# -------------------------------------------------
# Normalize Data
# -------------------------------------------------
warehouses = normalize_warehouses(
    data["warehouses"]
)

agents = normalize_agents(
    data["agents"]
)

packages = normalize_packages(
    data["packages"]
)


# -------------------------------------------------
# Initialize Report
# -------------------------------------------------
report = {}

for agent in agents:

    report[agent["id"]] = {

        "packages_delivered": 0,

        "total_distance": 0,

        "efficiency": 0,

        "total_delay": 0
    }


# -------------------------------------------------
# Package Counter
# -------------------------------------------------
package_count = 0


# -------------------------------------------------
# Simulate Deliveries
# -------------------------------------------------
print("\n========== DELIVERY ROUTES ==========\n")

for package in packages:

    package_count += 1

    # -------------------------------------------------
    # New Agent Mid-Day
    # -------------------------------------------------
    if package_count == 5:

        print(
            "\nNew Agent A4 Joined Mid-Day!\n"
        )

        agents.append({

            "id": "A4",

            "location": [50, 50]
        })

        report["A4"] = {

            "packages_delivered": 0,

            "total_distance": 0,

            "efficiency": 0,

            "total_delay": 0
        }

    warehouse_id = package["warehouse"]

    warehouse_location = warehouses[
        warehouse_id
    ]

    destination = package["destination"]

    # -------------------------------------------------
    # Find Nearest Agent
    # -------------------------------------------------
    nearest_agent, agent_distance = (
        find_nearest_agent(
            warehouse_location,
            agents
        )
    )

    # -------------------------------------------------
    # Warehouse -> Destination
    # -------------------------------------------------
    delivery_distance = (
        calculate_distance(
            warehouse_location,
            destination
        )
    )

    # -------------------------------------------------
    # Total Distance
    # -------------------------------------------------
    total_distance = (
        agent_distance +
        delivery_distance
    )

    # -------------------------------------------------
    # Random Delay
    # -------------------------------------------------
    delay = random.randint(1, 10)

    # -------------------------------------------------
    # Update Report
    # -------------------------------------------------
    report[nearest_agent][
        "packages_delivered"
    ] += 1

    report[nearest_agent][
        "total_distance"
    ] += total_distance

    report[nearest_agent][
        "total_delay"
    ] += delay

    # -------------------------------------------------
    # ASCII Route Visualization
    # -------------------------------------------------
    print(
        f"{nearest_agent} ---> "
        f"{warehouse_id} ---> "
        f"{package['id']}"
    )


# -------------------------------------------------
# Calculate Efficiency
# -------------------------------------------------
for agent_id in report:

    delivered = report[agent_id][
        "packages_delivered"
    ]

    total_distance = report[agent_id][
        "total_distance"
    ]

    if delivered > 0:

        efficiency = (
            total_distance / delivered
        )

    else:

        efficiency = 0

    report[agent_id][
        "total_distance"
    ] = round(total_distance, 2)

    report[agent_id][
        "efficiency"
    ] = round(efficiency, 2)


# -------------------------------------------------
# Find Best Agent
# -------------------------------------------------
best_agent = None

best_efficiency = float("inf")

for agent_id in report:

    delivered = report[agent_id][
        "packages_delivered"
    ]

    efficiency = report[agent_id][
        "efficiency"
    ]

    if delivered > 0:

        if efficiency < best_efficiency:

            best_efficiency = efficiency

            best_agent = agent_id


report["best_agent"] = best_agent


# -------------------------------------------------
# Save JSON Report
# -------------------------------------------------
with open("report.json", "w") as file:

    json.dump(report, file, indent=4)


# -------------------------------------------------
# Export CSV
# -------------------------------------------------
with open(
    "top_performer.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Agent",
        "Packages Delivered",
        "Total Distance",
        "Efficiency",
        "Total Delay"
    ])

    writer.writerow([

        best_agent,

        report[best_agent][
            "packages_delivered"
        ],

        report[best_agent][
            "total_distance"
        ],

        report[best_agent][
            "efficiency"
        ],

        report[best_agent][
            "total_delay"
        ]
    ])


# -------------------------------------------------
# Display Final Report
# -------------------------------------------------
print("\n========== DELIVERY REPORT ==========\n")

for agent_id, details in report.items():

    if agent_id == "best_agent":
        continue

    print(f"Agent : {agent_id}")

    print(
        f"Packages Delivered : "
        f"{details['packages_delivered']}"
    )

    print(
        f"Total Distance : "
        f"{details['total_distance']}"
    )

    print(
        f"Efficiency : "
        f"{details['efficiency']}"
    )

    print(
        f"Total Delay : "
        f"{details['total_delay']} minutes"
    )

    print("----------------------------------")


print(f"\nBest Agent : {report['best_agent']}")

print(
    "\nreport.json file created successfully!"
)

print(
    "top_performer.csv file created successfully!"
)