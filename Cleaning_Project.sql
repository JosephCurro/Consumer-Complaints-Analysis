SELECT COUNT(*)
FROM consumer_complaints
;

-- Confirming character count uniformity of specific
-- columns that should be constant. Min and max values should be identical
SELECT MAX(CHAR_LENGTH(State)) Max_State,
	MIN(CHAR_LENGTH(State)) Min_State,
    MAX(CHAR_LENGTH(ZIP)) Max_ZIP,
    MIN(CHAR_LENGTH(ZIP)) Min_ZIP,
    MAX(CHAR_LENGTH(Complaint_ID)) Max_ID,
	MIN(CHAR_LENGTH(Complaint_ID)) Min_ID
FROM consumer_complaints
;

-- Creating a duplicate table to work on while keeping the original dataset unaltered
CREATE TABLE worksheet (
	Date_Received VARCHAR(15),
    Product VARCHAR(100),
    Sub_Product VARCHAR(100),
    Issue VARCHAR(255),
    Sub_Issue VARCHAR(255),
    Consumer_Narrative TEXT,
    Company_Response_Pub VARCHAR(255),
    Company VARCHAR(255),
    State CHAR(2),
    ZIP CHAR(5),
    Tags VARCHAR(255),
    Consumer_Consent VARCHAR(50),
    Submitted VARCHAR(50),
    Date_Submitted VARCHAR(15),
    Company_Response_Con VARCHAR(255),
    Timely_Response VARCHAR(50),
    Consumer_Disputed VARCHAR(255),
    Complaint_ID CHAR(7)
)
;

INSERT INTO worksheet 
SELECT *
FROM consumer_complaints
;

-- confirming table duplicated properly
DESCRIBE TABLE worksheet
;
SELECT *
FROM worksheet
;
SELECT COUNT(*) 
FROM worksheet
;

-- Identifying any columns with blank or null values
SELECT COUNT(*) AS Total_Rows,
 	SUM(CASE WHEN Date_Received IS NULL OR Date_Received = '' THEN 1 ELSE 0 END) AS Null_Blank_Date_Received,
    SUM(CASE WHEN Product IS NULL OR Product = '' THEN 1 ELSE 0 END) AS Null_Blank_Product,
	SUM(CASE WHEN Sub_Product IS NULL OR Sub_Product = '' THEN 1 ELSE 0 END) AS Null_Blank_Sub_Product,
    SUM(CASE WHEN Issue IS NULL OR Issue = '' THEN 1 ELSE 0 END) AS Null_Blank_Issue,
    SUM(CASE WHEN Sub_Issue IS NULL OR Sub_Issue = '' THEN 1 ELSE 0 END) AS Null_Blank_Sub_Issue,
    SUM(CASE WHEN Consumer_Narrative IS NULL OR Consumer_Narrative = '' THEN 1 ELSE 0 END) AS Null_Blank_Narrative,
    SUM(CASE WHEN Company_Response_Pub IS NULL OR Company_Response_Pub = '' THEN 1 ELSE 0 END) AS Null_Blank_Public_Response,
    SUM(CASE WHEN Company IS NULL OR Company = '' THEN 1 ELSE 0 END) AS Null_Blank_Company,
    SUM(CASE WHEN State IS NULL OR State = '' THEN 1 ELSE 0 END) AS Null_Blank_State,
    SUM(CASE WHEN ZIP IS NULL OR ZIP = '' THEN 1 ELSE 0 END) AS Null_Blank_ZIP,
    SUM(CASE WHEN Tags IS NULL OR Tags = '' THEN 1 ELSE 0 END) AS Null_Blank_Tags,
    SUM(CASE WHEN Consumer_Consent IS NULL OR Consumer_Consent = '' THEN 1 ELSE 0 END) AS Null_Blank_Consent,
    SUM(CASE WHEN Submitted IS NULL OR Submitted = '' THEN 1 ELSE 0 END) AS Null_Blank_Submitted,
    SUM(CASE WHEN Date_Submitted IS NULL OR Date_Submitted = '' THEN 1 ELSE 0 END) AS Null_Blank_Date_Submitted,
    SUM(CASE WHEN Company_Response_Con IS NULL OR Company_Response_Con = '' THEN 1 ELSE 0 END) AS Null_Blank_Response_To_Consumer,
    SUM(CASE WHEN Timely_Response IS NULL OR Timely_Response = '' THEN 1 ELSE 0 END) AS Null_Blank_Timely_Response,
    SUM(CASE WHEN Consumer_Disputed IS NULL OR Consumer_Disputed = '' THEN 1 ELSE 0 END) AS Null_Blank_Consumer_Disputed,
    SUM(CASE WHEN Complaint_ID IS NULL OR Complaint_ID = '' THEN 1 ELSE 0 END) AS Null_Blank_Complaint_ID
FROM worksheet
;

-- No nulls or blanks detected. If there were, this would be to remove them
DELETE FROM worksheet
	WHERE
    Date_Received IS NULL -- DATE data types can't have empty strings like ''
    OR Product IS NULL OR Product = ''
	OR Sub_Product IS NULL OR Sub_Product = ''
    OR Issue IS NULL OR Issue = ''
	OR Sub_Issue IS NULL OR Sub_Issue = ''
    OR Consumer_Narrative IS NULL OR Consumer_Narrative = ''
    OR Company_Response_Pub IS NULL OR Company_Response_Pub = ''
    OR Company IS NULL OR Company = ''
    OR State IS NULL OR State = ''
    OR ZIP IS NULL OR ZIP = ''
    OR Tags IS NULL OR Tags = ''
	OR Consumer_Consent IS NULL OR Consumer_Consent = ''
    OR Submitted IS NULL OR Submitted = ''
    OR Date_Submitted IS NULL  -- DATE data types can't have empty strings like ''
    OR Company_Response_Con IS NULL OR Company_Response_Con = ''
    OR Timely_Response IS NULL OR Timely_Response = ''
    OR Consumer_Disputed IS NULL OR Consumer_Disputed = ''
    OR Complaint_ID IS NULL OR Complaint_ID = ''
;

-- Determining any columns with only one distinct entry
SELECT DISTINCT State,
	Submitted, 
	Timely_Response, 
    Consumer_Consent, 
    Consumer_Disputed, 
    Tags
FROM worksheet
;

-- The State, Submitted, Consumer_Consent, and Consumer_Disputed columns all have only one distinct value
-- Deleting them from the dataset as they don't offer insight 
ALTER TABLE worksheet
	DROP State, 
	DROP Submitted, 
    DROP Consumer_Consent,
    DROP Consumer_Disputed
;

-- Converting appropriate data types
UPDATE worksheet
	SET Date_Submitted = STR_TO_DATE(Date_Submitted, '%m/%d/%Y'),
		Date_Received = STR_TO_DATE(Date_Received, '%m/%d/%Y')
;

-- Modifying appropriate columns
-- ZIP could technically be changed to enum, but has 872 distinct entries; better suited as CHAR(5)
ALTER TABLE worksheet
	MODIFY COLUMN Date_Received date,
	MODIFY COLUMN Date_Submitted date,
	MODIFY COLUMN Timely_Response ENUM('Yes','No'),
	MODIFY COLUMN Tags ENUM('None', 'Older American', 'Servicemember', 'Older American, Servicemember')
;

-- Changing different columns to uppercase/lowercase
-- Most get UPPER() since they have a lower character count (<200)
-- Consumer_Narrative gets lowercase for legibility because of being so long on average
UPDATE worksheet
SET Date_Received = TRIM(Date_Received),
	Product = TRIM(UPPER(Product)),
	Sub_Product = TRIM(UPPER(Sub_Product)),
    Issue = TRIM(UPPER(Issue)),
    Sub_Issue = TRIM(UPPER(Sub_Issue)),
    Consumer_Narrative = TRIM(LOWER(Consumer_Narrative)),
    Company_Response_Pub = TRIM(UPPER(Company_Response_Pub)),
    Company = TRIM(UPPER(Company)),
    ZIP = TRIM(ZIP),
    Tags = TRIM(Tags),
    Date_Submitted = TRIM(Date_Submitted),
    Company_Response_Con = TRIM(UPPER(Company_Response_Con)),
    Timely_Response = TRIM(Timely_Response),
    Complaint_ID = TRIM(Complaint_ID)
;
-- Confirming each Complaint_ID is unique
-- Making Complaint_ID the primary key; is the only field with wholly unique values for each row
SELECT COUNT(Complaint_ID), 
	COUNT(DISTINCT(Complaint_ID))
FROM worksheet
;
ALTER TABLE worksheet
ADD PRIMARY KEY (Complaint_ID)
;

-- Indexing columns that can be pulled frequently in queries
-- Creating some composite indexes for same reason
CREATE INDEX idx_date_received ON worksheet(Date_Received);
CREATE INDEX idx_product ON worksheet(Product);
CREATE INDEX idx_issue ON worksheet(Issue);
CREATE INDEX idx_company ON worksheet(Company);
CREATE INDEX idx_zip ON worksheet(ZIP);
CREATE INDEX idx_date_submitted ON worksheet(Date_Submitted);

