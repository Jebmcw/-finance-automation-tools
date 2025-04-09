
CREATE TABLE gl_entries (
    id           NUMBER PRIMARY KEY,
    account      NUMBER(12),
    company_code NUMBER(12),
    amount       NUMBER(12),
    period       DATE
);
