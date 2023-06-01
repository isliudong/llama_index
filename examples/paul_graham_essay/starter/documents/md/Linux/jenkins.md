[查看Docker启动jenkins的管理员密码](https://www.cnblogs.com/Uni-Hoang/p/12878634.html)

Docker启动docker后，第一次方法jenkins，需要输入管理员密码。

其实查看启动时候的日志可以看到密码，也可以按照以下方法找到密码。

![img](C:\Users\liudong\Documents\mdDocument\Linux\jenkins.assets\1725305-20200512210240564-1750526940.png)

 

 

1.查看docker容器ID：docker ps -a

 

2.登陆到容器：docker exec -u 0 -it 6b71192760e2 /bin/bash

 -u 0 是使用root权限，如果不需要修改文件可以不使用此参数。

 

docker attach 容器ID

docker exec -it 容器ID /bin/bash

 

3.查看密码文件：cat /var/jenkins_home/secrets/initialAdminPassword

 

![img](C:\Users\liudong\Documents\mdDocument\Linux\jenkins.assets\1725305-20200512210821785-669830890.png)

 

 

 ![img](C:\Users\liudong\Documents\mdDocument\Linux\jenkins.assets\1725305-20200512211326005-2146570202.png)

 









centos安装通过yum安装jenkins

unhejing 2020-05-21 18:21:52  3055  收藏 9
分类专栏： centos7最厉害的服务器
版权

centos7最厉害的服务器
专栏收录该内容
19 篇文章0 订阅
订阅专栏
前言：之前安装jenkins是通过tomcat直接部署jenkins的war包，该文是通过yum安装jenkins。方便管理，随启随停。
1.前提安装了java

（1）输入java -version



（2）获取java路径，后面启动jenkins需要

输入 echo $JAVA_HOME，如图：将下面路径记录下来后面追加/bin/java   如： /usr/local/java/jdk1.8.0_141/bin/java



 

2.获取jenkins源文件

wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo
3.导入jenkins公钥

rpm --import https://jenkins-ci.org/redhat/jenkins-ci.org.key
4.yum安装jenkins

yum install -y jenkins
（1）备注：2，3，4步骤不行的话就去官网下载rpm包。

wget http://pkg.jenkins-ci.org/redhat-stable/jenkins-2.7.3-1.1.noarch.rpm
rpm -ivh jenkins-2.7.3-1.1.noarch.rpm
（2）配置文件

/usr/lib/jenkins/ #jenkins安装目录，WAR包会放在这里。

/etc/sysconfig/jenkins #jenkins配置文件
/var/lib/jenkins/ #默认的JENKINS_HOME。 
/var/log/jenkins/jenkins.log #日志文件


5.启动jenkins

service jenkins start
service jenkins stop
service jenkins restart
启动会报错：



查看错误信息是因为找不到java，所以需要配置java路径。将第一步的路径复制一下

编辑配置：

vim  /etc/init.d/jenkins


将路径输入在如图位置，保存退出即可

6.访问

http://{IP地址}:8080

7.卸载

 卸载jenkins：rpm -e jenkins

 删除缓存文件: find / -iname jenkins | xargs -n 1000 rm -rf