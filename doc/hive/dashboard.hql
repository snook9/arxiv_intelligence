-- Primary categories
%jdbc(hive)
-- This PIE chart shows articles by primary category
SELECT primary_category, COUNT(primary_category) AS number FROM cs_2022_spring_1.cassaing_project GROUP by primary_category;

-- Publication of articles over time
%jdbc(hive)
-- This chart shows articles publication over time, by day
SELECT published, COUNT(published) AS number FROM cs_2022_spring_1.cassaing_project GROUP by published;

-- Number of documents in relation to their size
%jdbc(hive)
SELECT number_of_pages, COUNT(number_of_pages) AS number FROM cs_2022_spring_1.cassaing_project GROUP BY number_of_pages ORDER BY number_of_pages;

-- Average page number
%jdbc(hive)
SELECT AVG(number_of_pages) AS AVG_NB_PAGES FROM cs_2022_spring_1.cassaing_project;