CREATE TABLE PolicyHolder (
    policyholder_id INT PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    age INT NOT NULL,
    sex VARCHAR2(10) NOT NULL,
    bmi NUMBER(5,2),
    smoker NUMBER(1) NOT NULL, -- 1 = TRUE, 0 = FALSE
    region VARCHAR2(50) NOT NULL
);

--------------------------------------------------
-- Policy
--------------------------------------------------
CREATE TABLE Policy (
    policy_id INT PRIMARY KEY,
    policyholder_id INT NOT NULL,
    policy_type VARCHAR2(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    premium_amount NUMBER(10,2) NOT NULL,
    CONSTRAINT fk_policyholder
        FOREIGN KEY (policyholder_id)
        REFERENCES PolicyHolder(policyholder_id)
);

--------------------------------------------------
-- Dependent
--------------------------------------------------
CREATE TABLE Dependent (
    dependent_id INT PRIMARY KEY,
    policyholder_id INT NOT NULL,
    name VARCHAR2(100) NOT NULL,
    relationship VARCHAR2(50) NOT NULL,
    age INT,
    CONSTRAINT fk_dependent_policyholder
        FOREIGN KEY (policyholder_id)
        REFERENCES PolicyHolder(policyholder_id)
);

--------------------------------------------------
-- Claim
--------------------------------------------------
CREATE TABLE Claim (
    claim_id INT PRIMARY KEY,
    claim_date DATE NOT NULL,
    total_charges NUMBER(10,2) NOT NULL,
    claim_occured NUMBER(1) NOT NULL, -- 1 = TRUE, 0 = FALSE
    fraud_risk_score NUMBER(5,2)
);

--------------------------------------------------
-- Analyst
--------------------------------------------------
CREATE TABLE Analyst (
    analyst_id INT PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    department VARCHAR2(50) NOT NULL
);

--------------------------------------------------
-- PolicyClaim (Bridge Table)
--------------------------------------------------
CREATE TABLE PolicyClaim (
    policy_id INT NOT NULL,
    claim_id INT NOT NULL,
    status VARCHAR2(50) NOT NULL,
    approval_date DATE,
    PRIMARY KEY (policy_id, claim_id),
    CONSTRAINT fk_policyclaim_policy
        FOREIGN KEY (policy_id)
        REFERENCES Policy(policy_id),
    CONSTRAINT fk_policyclaim_claim
        FOREIGN KEY (claim_id)
        REFERENCES Claim(claim_id)
);

--------------------------------------------------
-- FraudInvestigation
--------------------------------------------------
CREATE TABLE FraudInvestigation (
    investigation_id INT PRIMARY KEY,
    claim_id INT NOT NULL,
    analyst_id INT NOT NULL,
    investigation_date DATE NOT NULL,
    fraud_flag NUMBER(1) NOT NULL, -- 1 = TRUE, 0 = FALSE
    notes CLOB,
    CONSTRAINT fk_investigation_claim
        FOREIGN KEY (claim_id)
        REFERENCES Claim(claim_id),
    CONSTRAINT fk_investigation_analyst
        FOREIGN KEY (analyst_id)
        REFERENCES Analyst(analyst_id)
);