CREATE TABLE gl_vs_ap(
    id           NUMBER PRIMARY KEY,
    account       NUMBER(12),
    company_code   NUMBER(12),
    ap_amount      NUMBER(12),
    gl_amount       NUMBER(12),
    matched       VARCHAR2(10)
    
);