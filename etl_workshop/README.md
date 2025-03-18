# AWS ETL Workshop

This workshop demonstrates how to use AWS Glue to ingest customer and order data from S3 into an RDS database, and how to display the data using a Python Flask app running on EC2.

## Steps
1. **Set up AWS Glue**: Create a Glue job to ingest JSON files from S3 into a database.
2. **Create a Database**: Use Amazon RDS (PostgreSQL) to store the ingested data.
3. **Python App**: Develop a Flask app to query and display the data, which will run on an EC2 instance.

## Files
- `glue_etl_script.py`: AWS Glue ETL script to ingest data from S3 into RDS.
- `app.py`: Flask app to display data from the RDS database.
- `templates/index.html`: HTML template to render the data in a table.
