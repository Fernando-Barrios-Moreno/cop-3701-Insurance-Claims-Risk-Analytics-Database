from nicegui import ui
import oracledb

oracledb.init_oracle_client(
    lib_dir="/workspaces/cop-3701-Insurance-Claims-Risk-Analytics-Database/instantclient_21_12"
)

USERNAME = "FERNANDOPAULBARRI_SCHEMA_4O4M7"
PASSWORD = "92LXC9OMBNFIPFZHCZLr3KGC257!DE"
DSN = "db.freesql.com:1521/23ai_34ui2"


def get_connection():
    return oracledb.connect(
    user=USERNAME,
    password=PASSWORD,
    dsn=DSN
    )

def view_policies(policyholder_id, output):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT policy_id, policy_type, start_date, end_date, premium_amount
    FROM Policy
    WHERE policyholder_id = :id
    """

    cursor.execute(query, id=policyholder_id)
    rows = cursor.fetchall()

    output.clear()

    with output:
        if not rows:
            ui.label("No policies found.")
        for row in rows:
            ui.label(f"Policy ID: {row[0]}")
            ui.label(f"Type: {row[1]}")
            ui.label(f"Start Date: {row[2].strftime('%Y-%m-%d') if row[2] else 'N/A'}")
            ui.label(f"End Date: {row[3].strftime('%Y-%m-%d') if row[3] else 'N/A'}")
            ui.label(f"Premium: ${row[4]}")
            ui.separator()

    conn.close()

def view_claims(policy_id, output):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT c.claim_id, c.claim_date, c.total_charges, pc.status, pc.approval_date
    FROM Claim c
    JOIN PolicyClaim pc ON c.claim_id = pc.claim_id
    WHERE pc.policy_id = :id
    """

    cursor.execute(query, id=policy_id)
    rows = cursor.fetchall()

    output.clear()

    with output:
        if not rows:
            ui.label("No claims found.")
        for row in rows:
            ui.label(f"Claim ID: {row[0]}")
            ui.label(f"Claim Date: {row[1].strftime('%Y-%m-%d') if row[1] else 'N/A'}")
            ui.label(f"Total Charges: ${row[2]}")
            ui.label(f"Status: {row[3]}")
            ui.label(f"Approval Date: {row[4].strftime('%Y-%m-%d') if row[4] else 'N/A'}")
            ui.separator()

    conn.close()

def fraud_risk(threshold, output):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT claim_id, claim_date, total_charges, fraud_risk_score
    FROM Claim
    WHERE fraud_risk_score > :t
    """

    cursor.execute(query, t=float(threshold))
    rows = cursor.fetchall()

    output.clear()

    with output:
        if not rows:
            ui.label("No high-risk claims found.")
        for row in rows:
            ui.label(f"Claim ID: {row[0]}")
            ui.label(f"Date: {row[1].strftime('%Y-%m-%d') if row[1] else 'N/A'}")
            ui.label(f"Charges: ${row[2]}")
            ui.label(f"Fraud Risk Score: {row[3]}")
            ui.separator()

    conn.close()

def investigations(output):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT fi.investigation_id, fi.investigation_date, fi.fraud_flag,
           a.first_name, a.last_name, fi.claim_id
    FROM FraudInvestigation fi
    JOIN Analyst a ON fi.analyst_id = a.analyst_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    output.clear()

    with output:
        if not rows:
            ui.label("No investigations found.")
        for row in rows:
            ui.label(f"Investigation ID: {row[0]}")
            ui.label(f"Date: {row[1].strftime('%Y-%m-%d') if row[1] else 'N/A'}")
            ui.label(f"Fraud Flag: {'Yes' if row[2] == 1 else 'No'}")
            ui.label(f"Analyst: {row[3]} {row[4]}")
            ui.label(f"Claim ID: {row[5]}")
            ui.separator()

    conn.close()

def dependents(policyholder_id, output):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT name, relationship, age
    FROM Dependent
    WHERE policyholder_id = :id
    """

    cursor.execute(query, id=policyholder_id)
    rows = cursor.fetchall()

    output.clear()

    with output:
        if not rows:
            ui.label("No dependents found.")
        for row in rows:
            ui.label(f"Name: {row[0]}")
            ui.label(f"Relationship: {row[1]}")
            ui.label(f"Age: {row[2]}")
            ui.separator()

    conn.close()


ui.label("Insurance Database System").classes("text-h4")

output = ui.column()

with ui.card():
    ph_input = ui.input("Policyholder ID")
    ui.button("View Policies", on_click=lambda: view_policies(ph_input.value, output))

with ui.card():
    policy_input = ui.input("Policy ID")
    ui.button("View Claims", on_click=lambda: view_claims(policy_input.value, output))

with ui.card():
    threshold_input = ui.input("Fraud Threshold")
    ui.button("High Fraud Claims", on_click=lambda: fraud_risk(threshold_input.value, output))

with ui.card():
    ui.button("View Investigations", on_click=lambda: investigations(output))

with ui.card():
    dep_input = ui.input("Policyholder ID")
    ui.button("View Dependents", on_click=lambda: dependents(dep_input.value, output))

ui.run(port=8081)