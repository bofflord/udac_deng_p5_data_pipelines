# Udacity Project: Data Pipelines
This educational project is about enabling data analysis in a fictional startup called Sparkify. An ETL pipeline that uses Apache Airflow as workflow management platform:
- extracts user activity and 
- song data from AWS S3, 
- stages them in AWS Redshift, 
- transforms data into a set of dimensional tables for the analytics team and
- performs data quality checks.

**Data analysis enablement goals**  
- load data from S3 
- query song play data, meaning songs that users are listing to.  

**Initial situation**
- no easy way to query song play data due to source data structure.  
- directory of JSON logs on user activity on the app.  
- directory with JSON metadata on the songs in their app.  


## Purpose of database and design
The purpose of this AWS Redshift database is to ease queries on song play data. The stored data is extracted from JSON user log files and JSON song metadata files.  
The database design follows a classic star structure. The fact table at the center is "songplays". It references 4 dimension tables: users, songs, artists, time. Additionally there are two staging tables for data load from the S3 source.

### Fact table "songplays"
As mentioned above this is fact table which enables easy queries on songs that users are listing to.  
Its elements (column_name data_type) are:  
- songplay_id INT IDENTITY(0,1) PRIMARY KEY: automatically generated for each load from a user log file.
- start_time TIMESTAMP REFERENCES time(start_time): reference to fact table "time"
- user_id INT REFERENCES users(user_id): reference to fact table "users"
- level VARCHAR NOT NULL
- song_id VARCHAR REFERENCES songs(song_id): reference to fact table "songs"
- artist_id VARCHAR REFERENCES artists(artist_id): reference to fact table "artist_id"
- session_id INT
- location VARCHAR
- user_agent VARCHAR

### Dimension table "users"
Dimension table that stores user data.
- user_id INT NOT NULL PRIMARY KEY,\
- first_name VARCHAR,\
- last_name VARCHAR,\
- gender VARCHAR,\
- level VARCHAR NOT NULL
                                                        
### Dimension table "songs"
Dimension table that stores song data.
- song_id VARCHAR NOT NULL PRIMARY KEY,\
- title VARCHAR,\
- artist_id VARCHAR NOT NULL,\
- year INT,\
- duration NUMERIC
                                                        
### Dimension table "artists"
Dimension table that stores artist data.
- artist_id VARCHAR NOT NULL PRIMARY KEY,\
- name VARCHAR,\
- location VARCHAR,\
- latitude NUMERIC(9,5),\
- longitude NUMERIC(9,5))

### Dimension table "time"
Dimension table describes time and data information based on the provided timestamp.
- start_time TIMESTAMP NOT NULL PRIMARY KEY,\
- hour INT,\
- day INT,\
- week INT,\
- month INT,\
- year INT,\
- weekday INT

### Staging table "staging_events"
- event_raw_id INT IDENTITY(0,1) PRIMARY KEY,\
- artist VARCHAR,\
- auth VARCHAR,\
- first_name VARCHAR,\
- gender VARCHAR,\
- item_in_session INT,\
- last_name VARCHAR,\
- length NUMERIC,\
- level VARCHAR,\
- location VARCHAR,\
- method VARCHAR,\
- page VARCHAR,\
- registration VARCHAR,\
- session_id INT,\
- song VARCHAR,\
- status INT,\
- ts DOUBLE PRECISION,\
- user_agent  VARCHAR,\
- user_id INT

### Staging table "staging_songs"
- song_raw_id INT IDENTITY(0,1) PRIMARY KEY, \
- artist_id  VARCHAR,\
- artist_latitude VARCHAR,\
- artist_location VARCHAR,\
- artist_longitude VARCHAR,\
- artist_name VARCHAR,\
- duration NUMERIC,\
- num_songs INT,\
- song_id  VARCHAR,\
- title VARCHAR,\
- year INT

## Airflow Data Pipeline
- The data pipeline consists of one dag that uses 4 custom operators to perform 10 tasks.
- all SQL transformations are stored in a helper file sql_queries.py

### DAG
- DAG settings:
  - The DAG does not have dependencies on past runs.
  - On failure, the task are retried 3 times.
  - Retries happen every 5 minutes.
  - Catchup is turned off.
  - No email on retry.
- DAG tasks & operators:
	- start_operator: Dummy Operator
    - stage_events_to_redshift: Stage Operator
    - stage_songs_to_redshift: Stage Operator
	- load_songplays_table: Fact Operator
    - load_song_dimension_table: Dimension Operator
    - load_user_dimension_table: Dimension Operator
    - load_artist_dimension_table: Dimension Operator
    - load_time_dimension_table: Dimension Operator
    - run_quality_checks: Data Quality Operator
    - end_operator: Dummy Operator

### Operators
#### Stage Operator stage_redshift.py
- loads any JSON formatted files from S3 to Amazon Redshift. 
- creates and runs a SQL COPY statement based on the parameters provided. 
- The operator's parameters specify where in S3 the file is loaded and the target table in AWS Redshift.
- parameters:
	- redshift_conn_id : name of Airflow connection to AWS Redshift database.
    - aws_credentials_id : name of Airflow connection that provides AWS credentials
    - table : name of target AWS Redshift database table for copy from S3. 
    - s3_bucket : S3 bucket
    - s3_key: S3 key
    - json : COPY options for JSON (see https://docs.aws.amazon.com/redshift/latest/dg/copy-usage_notes-copy-from-json.html for details)
    - region : AWS region in which Redshift database is hosted.

#### Fact Operator load_fact.py
- creates fact table from data in staging tables.
- parameters:
	- tbd

#### Dimension Operator load_dimension.py
- creates dimension table from data in staging tables.
- parameters:
	- tbd


#### Data Quality Operator data_quality.py
- receive one or more SQL based test cases along with the expected results and execute the tests. 
- For each the test, the test result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually.
- parameters:
	- tbd

### SQL transformations
- tbd

## How to interact with project repository
This sections describes:  
- how to deploy the current project version and 
- how to further develop the project

### File and folder overview
- documentation "README.MD": this file
- configuration "dwh.cfg": contains the required credentials for a connection to the AWS Redshift database and the S3 location of the JSON source data.
- module "sql_queries.py": contains all SQL statements to 
    - create and drop tables.
    - insert records into tables.
    - copy source data from S3 into staging tables.
    - additionally the path to the S3 files is read from file dwh.cfg.
- module "create_tables.py": contains all functions to
    - drop all tables.
    - create all tables.
- module "etl.py": see section above on ETL process.

### Deployment of current project version

#### Prerequistes for connection to AWS Redshift database
In AWS the Redshift database needs to be setup and a corresponding IAM user defined. This IAM user requires a role policy that enable read-only access to the AWS S3 service. The relevent configurations for a database connection from these need to be stored in the dwh.cfg file.

#### Prerequisites for Python scripts
To run the scripts, the Python environment and packages need to be set up correctly. Required packages for modules and notebooks are:
configparser                  5.0.1
pandas                        0.23.3  
psycopg2                      2.7.4 

#### Step 1: Create database tables via module create_tables.py
Open console and navigate to project directory.   
Run command "python create_tables.py".  
Note: prerequisite is no other open database connection.  

#### Step 2: Extract data from input files, transform and load results to database via module etl.py 
Open console and navigate to project directory.   
Run command "python etl.py".  
Note: prerequisite is no other open database connection.  

### Further development
- Any further development of database will have effects on the modules sql_queries.py and etl.py. Changes in these files need to be aligned.
- Since module "create_tables" is essentially a wrapper for the SQL statements in sql_queries.py, there might not be the need to make any changes. 


## Example queries
- get number of users per level:  
``` sql
SELECT level, COUNT(DISTINCT user_id) 
FROM songplays 
GROUP BY level.
```
- Reference song title and song duration from table songs to fact table:  
``` sql
SELECT DISTINCT songplays.song_id, songplays.artist_id, songs.title, songs.duration
FROM songplays JOIN songs
ON songplays.song_id = songs.song_id
ORDER BY title
```


## OPTIONAL: Question for the reviewer
 
If you have any question about the starter code or your own implementation, please add it in the cell below. 

For example, if you want to know why a piece of code is written the way it is, or its function, or alternative ways of implementing the same functionality, or if you want to get feedback on a specific part of your code or get feedback on things you tried but did not work.

Please keep your questions succinct and clear to help the reviewer answer them satisfactorily. 

> **_Your question_**