# MySQL优化入门


> ## 优化思维
> 1、索引优、sql优化
2、存储引擎 参数配置 优化
索引缓冲区、查询缓冲区、数据缓冲区、读写缓冲区、日志缓冲区的一些大小配置
3、操作系统关于链接参数配置，比如timewait时长、socket链接的快速回收、socket链接reuse、backlog的队列大小等等
4、数据库瓶颈主要在磁盘io，mysql的redo log，undo log用来保持事务的持久性、原子性；binlog 用来做读写分离、主从、数据库集群等；可以关掉binlog减少刷磁盘，用redo log做主从因为它是物理日志，性能比较好，光关掉binlog是不够的，优化redo log，减少redo log 刷盘的性能抖动，包括去掉reuse 让redo log 日志去文件增长
5、spdk高性能磁盘io框架，主要技术是uio然后是polling，还能减少中断；这个技术也可以永在消息队列的持久化上。像rocks db存储引擎也用了spdk框架优化 



## 一、SQL优化

### 1、发现慢查询

```
//查看慢查询日志是否开启
show variables like 'slow_query_log';

//查看慢查询日志存储位置
show variables like 'slow_query_log_file';

//开启慢查询日志
set global slow_query_log=on;

//指定慢查询日志存储位置
set global show_query_log_file='/var/lib/mysql/homestead-slow.log';

//记录没有使用索引的sql
set global log_queries_not_using_indexes=on;

//记录查询超过1s的sql，注意下次会话才生效
set global long_query_time=1;
```



## 2、数据库优化方向

| 活动/峰值连接数  | 1/2    | 若值过大,增加max_connections         |
| :--------------- | ------ | ------------------------------------ |
| 线程缓存命中率   | 50.00% | 若过低,增加thread_cache_size         |
| 索引命中率       | 0%     | 若过低,增加key_buffer_size           |
| Innodb索引命中率 | 73.19% | 若过低,增加innodb_buffer_pool_size   |
| 查询缓存命中率   | OFF    | 若过低,增加query_cache_size          |
| 创建临时表到磁盘 | 0.00%  | 若过大,尝试增加tmp_table_size        |
| 已打开的表       | 0      | table_open_cache配置值应大于等于此值 |
| 没有使用索引的量 | 0      | 若不为0,请检查数据表的索引是否合理   |
| 没有索引的JOIN量 | 0      | 若不为0,请检查数据表的索引是否合理   |
| 排序后的合并次数 | 0      | 若值过大,增加sort_buffer_size        |
| 锁表次数         | 0      | 若值过大,请考虑增加您的数据库性能    |
