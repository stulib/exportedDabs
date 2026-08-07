# Databricks notebook source
import dlt


@dlt.table(comment="Seed bronze table for the dabs-migrator test pipeline")
def dm_bronze():
    return spark.range(10).withColumnRenamed("id", "row_id")

