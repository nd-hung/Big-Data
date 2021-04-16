#!/usr/bin/python3
"""mapper.py"""

import sys

# Chương trình Python chạy trên Hadoop MapReduce qua tính năng Streaming.
# Dữ liệu vào từ thiết bị nhập chuẩn (STDIN)
# Kết quả xử lý gửi ra thiết bị xuất chuẩn (STDOUT)

for line in sys.stdin.buffer.raw:
    # loại bỏ ký tự trắng ở đầu và cuối chuỗi
    line = line.strip()
    # tách ra thành các từ
    words = line.split()
    # đưa ra thiết bị xuất chuẩn các cặp <word, 1>, cách nhau bằng ký tự tab
    for word in words:
        print('%s\t%s' % (word, 1))