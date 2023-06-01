# 基于es的搜索补全、热词统计



## 一、产品搜索

### 1、原理

​        基于es的全文检索技术的多条件聚合搜索功能，在项目启动时检查es索引是否初始化，若未初化则创建索引，注意并未初始化产品相关的数据，需要在项目启动后手动调用es数据初始化接口

![image-20210818141359729](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20210818141359729.png)



## 二、热门词汇

### 1、原理

通过在用户搜索时进行数据埋点，埋点位置如图所示![image-20210818142047707](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20210818142047707.png)将搜索词汇记录到es（通过日志数据分发)，并在es存储前通过管道进行数据预处理，最终得到想要的记录，然后通过es的聚合分析功能，分析出topN词汇，并将其存入redis缓存（24h过期)

### 2、流程概览

![image-20210818144850266](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20210818144850266.png)

## 三、词汇补全

### 1、原理

​       基于es的Completion Suggester前缀补全功能，基本流程类似于搜索。在项目启动时检查es索引是否初始化，若未初化则创建索引，注意并未初始化产品相关的数据，需要在项目启动后手动调用es数据初始化接口（同产品搜索数据初始化，两者只需调用一次即可）

### 2、实现

①、实体

![image-20210818151932307](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20210818151932307.png)

②、设计思路

+ input：推荐词，产品的相关信息通过es的分词器提取产品相关词汇，放入该字段。

+ weight：优先级，将产品不同的部分的信息分配不同的权重，如产品名具有较高权重，再搜索是会优先推荐补全相关词汇。
