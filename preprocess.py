import csv
import os
import random
from datetime import datetime, timedelta

# Create data folder
os.makedirs("data", exist_ok=True)

# Input file (paste your dataset into this file)
INPUT_FILE = "data/raw_data.csv"

# Output files
policyholder_file = "data/policyholder.csv"
policy_file = "data/policy.csv"
claim_file = "data/claim.csv"
policyclaim_file = "data/policyclaim.csv"
dependent_file = "data/dependent.csv"
analyst_file = "data/analyst.csv"
fraud_file = "data/fraudinvestigation.csv"

# Helper functions
def random_date(start_year=2020, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# Create analysts (static small set)
analysts = []
for i in range(1, 6):
    analysts.append([i, f"Analyst{i}", f"Last{i}", "Fraud Dept"])

# Write analysts
with open(analyst_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["analyst_id", "first_name", "last_name", "department"])
    writer.writerows(analysts)

policyholders = []
policies = []
claims = []
policyclaims = []
dependents = []
frauds = []

dependent_id = 1
policy_id = 1
claim_id = 1
investigation_id = 1

with open(INPUT_FILE, "r") as f:
    reader = csv.DictReader(f)

    for idx, row in enumerate(reader, start=1):

        # -------------------------
        # PolicyHolder
        # -------------------------
        policyholders.append([
            idx,
            f"First{idx}",
            f"Last{idx}",
            int(row["age"]),
            "Male" if row["sex"] == "1" else "Female",
            float(row["bmi"]),
            int(row["smoker"]),
            f"Region{row['region']}"
        ])

        # -------------------------
        # Policy
        # -------------------------
        start_date = random_date()
        end_date = start_date + timedelta(days=365)

        policies.append([
            policy_id,
            idx,
            "Health",
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            round(random.uniform(200, 1000), 2)
        ])

        # -------------------------
        # Claim
        # -------------------------
        claim_date = random_date()

        claims.append([
            claim_id,
            claim_date.strftime("%Y-%m-%d"),
            float(row["charges"]),
            int(row["insuranceclaim"]),
            round(random.uniform(0, 1), 2)
        ])

        # -------------------------
        # PolicyClaim
        # -------------------------
        policyclaims.append([
            policy_id,
            claim_id,
            "Approved" if row["insuranceclaim"] == "1" else "Denied",
            claim_date.strftime("%Y-%m-%d")
        ])

        # -------------------------
        # Dependents (based on children)
        # -------------------------
        num_children = int(row["children"])
        for c in range(num_children):
            dependents.append([
                dependent_id,
                idx,
                f"Child{dependent_id}",
                "Child",
                random.randint(1, 18)
            ])
            dependent_id += 1

        # -------------------------
        # Fraud Investigation (only some claims)
        # -------------------------
        if random.random() < 0.3:  # 30% chance
            analyst = random.choice(analysts)
            frauds.append([
                investigation_id,
                claim_id,
                analyst[0],
                claim_date.strftime("%Y-%m-%d"),
                random.choice([0, 1]),
                "Auto-generated investigation"
            ])
            investigation_id += 1

        policy_id += 1
        claim_id += 1

# -------------------------
# Write CSV Files
# -------------------------

def write_csv(filename, header, data):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

write_csv(policyholder_file,
          ["policyholder_id", "first_name", "last_name", "age", "sex", "bmi", "smoker", "region"],
          policyholders)

write_csv(policy_file,
          ["policy_id", "policyholder_id", "policy_type", "start_date", "end_date", "premium_amount"],
          policies)

write_csv(claim_file,
          ["claim_id", "claim_date", "total_charges", "claim_occured", "fraud_risk_score"],
          claims)

write_csv(policyclaim_file,
          ["policy_id", "claim_id", "status", "approval_date"],
          policyclaims)

write_csv(dependent_file,
          ["dependent_id", "policyholder_id", "name", "relationship", "age"],
          dependents)

write_csv(fraud_file,
          ["investigation_id", "claim_id", "analyst_id", "investigation_date", "fraud_flag", "notes"],
          frauds)

print("CSV files generated in /data folder")