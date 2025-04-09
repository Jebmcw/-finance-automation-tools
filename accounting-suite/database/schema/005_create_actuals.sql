
CREATE TABLE actuals (
    id           NUMBER PRIMARY KEY,
    cost_center  NUMBER(12),
    account      NUMBER(12),
    period       DATE,
    amount       NUMBER(12)
);
