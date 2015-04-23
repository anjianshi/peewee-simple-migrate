peewee-simple-migrate
=====================

其一
----

每当数据结构进行一次更新，就由用户为新版本生成一个由数字组成的版本号（不能为 0，且新的版本的版本号应大于老版本的版本号），
并创建一个名为 "ver_{版本号}.py" 的文件，文件中包含了从上一版本转换到这一版本需要执行的代码

此外，还有一个特殊的文件："initialize.py"，它包含了在数据库为空的情况下创建整个数据结构（包括填充默认数据）所用的代码

ver_xxx.py 和 initialize.py 中的代码应包裹在一个名为 `run()` 的函数中，并接收一个参数 `db`。
下面是一个例子：
.. code-block:: python

# ver_123.py
from playhouse.migrate import *


def run(db):
    migrator = PostgresqlMigrator(db)
    migrate(
        migrator.rename_column("my_table", "col", "new_name")
    )
```


其二
----

peewee-simple-migrate 会在数据库中创建一个名为 `migration` 的表，在里面记录当前数据结构的版本号
（如果当前还一个版本也没有，也就是整个应用的数据结构还没发生过变更，那么版本号为 0）


其三
-----

执行迁移时，Migration 会检查 migration 表中的数据：
1. 如果 migration 表不存在，说明数据库为空。执行 initialize.py 进行初始化。
   并创建 migration 表，把当前最新的版本号写进表中
2. 如果成功从 migration 表中读出了数据库中数据结构的版本号，则把本地中所有版本号高于它的代码依次执行一遍，将它的结构转换到最新的状态。
   并更新 migration 表中记录的版本号


其四
----
All you need is:
1. Define your models, initialize file, and migrate files properly.
2. Call the `run()` function whenever your app start.


支持 Python 2.7+, 3.2+
