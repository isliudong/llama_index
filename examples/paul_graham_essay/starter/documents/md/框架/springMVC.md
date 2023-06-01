异常处理

----

ExceptionHandlerExceptionResolver : 处理注解@ExceptionHandler 用于自定义异常处理
ResponseStatusExceptionResolver : 处理注解@ResponseStatus，用于自定义异常类型
DefaultHandlerExceptionResolver :判断是否SpringMVC自带的异常

springMVC运行流程

----

1、所有请求,前端控制器( DispatcherServlet )收到请求,调用doDispatch进行处理
2、根据HandlerMapping中保存的请 求映射信息找到,处理当前请求的,处理器执行链(包含拦
截器)
3、根据当前处理器找到他的HandlerAdapter (适配器)
4、拦截器的preHandle先执行
5、适配器执行目标方法，返回ModelAndView
    1 )、ModelAttribute注解标注的方法提前运行
    2)、执行目标方法的时候(确定目标方法用的参数)
          1 )、有注解
           2)、没注解:
                 1)、 看是否Model、Map以及其他的
                 2 )、如果是自定义类型
                        1 )、从隐含模型中看有没有,如果有就从隐含模型中拿
                        2)、如果没有,再看是否SessionAttributes标注的属性,如果是从Session中拿,如果拿不到会抛                               异常

​                        3)、都不是,就利用反射创建对象

6、拦截器的postHandle执行
7、处理结果; (页面渲染流程)
     1 )、如果有异常使用异常解析器处理异常;处理完后还会返回ModelAndView
     2)、调用render进行页面渲染
           1 )、视图解析器根据视图名得到视图对象
           2)、视图对象调用render方法;
           3 )、执行拦截器的afterCompletion ;

spring、SpringMVC 父子容器，注意事物配置可能错误配在另一个容器中

