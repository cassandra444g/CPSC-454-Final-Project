from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, date_format, sum as spark_sum

spark = SparkSession.builder \
    .appName("ECommerceAnalysis") \
    .getOrCreate()
spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")

df = spark.read.csv("/data/data.csv", header=True, inferSchema=True)

#Remove nulls
df = df.dropna(subset=["Quantity", "UnitPrice", "InvoiceDate", "StockCode"])

#Create Revenue column
df = df.withColumn("Revenue", col("Quantity") * col("UnitPrice"))

#Total revenue per product
product_revenue = df.groupBy("StockCode").agg(spark_sum("Revenue").alias("TotalRevenue"))
product_revenue.orderBy(col("TotalRevenue").desc()).show(10)

#Monthly sales trend
df = df.withColumn("InvoiceDate", to_date("InvoiceDate", "MM/dd/yyyy HH:mm"))
df = df.withColumn("YearMonth", date_format("InvoiceDate", "yyyy-MM"))
monthly_sales = df.groupBy("YearMonth").agg(spark_sum("Revenue").alias("MonthlyRevenue"))
monthly_sales.orderBy("YearMonth").show(12)

spark.stop()
