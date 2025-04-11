
CREATE TABLE bank_vs_book (
    id           NUMBER PRIMARY KEY,
    bank_account VARCHAR2(50),
    amount_bank   NUMBER(12),
    amount_book   NUMBER(12),
    matched       VARCHAR2(10)
    
);