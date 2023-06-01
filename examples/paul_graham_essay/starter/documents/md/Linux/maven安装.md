# [centos7 maven3.6.3安装]

环境：

操作系统：centos 7.6
maven版本:apache-maven-3.6.3-bin.tar.gz

1、下载maven
cd /backup/soft
wget https://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz

2、解压maven
tar -xvf apache-maven-3.6.3.tar.gz

mv apache-maven-3.6.3 /usr/local/maven3

3、添加环境变量
vi /etc/profile
export MVN_HOME=/usr/local/maven3
export PATH=${JAVA_HOME}/bin:${MVN_HOME}/bin:$PATH

source /etc/profile

4、添加软连接
ln -s /usr/local/maven3/bin/mvn /usr/bin/mvn

5、配制repo存放路径
cd conf
vi setttings.xml
<localRepository>/usr/local/repo</localRepository>