###  builder模式

```java
package com.wangjun.designPattern.builder;

public class Product3 {
	
	private final int id;
	private final String name;
	private final int type;
	private final float price;
	
	private Product3(Builder builder) {
		this.id = builder.id;
		this.name = builder.name;
		this.type = builder.type;
		this.price = builder.price;
	}
	
	public static class Builder {
		private int id;
		private String name;
		private int type;
		private float price;
		
		public Builder id(int id) {
			this.id = id;
			return this;
		}
		public Builder name(String name) {
			this.name = name;
			return this;
		}
		public Builder type(int type) {
			this.type = type;
			return this;
		}
		public Builder price(float price) {
			this.price = price;
			return this;
		}
		
		public Product3 build() {
			return new Product3(this);
		}
	}

}
```

可以看到builder模式将属性定义为不可变的，然后定义一个内部静态类Builder来构建属性，再通过一个只有Builder参数的构造器来生成Product对象。Builder的setter方法返回builder本身，以便可以将属性连接起来。我们就可以像下面这样使用了。

```java
Product3 p3 = new Product3.Builder()
                            .id(10)
                            .name("phone")
                            .price(100)
                            .type(1)
                            .build();
```

当然具体使用builder的情况肯定没有这么简单，但是思路大致一样：先通过某种方式取得构造对象需要的所有参数，再通过这些参数一次性构建这个对象。比如MyBatis中SqlSessionFactoryBuilder就是通过读取MyBatis的xml配置文件来获取构造SqlSessionFactory所需要的参数的。