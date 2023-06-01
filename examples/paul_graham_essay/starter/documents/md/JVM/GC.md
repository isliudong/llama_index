![image-20200312222842533](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20200312222842533.png)

## 一：对象：针对堆区对象实例

回收条件判断：引用计数法、GC ROOT可达性分析

## 二：触发回收机制：

GC是什么时候触发的（面试最常见的问题之一）

  由于对象进行了分代处理，因此垃圾回收区域、时间也不一样。GC有两种类型：Scavenge GC和Full GC。

### 1 Scavenge GC

  一般情况下，当新对象生成，并且在Eden申请空间失败时，就会触发Scavenge GC，对Eden区域进行GC，清除非存活对象，并且把尚且存活的对象移动到Survivor区。然后整理Survivor的两个区。这种方式的GC是对年轻代的Eden区进行，不会影响到年老代。因为大部分对象都是从Eden区开始的，同时Eden区不会分配的很大，所以Eden区的GC会频繁进行。因而，一般在这里需要使用速度快、效率高的算法，使Eden去能尽快空闲出来。

### 2 Full GC

  对整个堆进行整理，包括Young、Tenured和Perm。**Full GC因为需要对整个堆进行回收**，所以比Scavenge GC要慢，因此应该尽可能减少Full GC的次数。在对JVM调优的过程中，很大一部分工作就是对于Full GC的调节。有如下原因可能导致Full GC：

a) 年老代（Tenured）被写满；

b) 持久代（Perm）被写满；

c) System.gc()被显示调用；

d) 上一次GC之后Heap的各域分配策略动态变化；

## 三、常见的垃圾收集器

HotSpot虚拟机包含的所有收集器：

![img](C:\Users\liudong\Documents\mdDocument\JVM\GC.assets\1344248-20180318001758565-463873178.png)

- Serial收集器（复制算法)
  新生代单线程收集器，标记和清理都是单线程，优点是简单高效。是client级别默认的GC方式，可以通过`-XX:+UseSerialGC`来强制指定。
- Serial Old收集器(标记-整理算法)
  老年代单线程收集器，Serial收集器的老年代版本。
- ParNew收集器(停止-复制算法)　
  新生代收集器，可以认为是Serial收集器的多线程版本,在多核CPU环境下有着比Serial更好的表现。
- Parallel Scavenge收集器(停止-复制算法)
  并行收集器，追求高吞吐量，高效利用CPU。吞吐量一般为99%， 吞吐量= 用户线程时间/(用户线程时间+GC线程时间)。适合后台应用等对交互相应要求不高的场景。是server级别默认采用的GC方式，可用`-XX:+UseParallelGC`来强制指定，用`-XX:ParallelGCThreads=4`来指定线程数。
- Parallel Old收集器(停止-复制算法)
  Parallel Scavenge收集器的老年代版本，并行收集器，吞吐量优先。
- *CMS(Concurrent Mark Sweep)收集器（标记-清理算法）
  高并发、低停顿，追求最短GC回收停顿时间，cpu占用比较高，响应时间快，停顿时间短，多核cpu 追求高响应时间的选择。
- *CMS 和G1的垃圾回收器的原理