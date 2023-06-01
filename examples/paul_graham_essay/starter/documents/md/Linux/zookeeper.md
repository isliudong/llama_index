### docker安装zookeeper后进入查看镜像内部文件的命令

`docker ps`

### 进入容器

`docker exec -it f76b7e25baa9 /bin/bash`

### 进入bin目录
`cd bin`

### 登录server
`zkCli.sh -server 127.0.0.1:2181`

### 查看目录
`ls /`

#### 查看服务

`ls /services`