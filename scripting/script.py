# ADD CODE HERE
# change script to whatever language you are comfortable with
###################################################
# how to run
#must have python3 installed in your computer
#give command like 
#python scripting/script.py scripting/tfplan.json
#################################################

import json
import sys

filename = sys.argv[1]

#Load the JSON file
with open(filename, "r") as f:
    plan = json.load(f)

violations = []

#Loop through each resource change in the plan
for resource in plan.get("resource_changes", []):
    address = resource.get("address")
    actions = resource.get("change", {}).get("actions", [])
    before = resource.get("change", {}).get("before") or {}
    after = resource.get("change", {}).get("after") or {}

    #ignore create
    if actions == ["create"] or actions == ["read"]:
        continue

    #catch delete action
    if "delete" in actions:
        violations.append(f"Resource '{address}' is being deleted.")
        continue

    #handle update actions
    if actions == ["update"]:
        # Check if anything besides "tags" changed
        for key in set(list(before.keys()) + list(after.keys())):
            if key != "tags" and before.get(key) != after.get(key):
                violations.append(f"Resource '{address}' modifies non-tag attribute '{key}'.")

        # Check if any tag besides "GitCommitHash" changed
        before_tags = before.get("tags") or {}
        after_tags = after.get("tags") or {}
        for tag in set(list(before_tags.keys()) + list(after_tags.keys())):
            if tag != "GitCommitHash" and before_tags.get(tag) != after_tags.get(tag):
                violations.append(f"Resource '{address}' modifies disallowed tag '{tag}'.")

#printing result
print("----------------------------------------")
if violations:
    print("Plan REJECTED. Do not proceed with apply.\n")
    print("Forbidden actions detected:")
    for v in violations:
        print(f" - {v}")
    sys.exit(1)
else:
    print("RESULT: Plan APPROVED. Proceed with apply.")
    sys.exit(0)