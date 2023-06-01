###  kibana安装

+ 拉取镜像

```
docker pull kibana:7.6.1
```

+ 创建kibana容器，连接es

```bash
docker run --name kibana -e ELASTICSEARCH_HOSTS=http://172.18.0.4:9200 -p 5601:5601 -d f9ca33465ce3
```

#### elasticsearch 插件ik分词器

+ 进入容器

```bash
docker exec -it elasticsearch /bin/bash
```

+ 在线下载并安装（注意保持与elasticsearch 版本一致）

```bash
./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.8.0/elasticsearch-analysis-ik-7.8.0.zip
```

![image-20200826135044497](C:\Users\liudong\Documents\mdDocument\docker\Untitled.assets\image-20200826135044497.png)

+ 进入plugins可以看到IK分词器已经安装成功

![image-20200826135201413](C:\Users\liudong\Documents\mdDocument\docker\Untitled.assets\image-20200826135201413.png)