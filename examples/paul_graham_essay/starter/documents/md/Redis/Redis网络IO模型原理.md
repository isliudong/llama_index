# Redis IO 模型及原理

## 一、常用的五种IO模型

### socket通信

Socket 中文翻译为套接字，是计算机网络中进程间进行双向通信的端点的抽象。一个 Socket 代表了网络通信的一端，是由操作系统提供的进程间通信机制。在操作系统中，通常会为应用程序提供一组应用程序接口，称为 Socket 接口（Socket API）。应用程序可以通过 Socket 接口，来使用网络 Socket，以进行数据的传输。一个 Socket 由IP地址和端口组成。

即：Socket 地址 = IP地址 : 端口号

![image.png](http://快乐星球.site:8211/661d7df4-ff58-412b-a231-11b8fa38ceec.png)

在同一台计算机上，TCP 协议与 UDP 协议可以同时使用相同的端口（Port），而互不干扰。要想实现网络通信，至少需要一对 Socket，其中一个运行在客户端，称之为 Client Socket；另一个运行在服务器端，称之为 Server Socket。

![image.png](http://快乐星球.site:8211/cefc33aa-38c4-4b89-a5d2-e030524894e2.png)

Socket 之间的连接过程可以分为三个步骤：

（1）服务器监听

（2）客户端连接

（3）连接确认





### 1.阻塞式IO模型 (Blocking IO Model)

阻塞式 IO （Blocking IO）：应用进程从发起 IO 系统调用，至内核返回成功标识，这整个期间是处于阻塞状态的。

![image.png](http://快乐星球.site:8211/1f596279-b982-4b31-963e-7c8ce2af4906.png)


### 2.非阻塞式IO模型 (Non-blocking IO Model)

非阻塞式IO（Non-Blocking IO）：应用进程可以将 Socket 设置为非阻塞，这样应用进程在发起 IO 系统调用后，会立刻返回。应用进程可以轮询的发起 IO 系统调用，直到内核返回成功标识。

![image.png](http://快乐星球.site:8211/1d84073c-e412-43bb-8045-c3160b6a2401.png)

### 3.多路复用IO模型 (Multiplexing IO Model)

IO 多路复用（IO Multiplexin）：可以将多个应用进程的 Socket 注册到一个 Select（多路复用器）上，然后使用一个进程来监听该 Select（该操作会阻塞），Select 会监听所有注册进来的 Socket。只要有一个 Socket 的数据准备好，就会返回该Socket。再由应用进程发起 IO 系统调用，来完成数据读取。

优点：与多进程和多线程技术相比，IO 多路复用技术的最大优势是系统开销小，系统不必创建进程或线程，也不必维护这些进程，从而大大减小了系统的开销。

具体实现: select poll epoll

![image.png](http://快乐星球.site:8211/6a61264c-c5f3-4bef-8302-f26a01a470ac.png)

### 4.信号驱动IO模型 (Signal-driven IO Model)

信号驱动 IO（Signal Driven IO）：可以为 Socket 开启信号驱动 IO 功能，应用进程需向内核注册一个信号处理程序，该操作并立即返回。当内核中有数据准备好，会发送一个信号给应用进程，应用进程便可以在信号处理程序中发起 IO 系统调用，来完成数据读取了。

![image.png](http://快乐星球.site:8211/ac7c06bb-bafc-4c9e-a99b-4d5f16ffe1ff.png)

### 5.异步驱动IO模型 (Asynchronous IO Model)

异步 IO（Asynchronous IO）： 应用进程发起 IO 系统调用后，会立即返回。当内核中数据完全准备后，并且也复制到了用户空间，会产生一个信号来通知应用进程。

![image.png](http://快乐星球.site:8211/18fe2f5e-65fa-4c2c-8b09-160bafb21149.png)