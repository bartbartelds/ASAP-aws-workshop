import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data from S3
datasource = glueContext.create_dynamic_frame.from_catalog(database = "your_database", table_name = "your_table")

# Write data to RDS
datasink = glueContext.write_dynamic_frame.from_catalog(frame = datasource, database = "your_database", table_name = "your_table")

job.commit()
