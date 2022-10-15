from pyspark.sql import SparkSession
import dbldatagen as dg


spark = SparkSession.builder \
    .appName("Data-Generator") \
    .getOrCreate()

schema = dg.SchemaParser.parseCreateTable(spark, """
    create table Test1 (
    site_id int ,
    site_cd string ,
    c string ,
    c1 string ,
    sector_technology_desc string )
""")

# will have implied column `id` for ordinal of row
x3 = (dg.DataGenerator(sparkSession=spark, name="association_oss_cell_info", rows=1000000, partitions=20)
      .withSchema(schema)
      # withColumnSpec adds specification for existing column
      .withColumnSpec("site_id")
      # base column specifies dependent column
      .withIdOutput()
      .withColumnSpec("site_cd", prefix='site', baseColumn='site_id')
      .withColumn("sector_status_desc", "string", prefix='status', random=True)
      # withColumn adds specification for new column
      .withColumn("rand", "float", expr="floor(rand() * 350) * (86400 + 3600)")
      .withColumn("last_sync_dt", "timestamp", random=True)
      .withColumnSpec("sector_technology_desc", values=["GSM", "UMTS", "LTE", "UNKNOWN"], random=True)
      .withColumn("test_cell_flg", "int", values=[0, 1], random=True)
      )

result = x3.build(withTempView=True)

result.write.format("bigquery") \
    .option("credentialsFile", "/credentialsFile.json") \
    .option("writeMethod", "direct") \
    .save("data-generator-363818.test.test_table")