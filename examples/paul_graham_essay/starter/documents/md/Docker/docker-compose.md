#### docker-compose的作用

docker-comopse可以帮助我们快速搭建起开发环境，比如你可以去把redis,mongodb,rabbitmq,mysql,eureka,configserver等一次部署在本机，然后让它们做为其它项目的基础，这是可以实现的。

#### 容器之间的通讯-links

由于每个docker实例都是一个封闭的环境，所以默认情况下它们是不能共享的，即你的rabbit容器不能连接你的redis容器，你的configserver不能连接你的eureka容器，如果希望让它们之间进行数据通讯，需要设置`links`属性来实现，而在本机（宿主机）上进行连接时，使用localhost和端口是可以访问这些容器的，这个我们要清楚。

#### 启动顺序-depends_on

而对于启动顺序来说，比如你的configserver依赖于eureka，希望先启动被依赖的容器，再运行自己，这时我们可以使用depends_on属性来实现，当然它也只是启动顺序，不能保证服务真的越来后再去启动另一个，解决的方法是使用`失败重试`机制`restart: on-failure`，当configserver失败后，你可以重启，直到成功为止（主是直到eureka启动越来为止）。

#### 容器与容器之间要用服务名通讯

如果我们的具体项目也希望部署到docker-compose里，希望去访问其它的服务，这时，需要使用docker-compose里定义的服务名称，而不是localhost，因为当你的容器起来之后，它的localhost是自己的容器，而不是宿主机，反之在宿主机上，如果希望访问容器，可以使用`localhost`，这一点在前文中已经提到。

#### 下面是我写的一个部署开发环境的例子

```bash
version: "3.3"



services:



 



  # 公用组件相关配置



  mongodb:



    image: mongo:3.4.10



    ports:



      - "27017:27017"



    networks:



      - dev



    volumes:



      - mongo_data:/data/db



 



  redis:



    image: redis:3.2-alpine



    networks:



      - dev



    ports:



      - "6379:6379"



    volumes:



      - redis_data:/data



 



  rabbit:



    image: rabbitmq:3.6.10-management-alpine



    hostname: rabbit



    ports:



      - "5672:5672"



      - "15672:15672"



      - "61613:61613"



    networks:



      - dev



    environment:



      RABBITMQ_DEFAULT_VHOST: pilipa



    volumes:



      - rabbitmq_data:/var/lib/rabbitmq



  



  eurekaserver:



    build: ./springcloud/eureka-server



    restart: on-failure



    ports:



      - "8761:8761"



      - "8762:8762"



    networks:



      - dev



 



  configserver:



      build: ./springcloud/config-server



      restart: on-failure



      ports:



        - "8888:8888"



        - "8889:8889"



      networks:



        - dev



      depends_on:



        - eurekaserver #依赖服务



      links:



        - eurekaserver



      environment:



        SPRING_PROFILES_ACTIVE: devops



      volumes:



        - /Users/lind.zhang/project/config-repo:/config_repo #前面是本地路径，后而是容器里的路径，在configserver里配置的是后面的容器路径
```

#### 启动与更新

1. 先打镜像

```undefined
docker-compose build
```

1. 再启动服务

```r
docker-compose up -d #-d是后台运行
```

1. 停止服务

```undefined
docker-compose down
```

1. 查看容器的日志

```undefined
docker logs -f 容器ID
```