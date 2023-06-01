
# 建立3master、3从节点的redis-cluster集群


## 1、在linux服务器中生成redis配置文件模板redis.conf
```
#port（端口号）
port ${PORT}
#masterauth（设置集群节点间访问密码，跟下面一致）
masterauth 123456
#requirepass（设置redis访问密码）
requirepass 123456
#cluster-enabled yes（启动集群模式）
cluster-enabled yes
#cluster-config-file nodes.conf（集群节点信息文件）
cluster-config-file nodes.conf
#cluster-node-timeout 5000（redis节点宕机被发现的时间）
cluster-node-timeout 5000
#cluster-announce-ip（集群节点的汇报ip，防止nat，预先填写为网关ip后续需要手动修改配置文件）
cluster-announce-ip 172.19.0.1
#cluster-announce-port（集群节点的汇报port，防止nat）
cluster-announce-port ${PORT}
#cluster-announce-bus-port（集群节点的汇报bus-port，防止nat）
cluster-announce-bus-port 1${PORT}
#appendonly yes（开启aof）	
appendonly yes
```

也可以批量在一台服务器上生成，创建shell脚本，输入下面内容，该脚本将批量生成6个redis配置文件对应端口6500-6505，redis-cluster.tmpl是上面的配置内容
```
for port in $(seq 6500 6505);
 do
    mkdir -p ./${port}/conf && PORT=${port} envsubst < ./redis-cluster.tmpl > ./${port}/conf/redis.conf && mkdir -p ./${port}/data;
done
```
## 2、创建容器，根据需要执行
```
docker run -d --net=host -v /root/6500/conf/redis.conf:/etc/redis/redis.conf -v /root/6500/data:/data --restart always  --privileged=true --name=redis-6500  redis redis-server /etc/redis/redis.conf

docker run -d --net=host -v /root/6501/conf/redis.conf:/etc/redis/redis.conf -v /root/6501/data:/data --restart always  --privileged=true --name=redis-6501  redis redis-server /etc/redis/redis.conf

docker run -d --net=host -v /root/6502/conf/redis.conf:/etc/redis/redis.conf -v /root/6502/data:/data --restart always  --privileged=true --name=redis-6502  redis redis-server /etc/redis/redis.conf

docker run -d --net=host -v /root/6503/conf/redis.conf:/etc/redis/redis.conf -v /root/6503/data:/data --restart always  --privileged=true --name=redis-6503  redis redis-server /etc/redis/redis.conf

docker run -d --net=host -v /root/6504/conf/redis.conf:/etc/redis/redis.conf -v /root/6504/data:/data --restart always  --privileged=true --name=redis-6504  redis redis-server /etc/redis/redis.conf

docker run -d --net=host -v /root/6505/conf/redis.conf:/etc/redis/redis.conf -v /root/6505/data:/data --restart always  --privileged=true --name=redis-6505  redis redis-server /etc/redis/redis.conf
该命令中我批量生成的配置文件在/usr/local/redis-cluster-d/目录下，根据不同端口分为不同目录
```


## 3、查看创建好的容器 

docker ps -a | grep redis



## 4、进入其中一台要设定master的节点docker容器中

2cd952c5a343为该容器ID

``` language
  docker exec -it 2cd952c5a343 bash
```

## 5、执行集群初始化命令

``` language
  redis-cli -a 123456 --cluster create 127.0.0.1:6500 127.0.0.1:6501 127.0.0.1:6502 127.0.0.1:6503 127.0.0.1:6504 127.0.0.1:6505 --cluster-replicas 1
```
初始化过程中会将各节点分配至不同的容器中，然后输入yes



## 6、完成后使用redis-cli 进行测试

执行命令，重点参数为-c 以集群的方式连接，不然将连接该单机节点，无法进行集群

``` language
  redis-cli -c -a 123456  -h 127.0.0.1 -p 6500
```

RDM连接
![image.png](http://快乐星球.site:8211/e03acdf1-8989-4a74-94b0-ae2f69db7bc9.png)
![image.png](http://快乐星球.site:8211/327a90bf-f638-4b63-8a78-4c4941e3514c.png)