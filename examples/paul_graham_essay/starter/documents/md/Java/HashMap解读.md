# HashMap解读

![image-20200706191835895](C:\Users\liudong\Documents\mdDocument\HashMap解读.assets\image-20200706191835895.png)

## 一.HashMap实现

0000 0000 1000 ****

0000 0000 0100 0***

hashtable：

jdk1.7：数组+链表

hash碰撞解决：hashcode相同放入相同数组索引，用头插法以链表形式插入当前数组位置，即将它指向原数据。

扩容条件：的扩容条件有两个,1.数组元素到达阈值，且新来的元素插入的位置有元素占着

1.7扩容问题：头插法（快）会产生链表数据方向反转，并可能产生环形链表导致死锁

jdk1.8：数组+链表+红黑树，增加segment分段锁

扩容条件：摒弃了第二个条件，只要数组使用了12（默认）个位置就进行扩容，之前元素的位置不会发生改变

hash碰撞解决：当一个链表长度达到8时，将转换为红黑树，这是发生hash碰撞时的第一个不同点；

1.8扩容：尾插法，当计算出元素在数组中的位置相同时，则生成链表，并将新的元素插入到尾部，假如链表上元素超过了8个，那么链表将被改为红黑树，同时也提高了增删查效率
当数组元素个数达到了阈值，那么此时不需要判断新的元素的位置是否为空，数组都会扩容，2倍扩容
扩容完之后，之前的元素位置不会发生改变，也就不会产生死锁。

## 二.位运算的使用



## 三.多线程JDk7HashMap扩容阻塞



## 四.JDK8关于HashMap的优化

concurrenthashmap红黑树产生：链表到达8 -->map扩容到64减少碰撞 -->到达64则转化为红黑树解决碰撞带来的速度问题 -->小于6退化为链表

尾插法解决扩容死锁，但是任然存在扩容数据丢失问题

## 五.使用技巧

# 排序算法总结：

## 1.定义

将杂乱无章的[数据元素](https://baike.baidu.com/item/数据元素)，通过一定的方法按[关键字](https://baike.baidu.com/item/关键字)顺序排列的过程叫做排序。

## 2.排序的稳定性

即当关键字相同时，不改变原始顺序则称之为稳定排序算法。

## 3.排序的分类之内排序和外排序

即将待排序记录全部置于内存中操作我们称之为内排序，否则为外排序

## 4.常见排序算法

### （1）[冒泡排序]([https://baike.baidu.com/item/%E5%86%92%E6%B3%A1%E6%8E%92%E5%BA%8F](https://baike.baidu.com/item/冒泡排序))

基本思想：比较相邻记录关键字，按顺序交换，直到没有反序为止。

一般实现：

```java
public void bubbleSort(int[] a){
        int length=a.length;
        for (int i=0;i<length;i++){
            for (int j=i;j<length;j++){
                if (a[i]>a[j]){
                    int temp=a[i];
                    a[i]=a[j];
                    a[j]=temp;
                }
            }
        }
    }
```

优化基本思路：添加标记记录正序，减少正序无用遍历

如下优化实现：

```java
void bubbleSort1(int a[], int nlength)
{
	for (int i = 0; i < nlength - 1; i++)
	{
		int flag = 0;
		for (int j = 0; j < nlength - 1 - i; j++)
		{
			if (a[j] > a[j + 1])
			{
				int tmp = a[j];
				a[j] = a[j + 1];
				a[j + 1] = tmp;
				flag = 1;
			}
		}

		if (flag == 0)  
		{
			break;
		}
	}
}

```

冒泡排序时间复杂度：O(n^2)

### (2)简单选择排序

基本思想：选择未排序中的关键字的最小的放入已排序的尾部（从小到大）。

一般实现：

```java
public void selectionSort(int[] arr){
        
       for (int i = 0; i < arr.length - 1; i++) {    
            int  min = i;
            for (int j = i + 1; j < arr.length; j++) {
                  if (arr[min] > arr[j]) {
                       min = j;
                  }
            }
            if (min != i) {
               int tmp = arr[min];
               arr[min] = arr[i];
               arr[i] = tmp;
            }             
      }
 
}
```

选择排序时间复杂度：O(n^2)

### （3）直接插入排序

基本实现：将无序表中一个

