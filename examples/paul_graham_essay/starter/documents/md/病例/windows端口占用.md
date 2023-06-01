### cmd 端口占用

`netstat -ano|findstr 1080`

`taskkill /pid 3188 /f`

### 重启网卡

网上大多数教程表示需要关闭被占用的端口，但实际上并没有任何端口被占用。
实际上这个问题只需要重启一下网卡就可以了，具体步骤如下：

以管理员身份打开PowerShell。
用下面的命令停止winnat。
 net stop winnat
用下面的命令再次启动winnat。
net start winnat

