CREATE TABLE book_cash (
    id           NUMBER PRIMARY KEY,
    bank_account VARCHAR2(50),
    txn_date     DATE,
    amount       NUMBER(12, 2),
    description  VARCHAR2(255),
    cleared_flag VARCHAR2(5)  -- allows values like 'yes', 'no'
);
ALTER TABLE book_cash MODIFY cleared_flag VARCHAR2(5);