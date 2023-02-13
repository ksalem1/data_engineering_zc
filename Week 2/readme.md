# Week 2 - Workflow Orchestration using Prefect


During this week the aim was to orchestrate a job that is able to ingest web data to a Data Lake in it's raw form.

## Data Lake

Started off by defining and knowing what a data lake is, how its use cases are different to that of a Data Warehouse. A Data Lake is a repository which holds Big Data from many sources, which include structured, semi-structured, and unstructured data.

### Data Lake Use Cases
* Ingest Unstructured and Structured data
* Stores, secures, and protects data at unlimited scales
* Connects data with analytics and machine learning tools
* Allows us to store and access data quickly, without thinking about schemas

Additionally, data lakes contain huge amounts of data, sometimes ingesting data everyday. In Data Warehousing, data is usually structured, and data size is relatively small.

### ELT vs ETL
**ELT stands for Extract, Load, Transform while ETL is Extract, Transform, Load**
ELT provides data lake support (schema on read). It is used for large amounts of data.

### Data Lake Providers

Cloud providers provide data lakes solutions.
* Azure - Azure Blob
* AWS - S3
* GCP - Cloud Storage

### Orchestration of Workflow
This week, data will be fetched from the a web source, downloaded locally as a flat file. Afterwards, data will be converted from its CSV format into a more effective and efficient format - Parquet. This file will then be taken and upload to Google Cloud Storage (data lake). We will then copy this to Google Biq Query (data warehouses) so that we would be able to query it using SQL.

The tool used in managing this data flow is Prefect. Prefect allows us to orchestrate and observe your dataflow using Prefect's open source Python library, the glue of the modern data stack. Moreover, it can aid in scheduling, executing and visualizing data workflows. Below are some code snippets of working with Prefect

    # Install package
    pip install prefect==2.7.7

    # Run prefect server and UI
    prefect orion start

    # Create a deployment 
    prefect deployment build flows/file_name.py:flow_name -n "deployment-name"

    # Apply the deployment
    prefect deployment apply deployment-name-deployment.yaml

    # Create Work Queues
    prefect agent start  --work-queue "default"
