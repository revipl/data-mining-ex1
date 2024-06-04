import os
import json
import names
import numpy as np
import random

# Create the output directory if it doesn't exist
output_dir = "../../output/problem1"
os.makedirs(output_dir, exist_ok=True)

PROJECTS_NUM = 300

# Generate dummy data with projects
projects = []
for i in range(PROJECTS_NUM):
    project = {
        "id": str(i),
        "url": f"http://something/{i}",
        "Creators": f"{names.get_full_name()}",
        "Title": f"Project {i}",
        "Text": f"Description for project {i}",
        "DollarsPledged": np.random.randint(0, 50000),
        "DollarsGoal": np.random.randint(0, 100000),
        "NumBackers": np.random.randint(0, 2000),
        "DaysToGo": np.random.randint(0, 100),
        "FlexibleGoal": bool(random.getrandbits(1))
    }
    projects.append(project)

# Create the final JSON structure
data = {
    "records": {
        "record": projects
    }
}

# Save the generated data to a JSON file
output_file = os.path.join(output_dir, "dummy.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Dummy data generated and saved to {output_file}")
