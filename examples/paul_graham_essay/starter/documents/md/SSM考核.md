# SSM考核

## 概述

1. 本次考核内容为物料管理功能
1. 本次考核时间为5天(含周末 20-08-01~20-08-05)
1. 本次考核需要将所有业务要求考点都操作一遍，并录屏后转为gif文件，放至项目根目录中
1. 本次考核完成后将项目提交给对应的指导教师，指导教师根据完成情况考核评分

## 业务要求

1. 完成一个物料管理页面
1. 无需登录，打开系统即可使用
1. 首页实现对物料数据的分页条件查询
1. 点击新增按钮，出现新增物料功能弹框(或侧滑框)，录入必输字段和非必输字段后，点击保存，将录入的数据传入后台保存，同时自动生成ID和物料编号(规则为当前DB中ID最大的物料的物料编号 + 1)。保存成功后功能框关闭，同时主页自动重新执行一次查询。如果在保存之前点击关闭按钮，则直接关闭功能框
1. 点击修改按钮，出现修改物料功能弹框(或侧滑框)，录入必输字段和非必输字段后，点击保存，将录入的数据传入后台保存，更新数据信息。注意需校验某些字段不能编辑(详见原型图)。保存成功后功能框关闭，同时主页自动重新执行一次查询。如果在保存之前点击关闭按钮，则直接关闭功能框
1. 点击删除按钮，出现提示框["确认删除?"]，点击是，将本条数据从DB中删除，同时自动重新执行一次查询。点击否则关闭提示框，不做任何操作

## 扩展要求

*此部分要求作为额外加分项，但总分不会超过满分(20分)。*

1. 查询功能实现后端排序，既前端可以动态设置排序条件传至后端，后端根据条件动态拼接排序sql
1. 实现勾选批量删除功能
1. 实现Excel导出功能，导出的Excel字段及其值要求和页面上完全一样，所见即所得
1. 后端实现hibernate validation(JSR-303)，防止前端恶意攻击。校验规则要求和数据库约束一致(必输、长度限制等)

## 开发要求

1. 使用`Spring + Spring MVC + Mybatis + JSP(或其他模板引擎)`。或者使用`React(Angular/Vue) + Spring boot web + Mybatis`。请注意只有这两种组合是允许的，其他组合**没有成绩**
1. Mybatis的使用必须是使用`Mapper.java`接口+`Mapper.xml`写sql，其他用法Mybatis项目不得分
1. 要求在代码中引入Service层做注解式数据库事务控制
1. 严格按照alibaba代码规范开发，否则会出现扣分

## 附件

### 表设计

```sql
CREATE TABLE `ssm_item` (
  `item_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '表ID，主键，供其他表做外键',
  `item_code` varchar(60) COLLATE utf8mb4_bin NOT NULL COMMENT '物料编码',
  `item_uom` varchar(60) COLLATE utf8mb4_bin NOT NULL COMMENT '物料单位',
  `item_description` varchar(240) COLLATE utf8mb4_bin NOT NULL COMMENT '物料描述',
  `start_active_date` date DEFAULT NULL COMMENT '生效起始时间',
  `end_active_date` date DEFAULT NULL COMMENT '生效结束时间',
  `enabled_flag` tinyint(1) NOT NULL DEFAULT '1' COMMENT '启用标识',
  `object_version_number` bigint(20) NOT NULL DEFAULT '1' COMMENT '版本号',
  `creation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` bigint(20) NOT NULL DEFAULT '-1',
  `last_updated_by` bigint(20) NOT NULL DEFAULT '-1',
  `last_update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`item_id`),
  UNIQUE KEY `ssm_item_u1` (`item_code`),
  KEY `ssm_item_n1` (`item_description`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='物料';
```

### 原型图

[原型图](./物料管理.rp)