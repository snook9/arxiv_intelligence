-- Zeppelin server: http://zep-1.au.adaltas.cloud:9995

%jdbc(hive)
-- Username configuration
SET hivevar:username=cassaing;

%jdbc(hive)
-- Create a table
CREATE EXTERNAL TABLE cs_2022_spring_1.${username}_project (
  entry_id STRING,
  updated STRING,
  published STRING,
  title STRING,
  authors STRING,
  summary STRING,
  comment STRING,
  journal_ref STRING,
  doi STRING,
  primary_category STRING,
  categories STRING,
  pdf_url STRING,
  number_of_pages INT,
  raw_info STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
STORED AS TEXTFILE
LOCATION '/education/cs_2022_spring_1/j.cassaing-cs/project/'
TBLPROPERTIES ('skip.header.line.count'='1');

%jdbc(hive)
-- Check the table creation
SHOW TABLES IN cs_2022_spring_1;

%jdbc(hive)
-- Check the data
SELECT * FROM cs_2022_spring_1.${username}_project LIMIT 10;
