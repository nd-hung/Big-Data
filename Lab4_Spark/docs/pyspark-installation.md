# Cài đặt PySpark

- [Giới thiệu](#intro)
- [Cài đặt PySpark](#install_pyspark)
- [Chạy ứng dụng PySpark](#run_pyspark)
- [Tài liệu tham khảo](#references)

## Giới thiệu <a name="intro"/>

Python + Spark -> PySpark

PySpark là phiên bản Apache Spark dùng cho Python, là một nền tảng xử lý dữ liệu lớn ưu việt nhờ kết hợp sức mạnh của Python và Spark:
- Apache Spark là nền tảng xử lý dữ liệu lớn nguồn mở, tốc độ xử lý cao, dễ sử dụng, hỗ trợ nhiều ngôn ngữ lập trình, chạy được trên nhiều môi trường, khả năng phát triển ứng dụng đa dạng: SQL, machine learning, graph, streaming,...
- Python là ngôn ngữ được sử dụng chủ yếu hiện nay trong lĩnh vực machine learning và khoa học dữ liệu. Python có nhiều thư viện giúp nhanh chóng phát triển các ứng dụng phân tích dữ liệu: numpy, pandas, scikit-learn, matplotlib,... 

Có thể cài đặt PySpark theo các chế độ sau:
- Cài đặt trên máy đơn
- Cài đặt một cluster độc lập 
- Cài đặt PySpark trên một nền tảng quản lý dữ liệu lớn sẵn có (như Hadoop YARN, Apache Mesos, Kubernetes)


## Cài đặt PySpark trên máy đơn <a name="install_pyspark"/>

Có thể dùng một trong các cách sau để cài PySpark: Dùng PIP, dùng Conda, hoặc cài đặt từ nguồn.

### Cài đặt PySpark với PyPI PIP

#### Cài đặt PIP
PIP là trình quản lý cài đặt các thư viện Python.

Trước hết, cần kiểm tra PIP đã được cài đặt chưa (PIP cài sẵn trên Python >= 3.4). Với Python 3, dùng phiên bản PIP3:

```shell
pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```
 
Nếu PIP chưa cài đặt, thực hiện cài đặt PIP bằng lệnh sau trên Ubuntu Terminal:
```
sudo apt install python3-pip
```

#### Cài đặt PySpark với PIP
Mở Ubuntu Terminal và nhập lệnh sau:

```shell
pip3 install pyspark
```

Chạy Spark shells để kiểm tra cài đặt PySpark:

```shell
hung@hung-VirtualBox:~$ pyspark
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
...
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.1.1
      /_/
```

### Cài đặt PySpark với Conda
Conda - được kèm theo Anaconda - là trình quản lý môi trường và các thư viện nguồn mở thay thế PIP và virtualenv. Ưu điểm của cài đặt bằng Conda là cho phép tạo môi trường ảo (virtual environment). Điều này cho phép tạo nhiều môi trường làm việc độc lập với nhau, mỗi môi trường ảo chỉ cài đặt các công cụ cần thiết.

Để sử dụng Conda, cần [tải và cài đặt Anaconda](https://www.anaconda.com/products/individual). Sau đó, kiểm tra việc cài đặt Conda bằng lệnh sau:
```shell
conda --version
conda 4.10.0
```

#### Tạo môi trường ảo
Mở Ubuntu Terminal và nhập lệnh sau để tạo môi trường ảo, chẳng hạn môi trường cài đặt `PySpark` có tên là `pyspark_env`:

```shell 
conda create -n pyspark_env
```

Để xem danh sách các môi trường ảo, nhập lệnh sau:
```shell 
conda env list
```

Kích hoạt môi trường ảo:
```shell
conda activate pyspark_env
```

Ở trong môi trường ảo, thực hiện cài đặt PySpark bằng một trong hai lệnh sau:
```shell
pip3 install pyspark
```
hoặc
```shell
conda install pyspark
```

### Tải & cài đặt PySpark từ nguồn

[Tải về Spark ở đây](https://spark.apache.org/downloads.html), hoặc bằng lệnh sau:
```shell
wget https://downloads.apache.org/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz
```

Giải nén nguồn cài đặt:

```shell
tar xzvf spark-3.1.1-bin-hadoop3.2.tgz
```
Spark sẽ được giải nén thành một thư mục có tên `spark-3.1.1-bin-hadoop3.2`

Tạo các biến môi trường sau để thiết lập đường dẫn đến PySpark và Py4J:
```shell
cd spark-3.1.1-bin-hadoop3.2
export SPARK_HOME=`pwd`
export PYTHONPATH=$(ZIPS=("$SPARK_HOME"/python/lib/*.zip); IFS=:; echo "${ZIPS[*]}"):$PYTHONPATH
```

## Chạy ứng dụng PySpark <a name="run_pyspark"/>

Đoạn chương trình PySpark sau đây thực hiện đếm số lần xuất hiện của mỗi từ trong một tập dữ liệu văn bản. Chương trình thực hiện bằng hai cách: (1) Chạy trực tiếp trên môi trường tương tác Spark shell, và (2) Chạy ứng dụng trên cluster. 

### Chạy PySpark trên môi trường dòng lệnh Spark Shell

Trước hết cần khởi động Spark shell:
```shell
pyspark
```

Giả sử có tập dữ liệu văn bản ở thư mục `/home/hung/labs/data/gutenberg`. Nhập lệnh sau để nạp dữ liệu:
```shell
lines = sc.textFile("/home/hung/labs/data/gutenberg/")
```
Tập dữ liệu sẽ được nạp vào cấu trúc lưu trữ của Spark gọi là RDD (resilient distributed datasets). Thực hiện lệnh sau để tách các dòng văn bản thành các từ riêng biệt (các từ cách nhau bởi khoảng trắng):

```shell
words = lines.flatMap(lambda line: line.split(" "))
```
Thực hiện lệnh sau để đếm số lần xuất hiện của mỗi từ:
```shell
wordFrequencies = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
```
In ra 10 dòng kết quả:
```shell
someResults = wordFrequencies.take(10)
print(someResults)                                                    
```
Kết quả:
```shell
[('Project', 185), ('of', 23948), ('Science,', 5), ('Vol.', 65), ('(of', 7), ('4),', 3), ('', 34586), ('for', 3372), ('the', 42097), ('anywhere', 18)]
```

Lưu kết quả xử lý lên bộ nhớ ngoài:

```shell
wordFrequencies.saveAsTextFile("/home/hung/labs/data/output/gutenberg-result")
```

### [Chạy PySpark trên cluster](https://spark.apache.org/docs/latest/submitting-applications.html)
Để chạy ứng dụng PySpark trên cluster, cần tổ chức thành file mã nguồn độc lập, sau đó sử dụng lệnh `spark-submit` để nạp & thực thi ứng dụng.

Giả sử file `wordcount.py` chứa mã nguồn PySpark đếm số lần xuất hiện của mỗi từ trong một tập dữ liệu văn bản:

<script src="https://emgithub.com/embed-v2.js?target=https%3A%2F%2Fgithub.com%2Fnd-hung%2FBig-Data%2Fblob%2Fmain%2FLab4_Spark%2Fsrc%2Fwordcount.py&style=default&type=code&showBorder=on&showLineNumbers=on&showFileMeta=on&showCopy=on"></script>

Từ Terminal gọi lệnh sau để nạp & chạy chương trình:
```shell
spark-submit wordcount.py
```

##  Tham khảo <a name="references"/>
[PySpark Documentation](https://spark.apache.org/docs/3.1.1/api/python/)

Zaharia M., et al. Learning Spark (O'Reilly, 2015)
