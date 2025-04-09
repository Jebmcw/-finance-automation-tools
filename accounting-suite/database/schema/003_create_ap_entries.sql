
CREATE TABLE ap_entries (
    id           NUMBER PRIMARY KEY,
    vendor_id    VARCHAR2(50),
    account      NUMBER(12),
    company_code NUMBER(12),
    amount       NUMBER(12),
    period       DATE,
    status       VARCHAR2(50)
);
