import sys

from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    # create Spark context with necessary configuration
    sc = SparkContext("local", "PySpark Word Count Exmaple")

    # read data from text file and split each line into words
    words = sc.textFile("/home/hung/labs/pyspark/data/gutenberg/").flatMap(lambda line: line.split(" "))

    # count the occurrence of each word
    wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

    # save the counts to output
    wordCounts.saveAsTextFile("/home/hung/labs/pyspark/data/gutenberg-output/")
