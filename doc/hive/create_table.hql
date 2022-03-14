-- Zeppelin server: http://zep-1.au.adaltas.cloud:9995

%jdbc(hive)
-- Create a table
CREATE EXTERNAL TABLE cs_2022_spring_1.cassaing_project (
  entry_id STRING,
  updated DATE,
  published DATE,
  title STRING,
  authors STRING,
  summary STRING,
  primary_category STRING,
  categories STRING,
  pdf_url STRING,
  number_of_pages INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ";",
   "quoteChar"     = "'"
--   "escapeChar"    = "\"
)
STORED AS TEXTFILE
LOCATION '/education/cs_2022_spring_1/j.cassaing-cs/project/'
TBLPROPERTIES ('skip.header.line.count'='1')

%jdbc(hive)
-- Check the table creation
SHOW TABLES IN cs_2022_spring_1;

%jdbc(hive)
-- Check the data
SELECT * FROM cs_2022_spring_1.cassaing_project LIMIT 10;
