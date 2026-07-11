from pyspark.sql import SparkSession
from pyspark.sql.functions import sum


def process_data_with_spark(input_path):

    print("\n========== PySpark Processing ==========")

    # Create Spark Session
    spark = (
        SparkSession.builder
        .appName("FinFlow ETL Pipeline")
        .getOrCreate()
    )

    print("✅ Spark Session Created!")

    # Read CSV
    df = spark.read.csv(
        input_path,
        header=True,
        inferSchema=True
    )

    print("✅ Dataset Loaded Successfully!")

    # Total Records
    total_records = df.count()
    print(f"\nTotal Records : {total_records}")

    # Total Columns
    print(f"Total Columns : {len(df.columns)}")

    # Schema
    print("\n========== Schema ==========")
    df.printSchema()

    # Preview
    print("\n========== First 5 Rows ==========")
    df.show(5)

    # Fraud Count
    fraud_count = df.filter(df.isFraud == 1).count()

    print(f"\nFraud Transactions : {fraud_count}")

    # Transaction Type Counts
    print("\n========== Transaction Types ==========")
    df.groupBy("type").count().show()

    # Total Amount
    print("\n========== Total Transaction Amount ==========")

    total_amount = df.select(
        sum("amount")
    ).collect()[0][0]

    print(total_amount)

    print("\n✅ PySpark Processing Completed!")

    spark.stop()