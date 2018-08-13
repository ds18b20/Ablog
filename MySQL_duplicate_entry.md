# MySQL error code 1062
使用Python管理MySQL时出现了`pymysql.err.IntegrityError: (1062, "Duplicate entry...`的错误。
说明规定不能重复的字段内出现了重复值。
比如`unique key `idx_email` (`email`)`就规定email不可重复，当此处值发生重复时就会报错。
## 参考
https://www.rathishkumar.in/2016/01/how-to-solve-mysql-error-code-1062.html
