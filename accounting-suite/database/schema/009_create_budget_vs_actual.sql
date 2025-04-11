CREATE TABLE budget_vs_actual(
    id           NUMBER PRIMARY KEY,
    cost_center     NUMBER(12),
    account         NUMBER(12),
    actuals_amount     NUMBER(12),
    budget_amount       NUMBER(12),
    matched       VARCHAR2(10)
    
);