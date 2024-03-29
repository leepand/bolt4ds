# bolt4ds

Accelerate data science - Python Libraries

对于数据科学家和数据工程师来说，bolt4ds是一个基于Python的产品集合，可以减少您的数据准备分析所需的时间。

![bolt4ds Workflow](pipelines.jpg "bolt4ds Workflow")

数据科学中的大部分时间都花在与数据分析无关的繁琐任务上。
bolt4ds简化了这些任务，使您可以体验到高达10倍的生产力提升。

* **管理数据流程**: 快速构建高效的数据科学工作流程
* **稀疏数据处理工具箱**: 建立在pandas和scipy之上，提供类似DataFrame的API来处理稀疏数据。
* **数据提取与存储**: 快速摄取杂乱的原始CSV和XLS文件到pandas、SQL等。
* **连接数据**: 使用模糊连接快速组合多个数据集
* **推荐引擎**: 封装特征处理和推荐预测
* **机器学习模型监控** 按sklearn接口标准实施模型特征的监控
* **项目模板**: 为数据科学提供标准模板

这些库是模块化的，所以你可以单独使用它们，但它们可以很好地协同工作，改善你的整个数据工作流程。 

## 管理数据流程

轻松管理数据工作流，包括复杂的依赖关系和参数。使用bolt4ds.flow，您可以轻松地将复杂的数据流串联起来，并智能地执行。您可以为每个任务快速加载输入和输出数据。它使您的工作流非常清晰直观。

### 它能做什么?

* 构建一个由任务组成的数据工作流程，其中包含依赖关系和参数的任务
* 在改变参数、代码或数据后，智能地重新运行工作流程
* 快速加载任务输入和输出数据，无需人工操作，快速加载任务输入和输出数据

Learn more at [https://github.com/leepand/bolt4ds](https://github.com/leepand/bolt4ds)

## 稀疏数据处理工具箱

许多任务，特别是在数据分析和机器学习领域，常用稀疏的数据结构来支持高维数据的输入。Pandas有自己的稀疏数据结构的实现。不幸的是，这种结构在我们经常使用的分组比和聚合中表现相当糟糕。此外，在Pandas SparseDataFrame上进行groupby操作会返回一个稠密结构的DataFrame。这使得在多个文件上进行groupby操作的链式操作非常繁琐，而且效率较低、占用大量内存。在对scipy.sparse csrr matrr上的许多函数调用进行了链式化后，我们决定启动这个项目，这些函数涉及到指数和列名的处理，以产生一个稀疏数据管道。

如果你有大量的稀疏数据，如点击流数据、分类时间序列、日志数据或类似的稀疏数据，这个包可能对你特别有用。

## 数据提取与存储

### 功能包括

* 用于postgres和mysql的快速pd.to_sql()
* 快速检查跨文件的列是否一致
* 修复新增/缺失的列
* 修复重命名的列
* 检查Excel选项卡在不同文件中的一致性
* Excel到CSV转换器(包括多表支持)
* 超出了处理大文件的核心功能
* 导出为CSV、parquet、SQL、pandas数据框架

## 连接数据

合并数据集是一种常见的数据工程操作。然而，由于标识符不匹配、日期约定等原因，经常会出现合并不同来源的数据集的问题。

bolt4ds.utils模块允许你测试连接精度，并快速识别和分析连接问题。

### 功能包括：

* 在尝试数据连接之前进行加入质量分析。
* 检测和分析基于字符串的标识符不匹配问题
* 查验分析日期不匹配

## 推荐引擎

数据侧封装交互、特征标准化处理流程和ID mapping，模型侧封装基于lightfm的训练、基础预测和基于最近邻的快速预测类


## 机器学习模型监控

每个生产机器学习系统都容易出现协变量偏移，当运行时预测的生产数据的分布与你训练过的分布 "漂移 "时，就会出现协变量偏移。这种现象会严重降低模型的性能，而且可能会因为各种原因而导致模型的性能下降--例如，你的公司现在销售新产品或不再提供旧产品，库存价格上涨，或者向你的模型发送数据的软件中存在错误。协变量漂移的影响可能很微妙，很难被发现，但尽管如此，抓住它还是很重要。在谷歌的机器学习指南中，他们报告说，刷新一个陈旧的表，导致Google Play的安装率增加了2%。重新训练和重新部署你的模型是一个明显的修复方法，但对于你应该多久做一次这样的事情，可能是模糊不清的，一旦有新的数据到来，每天、每周、每个星期、每个月都要做一次？更重要的是，这只适用于上面提到的前两个例子，不能用来修复集成BUG。

### 示例

```commandline

import logging
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
from bolt4ds.monitor import DataMonitorTransformer

SIZE = 100
df1 = pd.DataFrame({
    # categorical
    'feature1': np.random.randint(0, 5, size=SIZE),
    'feature2': np.random.randint(0, 5, size=SIZE),
    'feature3': np.random.randint(0, 5, size=SIZE),
    # numeric
    'feature4': np.random.uniform(0, 100, size=SIZE),
    'feature5': np.random.uniform(50, 100, size=SIZE),
    'response': np.random.randint(1, size=SIZE)
})
df2 = pd.DataFrame({
    # categorical
    'feature1': np.random.randint(0, 7, size=SIZE),  # extra values
    'feature2': np.random.randint(0, 5, size=SIZE),
    'feature3': np.random.randint(-1, 5, size=SIZE), # extra values
    # numeric
    'feature4': np.random.uniform(-10, 120, size=SIZE), # violate max/min
    'feature5': np.random.uniform(50, 110, size=SIZE),  # violate max
})
df1['feature1'] = df1.feature1.astype(str)
df2['feature1'] = df2.feature1.astype(str)
df1['feature2'] = df1.feature2.astype(str)
df2['feature2'] = df2.feature2.astype(str)
df1['feature3'] = df1.feature3.astype(str)
df2['feature3'] = df2.feature3.astype(str)

logging.basicConfig()
features = [c for c in df1.columns if c.startswith('feature')]
response = 'response'
feijiandu = DataMonitorTransformer()
feijiandu.fit(df1[features])

feijiandu.transform(df2[features])

feijiandu.data_monitor.schema

```


## 安装

Install with pip:


```commandline
pip install .
```