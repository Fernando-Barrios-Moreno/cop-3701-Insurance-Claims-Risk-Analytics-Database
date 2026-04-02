import oracledb
import csv
import os

oracledb.init_oracle_client(
    lib_dir=r"C:\oracle\instantclient_11_2"
)
# -----------------------------
# DATABASE CONNECTION CONFIG
# -----------------------------
USERNAME = "FERNANDOPAULBARRI_SCHEMA_4O4M7"
PASSWORD = "92LXC9OMBNFIPFZHCZLr3KGC257!DE"
DSN = "db.freesql.com:1521/23ai_34ui2"

# -----------------------------
# CONNECT TO ORACLE
# -----------------------------
connection = oracledb.connect(
    user=USERNAME,
    password=PASSWORD,
    dsn=DSN
)

cursor = connection.cursor()

DATA_DIR = "data"

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def load_csv(file_name, insert_query):
    file_path = os.path.join(DATA_DIR, file_name)

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            cursor.execute(insert_query, row)

    connection.commit()
    print(f"Loaded {file_name}")

# -----------------------------
# LOAD DATA (ORDER MATTERS)
# -----------------------------

# 1. PolicyHolder
load_csv(
    "policyholder.csv",
    """
    INSERT INTO PolicyHolder 
    (policyholder_id, first_name, last_name, age, sex, bmi, smoker, region)
    VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
    """
)

# 2. Analyst
load_csv(
    "analyst.csv",
    """
    INSERT INTO Analyst 
    (analyst_id, first_name, last_name, department)
    VALUES (:1, :2, :3, :4)
    """
)

# 3. Policy
load_csv(
    "policy.csv",
    """
    INSERT INTO Policy 
    (policy_id, policyholder_id, policy_type, start_date, end_date, premium_amount)
    VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), TO_DATE(:5, 'YYYY-MM-DD'), :6)
    """
)

# 4. Claim
load_csv(
    "claim.csv",
    """
    INSERT INTO Claim 
    (claim_id, claim_date, total_charges, claim_occured, fraud_risk_score)
    VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5)
    """
)

# 5. Dependent
load_csv(
    "dependent.csv",
    """
    INSERT INTO Dependent 
    (dependent_id, policyholder_id, name, relationship, age)
    VALUES (:1, :2, :3, :4, :5)
    """
)

# 6. PolicyClaim
load_csv(
    "policyclaim.csv",
    """
    INSERT INTO PolicyClaim 
    (policy_id, claim_id, status, approval_date)
    VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))
    """
)

# 7. FraudInvestigation
load_csv(
    "fraudinvestigation.csv",
    """
    INSERT INTO FraudInvestigation 
    (investigation_id, claim_id, analyst_id, investigation_date, fraud_flag, notes)
    VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6)
    """
)

# -----------------------------
# CLOSE CONNECTION
# -----------------------------
cursor.close()
connection.close()

print("All data loaded successfully!")