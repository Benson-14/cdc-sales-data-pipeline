# 📦 Real-Time CDC Data Pipeline for Gadgets Sales Analysis

This project demonstrates a **real-time Change Data Capture (CDC) data pipeline** built on AWS to process, transform, and analyze mock sales data for electronic gadgets.

---

## 🚀 Overview

The system simulates real-world e-commerce sales using a Python-based mock data generator that writes to **DynamoDB**. Any changes (INSERT/MODIFY) in the table are captured and streamed via an **EventBridge Pipe** to **Kinesis Data Streams**, then transformed using **AWS Lambda**, stored in **Amazon S3**, cataloged using **AWS Glue**, and finally queried using **Amazon Athena**.

---

## 🧩 Architecture Diagram

![CDC Architecture](./assets/cdc-sales-data-pipeline-light.svg)

---

## 🛠️ Components Used

| Component              | Purpose |
|------------------------|---------|
| 🐍 Python Script        | Simulates mock gadget sales and writes to DynamoDB |
| 🧾 DynamoDB            | Stores sales orders as raw data |
| 🔄 EventBridge Pipe     | Listens to DynamoDB stream and routes events to Kinesis |
| 🌊 Kinesis Data Stream | Acts as a buffer to handle streaming data |
| 🔥 Kinesis Firehose     | Triggers Lambda and delivers transformed data to S3 |
| 🧠 Lambda Function     | Transforms and flattens the raw CDC records |
| 🪣 Amazon S3           | Stores the transformed data in newline-delimited JSON format |
| 🧬 AWS Glue            | Crawls and catalogs the transformed data |
| 🔍 Amazon Athena       | Enables querying the data using standard SQL |

---

## 🔁 Data Flow Summary

1. Python script inserts and updates orders in **DynamoDB**.
2. **DynamoDB Streams** send CDC events to **EventBridge Pipe**.
3. **EventBridge Pipe** forwards events to **Kinesis Data Stream**.
4. Events are passed to **Kinesis Firehose** which invokes a **Lambda function**.
5. Lambda transforms and encodes the data before passing it back to Firehose.
6. Transformed data is stored in **S3**.
7. **AWS Glue Crawler** runs periodically to catalog the data.
8. **Athena** is used to run SQL queries and analyze the sales.

---

## 📂 Folder Structure

```
📁 assets/
    └── png-sales.drawio.png      # Architecture diagram

📁 lambda/
    └── transform_function.py     # Lambda function code

📁 generator/
    └── new_mock_generator.py     # Python mock data generator

📄 README.md
```

---

## 📊 Sample Athena Table (After Glue Crawler)

```sql
SELECT * FROM gadgets_sales_db.sales_data_table
WHERE payment_method = 'UPI'
ORDER BY order_timestamp DESC;
```

---

## ✅ Features

- Real-time data ingestion and transformation
- CDC handling with DynamoDB Streams
- Serverless architecture
- Queryable data lake via Athena

---

## 📌 Note

Ensure that:
- The Lambda function handles `base64` encoding/decoding properly
- Proper IAM permissions are configured for EventBridge, Firehose, Lambda, and Glue
- Timestamps are in a consistent format for Athena queries
