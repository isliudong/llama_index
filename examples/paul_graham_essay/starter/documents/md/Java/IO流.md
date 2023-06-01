# [java中InputStream和OutputStream的使用场景](https://segmentfault.com/a/1190000017542212)

java的I/O中有**两种**基本的流类型
分别是
**输入**流InputStream
**输出**流OutputStream

有的时候很容易搞混使用的顺序，只需要记住：
输入流是把数据从别的地方读入本程序的内存
输出流则是把数据从本程序的内存写到别处

比如说：
我在程序里new FileInputStream(...)
是把文件中的内容读入内存
new FileOutputStream(...)
则是把内存中的数据写入文件

又例如：
new Socket().getInputStream()
是为了从套接字读数据到内存
new Socket().getOutputStream()
是为了从内存写数据到套接字

再例如：
new URL(...).getInputStream()
是为了把URL定位到的数据读入内存
new URL(...).getOutputStream()
是为了把内存的数据写入URL定位的资源中去

最后只需要记住：
**划分输入/输出流是从程序运行时所在的内存考虑的，读入内存是输入，读出内存是输出。**
**并且输入流只能读数据，输出流只能写数据！也就是说输入和输出流都是单向的！**