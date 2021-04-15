# Cài đặt thuật toán K-means phân tán với PySpark

- [Spark Machine Learning Libarary](#mllib)
- [Thuật toán K-means với PySpark](#spark_kmeans)
- [So sánh kết quả với thư viện Scikit-learn](#comparison)

## Spark Machine Learning Library <a name="mllib"/>

Spark cung cấp [thư viện MLLib (Machine Learning Library)](https://spark.apache.org/docs/3.1.1/ml-guide.html) cho phép triển khai các dự án machine learning phân tán. Các tính năng của MLLib bao gồm:
- Một số thuật toán ML tiêu biểu: phân lớp (classification), hồi qui (regression), phân cụm (clustering), collaborative filtering.
- Xử lý đặc trưng (featurization): trích xuất (feature extraction), biến đối (transformation), giảm chiều (dimensionality reduction), chọn lọc (feature selection).

- Pipelines: các công cụ xây dựng, tinh chỉnh và đánh giá mô hình ML.
- Các tiện ích: xử lý dữ liệu, lưu/nạp mô hình, v.v.

Bên cạnh thư viện MLLib (RDD-based API), hiện nay Spark cung cấp thư viện ML mới (DataFrame-based API) với nhiều tính năng dễ sử dụng hơn MLLib. 

## Thuật toán K-means với PySpark <a name="spark_kmeans"/>
### Khai báo các thư viện 


```python
import pandas as pd
import numpy as np
from pyspark.ml.clustering import KMeans
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
```

### Khởi tạo Spark Session

Spark phiên bản 2.0 trở đi cung cấp lớp SparkSession để khởi tạo các chức năng của Spark. Sau khi tạo Spark Session, người dùng có thể lập trình với RDD, DataFrame và Dataset. 


```python
# Create new Spark session
spark = SparkSession.builder.appName("Distributed KMeans Example").getOrCreate()
```

### Tạo dữ liệu dạng DataFrame

Với Spark Context, người dùng phải tạo mới RDD sau đó lập trình xử lý trên RDD. Spark Session cung cấp các API xử lý với các loại dữ liệu khác, gồm cả DataFrame.

Để nạp dữ liệu iris vào Spark cluster, có thể thực hiện như sau: trước hết đọc dữ liệu đưa vào DataFrame dùng thư viện pandas, sau sử dụng phương thức spark.createDataFrame() để nạp dữ liệu vào Spark DataFrame.


```python
iris_data = spark.createDataFrame(pd.read_csv('/home/hung/Downloads/iris.data', 
                                                header=None, names=['sepal-length',
                                                                    'sepal-width', 'petal-length', 
                                                                    'petal-width','label']))
print("First 10 rows:")
iris_data.show(10)
```

    First 10 rows:
    +------------+-----------+------------+-----------+-----------+
    |sepal-length|sepal-width|petal-length|petal-width|      label|
    +------------+-----------+------------+-----------+-----------+
    |         5.1|        3.5|         1.4|        0.2|Iris-setosa|
    |         4.9|        3.0|         1.4|        0.2|Iris-setosa|
    |         4.7|        3.2|         1.3|        0.2|Iris-setosa|
    |         4.6|        3.1|         1.5|        0.2|Iris-setosa|
    |         5.0|        3.6|         1.4|        0.2|Iris-setosa|
    |         5.4|        3.9|         1.7|        0.4|Iris-setosa|
    |         4.6|        3.4|         1.4|        0.3|Iris-setosa|
    |         5.0|        3.4|         1.5|        0.2|Iris-setosa|
    |         4.4|        2.9|         1.4|        0.2|Iris-setosa|
    |         4.9|        3.1|         1.5|        0.1|Iris-setosa|
    +------------+-----------+------------+-----------+-----------+
    only showing top 10 rows
    


### Tạo vector đặc trưng từ DataFrame

Để tạo vector đặc trưng (feature vector) cho từng dòng dữ liệu, dùng lớp VectorAssembler để ghép giá trị ở các cột trong DataFrame thành một cột mới chứa vector đặc trưng:


```python
assembler = VectorAssembler(inputCols = ["sepal-length", "sepal-width", "petal-length", "petal-width"], 
                            outputCol="features") 
irisFeatures = assembler.transform(iris_data) 
irisFeatures.show(5)
```

    +------------+-----------+------------+-----------+-----------+-----------------+
    |sepal-length|sepal-width|petal-length|petal-width|      label|         features|
    +------------+-----------+------------+-----------+-----------+-----------------+
    |         5.1|        3.5|         1.4|        0.2|Iris-setosa|[5.1,3.5,1.4,0.2]|
    |         4.9|        3.0|         1.4|        0.2|Iris-setosa|[4.9,3.0,1.4,0.2]|
    |         4.7|        3.2|         1.3|        0.2|Iris-setosa|[4.7,3.2,1.3,0.2]|
    |         4.6|        3.1|         1.5|        0.2|Iris-setosa|[4.6,3.1,1.5,0.2]|
    |         5.0|        3.6|         1.4|        0.2|Iris-setosa|[5.0,3.6,1.4,0.2]|
    +------------+-----------+------------+-----------+-----------+-----------------+
    only showing top 5 rows
    


Lúc này dữ liệu đã sẵn sàng để đưa vào huấn luyện mô hình ML (ở đây là K-means).
Gỉa sử chọn số cụm là 3, tiến hành huấn luyện mô hình K-means với PySpark bằng các lệnh sau:

### Huấn luyện mô hình


```python
# Huấn luyện mô hình K-means với K=3 trên toàn bộ tập dữ liệu.
# Trong thực tế, để huấn luyện một mô hình ML, tập dữ liệu thường được chia làm 3 phần:
# - train set dùng để huấn luyện,
# - validation set dùng để đánh giá, tinh chỉnh mô hình trong quá trình huấn luyện,
# - test set để kiểm tra hiệu năng của mô hình trên dữ liệu hoàn toàn mới.
kmeans = KMeans().setK(3).setSeed(0)
model = kmeans.fit(irisFeatures)
```

### In kết quả


```python
# In ra tâm điểm của các cụm

centers = model.clusterCenters()
np.set_printoptions(precision=2)

print("Centers learned by Spark ML: ")
for center in centers:
    print(center)

spark.stop()
```

    Centers learned by Spark ML: 
    [5.9  2.75 4.39 1.43]
    [5.01 3.42 1.46 0.24]
    [6.85 3.07 5.74 2.07]


### So sánh với kết quả chạy K-means bằng thư viện Scikit-learn <a name="comparison"/>


```python
from sklearn import datasets
from sklearn.cluster import KMeans

np.random.seed(0)
```


```python
# Nạp dữ liệu

iris = datasets.load_iris()
X = iris.data

kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

print('Centers learned by scikit-learn:')
print(kmeans.cluster_centers_)
```

    Centers learned by scikit-learn:
    [[5.9  2.75 4.39 1.43]
     [5.01 3.43 1.46 0.25]
     [6.85 3.07 5.74 2.07]]

