# Xử lý dữ liệu văn bản với PySpark


- [Nạp dữ liệu](#load_data)
- [Chương trình word count](#wordcount)
- [Trích lọc văn bản](#text_filter)
- [Lưu kết quả lên bộ nhớ ngoài](#save_results)

- [Bài tập](#excercises)

- [Tham khảo](#references)




```python
import os, shutil

from pyspark import SparkContext


# create Spark context with necessary configuration
sc = SparkContext("local", "Text processing with PySpark Example")

# read data from text file into lines  
lines = sc.textFile("/home/hung/labs/data/gutenberg/")

# split the lines into words
words = lines.flatMap(lambda line: line.split(" "))

# count the occurrence of each word
wordFrequencies = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# count total number of words in the dataset
totalWordNumber = words.map(lambda word: 1).reduce(lambda a,b: a + b)

# display results
# print the number of lines
print('\nTotal number of lines:', lines.count())

# print total number of words in the dataset
print('\nTotal number of words:', totalWordNumber)

# show 10 rows 
someResults = wordFrequencies.take(10)
print("\nSome results:")
print(someResults)

# show top 10 most frequent words
topFrequentWords = wordFrequencies.takeOrdered(10, key = lambda x: -x[1])
print("\nTop frequent words:")
print(topFrequentWords)
```

    
    Total number of lines: 78753
    
    Total number of words: 664661
    
    Some results:
    [('Project', 185), ('of', 23948), ('Science,', 5), ('Vol.', 65), ('(of', 7), ('4),', 3), ('', 34586), ('for', 3372), ('the', 42097), ('anywhere', 18)]
    
    Top frequent words:
    [('the', 42097), ('', 34586), ('of', 23948), ('and', 16916), ('a', 12058), ('to', 12034), ('in', 11885), ('is', 7408), ('that', 6109), ('it', 4979)]



```python
# save the set of <word, frequency> to disk
savingPath = "/home/hung/labs/data/output/gutenberg-result"

if os.path.isdir(savingPath):
    shutil.rmtree(savingPath, ignore_errors=True)

wordFrequencies.saveAsTextFile(savingPath)
```

## Bài tập<a name="excercises"/>

1. Từ file `apache_logs` hãy lọc ra các dòng thông báo lỗi (chứa từ "error") với PySpark.
2. Xử lý dữ liệu Twitter
Cho file văn bản `elonmusk_tweets.csv` chứa các dòng tweets của Elon Musk từ 2011-2017. Dữ liệu được chia sẻ bởi [Adam Helsinger](https://data.world/adamhelsinger/elon-musk-tweets-until-4-6-17). Từ file dữ liệu trên, hãy thực hiện các xử lý sau với PySpark:
- Liệt kê top 20 từ được nhắc đến nhiều nhất.
- Liệt kê top 10 tài khoản được nhắc đến nhiều nhất.

## Tham khảo <a name="references"/>
[PySpark Documentation
](https://spark.apache.org/docs/3.1.1/api/python/)


Zaharia M., et al. Learning Spark (O'Reilly, 2015)


```python

```
