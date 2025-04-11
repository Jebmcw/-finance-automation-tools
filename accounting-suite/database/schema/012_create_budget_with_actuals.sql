
CREATE TABLE match_budget (
    id           NUMBER PRIMARY KEY,
    cost_center  NUMBER(12),
    account      NUMBER(12),
    amount       NUMBER(12),
    period       DATE
);