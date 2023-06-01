## 一、Java面试题J

熟练掌握java是很关键的，大公司不仅仅要求你会使用几个api，更多的是要你熟悉源码实现原理，甚至要你知道有哪些不足，怎么改进，还有一些java有关的一些算法，设计模式等等。

##### （一） java基础面试知识点

- java中==和equals和hashCode的区别

  1、==比较值

  2、equals为jdk1.8中Object类中默认比较传入对象的引用：

  ```java
  public boolean equals(Object obj) {
          return (this == obj);
      }
  ```

  具体对象可对其重写，如String对象则比较字符串是否等效：

  ```java
  public boolean equals(Object anObject) {
          if (this == anObject) {
              return true;
          }
          if (anObject instanceof String) {
              String anotherString = (String)anObject;
              int n = value.length;
              if (n == anotherString.value.length) {
                  char v1[] = value;
                  char v2[] = anotherString.value;
                  int i = 0;
                  while (n-- != 0) {
                      if (v1[i] != v2[i])
                          return false;
                      i++;
                  }
                  return true;
              }
          }
          return false;
      }
  ```

  3、hsahCode默认比较对象地址是否相等

  jdk1.8中默认hashCode为native修饰的接口，即调用本地方法（外部代码实现）

- int、char、long各占多少字节数（ byte short int long double float（4） char boolean ）

  int 4字节、char 2字节、long 8字节

- int与integer的区别

  1、int是基本数据类型；而integer是int的包装对象

  2、int作为方法成员变量初始化在栈区默认值为0；而integer对象初始化在堆区默认为null

  3、映射知识点：

  基本数据类型作为方法成员变量即局部变量创建于栈区，随着方法栈的销毁而丢失，但是基本数据类型作为全局变量时放置于堆区；而对象则全部存放于堆区，区别是作为局部成员时对象地址存放于栈区，对象本身存放于堆区，作为全局变量是则全部存放于堆区。

  

- 谈谈对java多态的理解

  

  1、多态：父类引用指向子类对象、在执行期间判断引用对象的实际类型并根据实际类型调用相关方法，比如同一消息可以根据发送对象的不同而采用多种不同的行为方式

  2、多态的作用（多态就是把做什么和怎么做分开了）：消除类型之间的耦合

  3、表面实现多态（实现多态的三要素）继承、重写、父类引用指向子类对象（即，声明是父类，实际指向的是子类的一个对象）

  3、多态底层实现原理（动态绑定）：是指在执行期间判断所引用对象的实际类型，根据其实际的类型调用其相应的方法。

  4、其他  面向对象的三大特征：封装、继承、多态

- String、StringBuffer、StringBuilder区别

  1、https://blog.csdn.net/yiguang_820/article/details/93849455

- 什么是内部类？内部类的作用

- 抽象类和接口区别

- 抽象类的意义

- 抽象类与接口的应用场景

- 抽象类是否可以没有方法和属性？

- 接口的意义

- 泛型中extends和super的区别

- 父类的静态方法能否被子类重写

- 进程和线程的区别

- final，finally，finalize的区别

- 序列化的方式

- Serializable 和Parcelable 的区别

- 静态属性和静态方法是否可以被继承？是否可以被重写？以及原因？

- 静态内部类的设计意图

- 成员内部类、静态内部类、局部内部类和匿名内部类的理解，以及项目中的应用

- 谈谈对kotlin的理解

- 闭包和局部内部类的区别

- string 转换成 integer的方式及原理

##### （二） java深入源码级的面试题（有难度）

- 哪些情况下的对象会被垃圾回收机制处理掉？

- 可以被看做是GC Roots的对象呢？

  - 虚拟机栈(栈桢中的本地变量表)中的引用的对象
  - 方法区中的类静态属性引用的对象
  - 方法区中的常量引用的对象
  - 本地方法栈中JNI（Native方法）的引用的对象

- 讲一下常见编码方式？

- utf-8编码中的中文占几个字节；int型几个字节？

- 静态代理和动态代理的区别，什么场景使用？

- 动态代理原理：

  **JDK动态代理**：利用反射机制生成一个实现代理接口的匿名类，在调用具体方法前调用InvokeHandler来处理。
  **CGlib动态代理**：利用ASM（开源的Java字节码编辑库，操作字节码）开源包，将代理对象类的class文件加载进来，通过修改其字节码生成子类来处理。

  **区别**：JDK代理只能对实现接口的类生成代理；CGlib是针对类实现代理，对指定的类生成一个子类，并覆盖其中的方法，这种通过继承类的实现方式，不能代理final修饰的类。

- Java的异常体系

   Java把异常作为一种类，当做对象来处理。所有异常类的基类是Throwable类，两大子类分别是Error和Exception。

    　　系统错误由Java虚拟机抛出，用Error类表示。Error类描述的是内部系统错误，例如Java虚拟机崩溃。这种情况仅凭程序自身是无法处理的，在程序中也不会对Error异常进行捕捉和抛出。

    　　异常（Exception）又分为RuntimeException(运行时异常)和CheckedException(检查时异常)，两者区别如下：

  - RuntimeException：程序运行过程中才可能发生的异常。一般为代码的逻辑错误。例如：类型错误转换，数组下标访问越界，空指针异常、找不到指定类等等。
  - CheckedException：编译期间可以检查到的异常，必须显式的进行处理（捕获或者抛出到上一层）。例如：IOException, FileNotFoundException等等。

  ![img](C:\Users\liudong\Documents\mdDocument\Java常见面试题.assets\20160331115514210)

- 谈谈你对解析与分派的认识。

- 修改对象A的equals方法的签名，那么使用HashMap存放这个对象实例的时候，会调用哪个equals方法？

- Java中实现多态的机制是什么？

- 泛型

  [泛型原理及其使用](https://www.cnblogs.com/jing99/p/11868986.html)

   一、什么是泛型

  　　Java从1.5之后支持泛型，泛型的本质是类型参数，也就是说所操作的数据类型被指定为一个参数。这种参数类型可以用在类、接口和方法的创建中，分别称为泛型类、泛型接口、泛型方法。

  　　若不支持泛型，则表现为支持Object，不是特定的泛型。泛型是对 Java 语言的类型系统的一种扩展，以支持创建可以按类型进行参数化的类。可以把类型参数看作是使用参数化类型时指定的类型的一个占位符，就像方法的形式参数是运行时传递的值的占位符一样。许多重要的类，比如集合框架，都已经成为泛型化的了。

   二、泛型有什么优点

  　　泛型的好处是在编译的时候检查类型安全，并且所有的强制转换都是自动和隐式的，以提高代码的重用率。

   　　**1、类型安全**

  　　泛型的主要目标是提高 Java 程序的类型安全。通过知道使用泛型定义的变量的类型限制，编译器可以在一个高得多的程度上验证类型假设。没有泛型，这些假设就无法落实到代码中，仅仅能停留在设计方案或者注释中。 

   　　**2、消除强制类型转换**

  　　泛型的一个附带好处是，消除源代码中的许多强制类型转换。这使得代码更加可读，并且减少了强制转换代码和出错机会。

  　　**3、潜在的性能收益**

  　　泛型为较大的优化带来可能。在泛型的初始实现中，编译器将强制类型转换（没有泛型的话，程序员会指定这些强制类型转换）插入生成的字节码中。

- 如何将一个Java对象序列化到文件里？

- 说说你对Java反射的理解

- 说说你对Java注解的理解

- 说说你对依赖注入的理解

- 说一下泛型原理，并举例说明

- Java中String的了解

- String为什么要设计成不可变的？

   1、便于实现字符串池（String pool）

  在Java中，由于会大量的使用String常量，如果每一次声明一个String都创建一个String对象，那将会造成极大的空间资源的浪费。Java提出了String pool的概念，在堆中开辟一块存储空间String pool，当初始化一个String变量时，如果该字符串已经存在了，就不会去创建一个新的字符串变量，而是会返回已经存在了的字符串的引用。

  ```
  String a = "Hello world!";
  String b = "Hello world!";
  ```

  如果字符串是可变的，某一个字符串变量改变了其值，那么其指向的变量的值也会改变，String pool将不能够实现！

  2、使多线程安全

   看下面这个场景，一个函数appendStr()在不可变的String参数后面加上一段“bbb”后返回。appendSb()负责在可变的StringBuilder后面加"bbb"。

  [![复制代码](C:\Users\liudong\Documents\mdDocument\Java常见面试题.assets\copycode.gif)](javascript:void(0);)

  ```
  public class test {
    // 不可变的String
    public static String appendStr(String s) {
        s += "bbb";
        return s;
    }
  
    // 可变的StringBuilder
    public static StringBuilder appendSb(StringBuilder sb) {
        return sb.append("bbb");
    }
    
    public static void main(String[] args) {
        String s = new String("aaa");
        String ns = test.appendStr(s);
        System.out.println("String aaa>>>" + s.toString());
        // StringBuilder做参数
        StringBuilder sb = new StringBuilder("aaa");
        StringBuilder nsb = test.appendSb(sb);
        System.out.println("StringBuilder aaa >>>" + sb.toString());
    }
  }
  ```

  3、避免安全问题

  在网络连接和数据库连接中字符串常常作为参数，例如，网络连接地址URL，文件路径path，反射机制所需要的String参数。其不可变性可以保证连接的安全性。如果字符串是可变的，黑客就有可能改变字符串指向对象的值，那么会引起很严重的安全问题。

  因为String是不可变的，所以它的值是不可改变的。但由于String不可变，也就没有任何方式能修改字符串的值，每一次修改都将产生新的字符串，如果使用char[]来保存密码，仍然能够将其中所有的元素设置为空和清零，也不会被放入字符串缓存池中，用字符串数组来保存密码会更好。

  4、加快字符串处理速度

- Object类的equal和hashCode方法重写，为什么？

##### （三） 数据结构

- 常用数据结构简介

- 并发集合了解哪些？

- 列举java的集合以及集合之间的继承关系

- 集合类以及集合框架

- 容器类介绍以及之间的区别（容器类估计很多人没听这个词，Java容器主要可以划分为4个部分：List列表、Set集合、Map映射、工具类（Iterator迭代器、Enumeration枚举类、Arrays和Collections），具体的可以看看这篇博文 [Java容器类](http://alexyyek.github.io/2015/04/06/Collection/)）

- List,Set,Map的区别

- List和Map的实现方式以及存储方式

- HashMap的实现原理

- HashMap数据结构？

- HashMap源码理解

- HashMap如何put数据（从HashMap源码角度讲解）？

- HashMap容量为什么是2的次幂

  当(n - 1) 和hash做与运算时，会保留hash中后x位的1好处有：

  - &运算速度快，至少比%取模运算快
  - 能保证索引值肯定在HashMap的容量大小范围内
  - (n - 1) & hash的值是均匀分布的，可以减少hash冲突

- HashMap怎么手写实现？

- ConcurrentHashMap的实现原理

- ArrayMap和HashMap的对比

- HashTable实现原理

- TreeMap具体实现

- HashMap和HashTable的区别

- HashMap与HashSet的区别

- HashSet与HashMap怎么判断集合元素重复？

- 集合Set实现Hash怎么防止碰撞

- ArrayList和LinkedList的区别，以及应用场景

- 数组和链表的区别

- 二叉树的深度优先遍历和广度优先遍历的具体实现

- 堆的结构

- 堆和树的区别

- 堆和栈在内存中的区别是什么(解答提示：可以从数据结构方面以及实际实现方面两个方面去回答)？

- 什么是深拷贝和浅拷贝

- 手写链表逆序代码

- 讲一下对树，B+树的理解

- 讲一下对图的理解

- 判断单链表成环与否？

- 链表翻转（即：翻转一个单项链表）

- 合并多个单有序链表（假设都是递增的）

- nginx负载均衡算法

  Nginx本身支持的算法：轮询(RR)、加权轮询(WRR)、ip_hash、least_conn

  

##### （四） 线程、多线程和线程池

- 开启线程的三种方式？
- 线程和进程的区别？
- 为什么要有线程，而不是仅仅用进程？
- run()和start()方法区别
- 如何控制某个方法允许并发访问线程的个数？
- 在Java中wait和seelp方法的不同；
- 谈谈wait/notify关键字的理解
- 什么导致线程阻塞？
- 线程如何关闭？
- 讲一下java中的同步的方法
- 数据一致性如何保证？
- 如何保证线程安全？
- 如何实现线程同步？
- 两个进程同时要求写或者读，能不能实现？如何防止进程的同步？
- 线程间操作List
- Java中对象的生命周期
- Synchronized用法
- synchronize的原理
- 谈谈对Synchronized关键字，类锁，方法锁，重入锁的理解
- static synchronized 方法的多线程访问和作用
- 同一个类里面两个synchronized方法，两个线程同时访问的问题
- volatile的原理
- 谈谈volatile关键字的用法
- 谈谈volatile关键字的作用
- 谈谈NIO的理解
- synchronized 和volatile 关键字的区别
- synchronized与Lock的区别
- ReentrantLock 、synchronized和volatile比较
- ReentrantLock的内部实现
- lock原理
- 死锁的四个必要条件？
- 怎么避免死锁？
- 对象锁和类锁是否会互相影响？
- 什么是线程池，如何使用?
- Java的并发、多线程、线程模型
- 谈谈对多线程的理解
- 多线程有什么要注意的问题？
- 谈谈你对并发编程的理解并举例说明
- 谈谈你对多线程同步机制的理解？
- 如何保证多线程读写文件的安全？
- 多线程断点续传原理
- 断点续传的实现

##### （五）并发编程有关知识点（这个是一般Android开发用的少的，所以建议多去看看）：

平时Android开发中对并发编程可以做得比较少，Thread这个类经常会用到，但是我们想提升自己的话，一定不能停留在表面，,我们也应该去了解一下java的关于线程相关的源码级别的东西。

**学习的参考资料如下：**

> Java 内存模型

- [java线程安全总结](http://www.iteye.com/topic/806990)
- [深入理解java内存模型系列文章](http://ifeve.com/java-memory-model-0/)

> 线程状态：

- [一张图让你看懂JAVA线程间的状态转换](https://my.oschina.net/mingdongcheng/blog/139263)

> 锁：

- [锁机制：synchronized、Lock、Condition](http://blog.csdn.net/vking_wang/article/details/9952063)
- [Java 中的锁](http://wiki.jikexueyuan.com/project/java-concurrent/locks-in-java.html)

> 并发编程：

- [Java并发编程：Thread类的使用](http://www.cnblogs.com/dolphin0520/p/3920357.html)
- [Java多线程编程总结](http://blog.51cto.com/lavasoft/27069)
- [Java并发编程的总结与思考](https://www.jianshu.com/p/053943a425c3#)
- [Java并发编程实战-----synchronized](http://www.cnblogs.com/chenssy/p/4701027.html)
- [深入分析ConcurrentHashMap](http://www.infoq.com/cn/articles/ConcurrentHashMap#)

