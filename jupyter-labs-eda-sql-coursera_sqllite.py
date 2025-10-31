!pip install sqlalchemy==1.3.9


!pip install ipython-sql
!pip install ipython-sql prettytable

%load_ext sql

import csv, sqlite3
import prettytable
prettytable.DEFAULT = 'DEFAULT'

con = sqlite3.connect("my_data1.db")
cur = con.cursor()

!pip install -q pandas

%sql sqlite:///my_data1.db

import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

#DROP THE TABLE IF EXISTS

%sql DROP TABLE IF EXISTS SPACEXTABLE;

%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null

%sql SELECT DISTINCT "Launch_Site" FROM SPACEXTABLE;

%sql SELECT * FROM SPACEXTABLE WHERE "Launch_Site" LIKE 'CCA%' LIMIT 5;

%sql SELECT SUM("Payload_Mass") AS Total_NASA_Payload FROM SPACEXTABLE WHERE "Customer" = 'NASA (CRS)';

%sql SELECT AVG("Payload_Mass") AS Avg_Payload FROM SPACEXTABLE WHERE "Booster_Version" = 'F9 v1.1';

%sql SELECT MIN("Date") AS First_Successful_Ground_Landing FROM SPACEXTABLE WHERE "Landing_Outcome" LIKE 'Success (ground pad)%';

%sql SELECT DISTINCT "Booster_Version" FROM SPACEXTABLE WHERE "Landing_Outcome" LIKE 'Success (drone ship)%' AND "Payload_Mass" > 4000 AND "Payload_Mass" < 6000;

%sql SELECT CASE WHEN "Mission_Outcome" = 'Success' THEN 'Successful' ELSE 'Failure' END AS Outcome_Type, COUNT(*) AS Count FROM SPACEXTABLE GROUP BY CASE WHEN "Mission_Outcome" = 'Success' THEN 'Successful' ELSE 'Failure' END;

%sql SELECT DISTINCT "Booster_Version" FROM SPACEXTABLE WHERE "Payload_Mass" = (SELECT MAX("Payload_Mass") FROM SPACEXTABLE);

%sql SELECT substr(Date, 6, 2) AS Month, "Booster_Version", "Launch_Site", "Landing_Outcome" FROM SPACEXTABLE WHERE substr(Date, 0, 5) = '2015' AND "Landing_Outcome" LIKE 'Failure (drone ship)%';

%sql SELECT substr(Date, 6, 2) AS Month, "Booster_Version", "Launch_Site", "Landing_Outcome" FROM SPACEXTABLE WHERE substr(Date, 0, 5) = '2015' AND "Landing_Outcome" LIKE 'Failure (drone ship)%';

