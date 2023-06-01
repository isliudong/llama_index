

### 应用市场日志分发

##### 基本流程：

filebeat->logstash->数据存储

![image-20210816172836098](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20210816172836098.png)

##### filebeat收集

1、开发环境

+ 编辑配置

  /root/config/filebeat/filebeat.yml

  ```shell
  filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /hmkt/logs/hmkt-service.log
    include_lines: ['search word:']
    fields:
      source: word
    ##配置多行日志合并规则，已时间为准，一个时间发生的日志为一个事件
    multiline.pattern: '^\d{4}-\d{2}-\d{2}'
    multiline.negate: true
    multiline.match: after
  - type: log
    enabled: true
    paths:
      - /hmkt/logs/hmkt-service.log
    include_lines: ['接口审计']
    fields:
      source: functionAudit
    multiline.pattern: '^\d{4}-\d{2}-\d{2}'
    multiline.negate: true
    multiline.match: after
  - type: log
    enabled: true
    paths:
      - /hmkt/logs/hmkt-service.log
    include_lines: ['.*"actionType":.*']
    fields:
      source: actionType
  output.logstash:
    hosts: ["172.23.16.110:5044"]
  
  setup.dashboards.enabled: false
  json.keys_under_root: false
  json.overwrite_keys: true
  ####################
  setup.template.settings:
    index.number_of_shards: 1
  #index.codec: best_compression
  #_source.enabled: false
  # 允许自动生成index模板
  setup.template.enabled: false
  # # 生成index模板时字段配置文件
  #setup.template.fields: fields.yml
  # # 如果存在模块则覆盖
  #setup.template.overwrite: true
  # # 生成index模板的名称
  setup.template.name: "hmkt-test" 
  # # 生成index模板匹配的index格式       
  setup.template.pattern: "hmkt-test-*" 
  # 这里一定要注意 会在alias后面自动添加-*
  setup.ilm.rollover_alias: "hmkt-test"
  setup.ilm.pattern: "{now/d}"
  # # 生成kibana中的index pattern，便于检索日志
  #setup.dashboards.index: myfilebeat-7.0.0-*
  #filebeat默认值为auto，创建的elasticsearch索引生命周期为50GB+30天。如果不改，可以不用设置
  setup.ilm.enabled: false
  
  #logging.level: debug
  
  
  ```

+ 启动

  ```shell
  docker run -d  --restart=always --name=filebeat -v /var/log/containers/:/applogs/ -v /root/config/filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml docker.elastic.co/beats/filebeat:7.4.2
  ```

  

2、集群环境（注意各个环境namespace、output的区别）

+ 直接使用filebeat-DaemonSet.yaml创建pod

  ```yaml
  apiVersion: apps/v1
  kind: DaemonSet
  metadata:
    name: filebeat
    namespace: hmkt-dev
  spec:
    selector:
      matchLabels:
          k8s-app: filebeat
    updateStrategy:
      rollingUpdate:
        maxUnavailable: 1
      type: RollingUpdate
    template:
      metadata: 
        labels:
           k8s-app: filebeat
      spec:
        containers:
        - image: docker.elastic.co/beats/filebeat:7.4.2
          name: filebeat
          securityContext:
            runAsUser: 0
          args: [
            "-c","/usr/share/filebeat.yml",
            "-e",
            "-strict.perms=false"
          ]
          volumeMounts:
          - name: data
            mountPath: /usr/share/filebeat/data
          - name: filebeat-config
            readOnly: true
            subPath: filebeat.yml
            mountPath: /usr/share/filebeat.yml
          - name: applogs
            mountPath: /applogs/
          - name: podslogs
            mountPath: /var/log/pods/
          - name: dockerlogs
            mountPath: /var/lib/docker/containers
        volumes:
        - name: data
          emptyDir: {}
        - name: filebeat-config
          configMap:
            name: filebeat-config
        - name: applogs
          hostPath:
            path: /var/log/containers/
        - name: podslogs
          hostPath:
            path: /var/log/pods/
        - name: dockerlogs
          hostPath:
            path: /var/lib/docker/containers
  ---
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: filebeat-config
    namespace: hmkt-dev
  data:
    filebeat.yml: |-
      filebeat.inputs:
        - type: container
          enabled: true
          paths:
            - /applogs/hmkt-service-*hmkt-service*.log
          include_lines: ['search word:']
          fields:
            source: word
          ##配置多行日志合并规则，已时间为准，一个时间发生的日志为一个事件
          multiline.pattern: '^\d{4}-\d{2}-\d{2}'
          multiline.negate: true
          multiline.match: after
        - type: container
          enabled: true
          paths:
            - /applogs/hmkt-service-*hmkt-service*.log
          include_lines: ['收到支付回调 param:','收到退款回调 param:']
          fields:
            source: payparam
          ##配置多行日志合并规则，已时间为准，一个时间发生的日志为一个事件
          multiline.pattern: '^\d{4}-\d{2}-\d{2}'
          multiline.negate: true
          multiline.match: after
        - type: container
          enabled: true
          paths:
            - /applogs/hmkt-service-*hmkt-service*.log
          include_lines: ['接口审计']
          fields:
            source: functionAudit
          multiline.pattern: '^\d{4}-\d{2}-\d{2}'
          multiline.negate: true
          multiline.match: after
        - type: container
          enabled: true
          paths:
            - /applogs/hmkt-service-*hmkt-service*.log
          include_lines: ['.*"actionType":.*']
          fields:
            source: actionType
      output.logstash:
        hosts: ["logstash:5044"]
      setup.dashboards.enabled: false
      json.keys_under_root: false
      json.overwrite_keys: true
      ####################
      setup.template.settings:
        index.number_of_shards: 1
      #index.codec: best_compression
      #_source.enabled: false
      # 允许自动生成index模板
      setup.template.enabled: false
      # # 生成index模板时字段配置文件
      #setup.template.fields: fields.yml
      # # 如果存在模块则覆盖
      #setup.template.overwrite: true
      # # 生成index模板的名称
      setup.template.name: "hmkt-log"
      # # 生成index模板匹配的index格式
      setup.template.pattern: "hmkt-log-*"
      # 这里一定要注意 会在alias后面自动添加-*
      setup.ilm.rollover_alias: "hmkt-log"
      setup.ilm.pattern: "{now/d}"
      # # 生成kibana中的index pattern，便于检索日志
      #setup.dashboards.index: myfilebeat-7.0.0-*
      #filebeat默认值为auto，创建的elasticsearch索引生命周期为50GB+30天。如果不改，可以不用设置
      setup.ilm.enabled: false
  
  ```
  
  
  
  ##### logstah分发
  
  + 开发环境
  
    1、编辑配置
  
    /root/hmkt/logstash/logstash.yml
  
    ```yaml
    path.config: /usr/share/logstash/conf.d/*.conf
    path.logs: /var/log/logstash
    ```
  
    /root/hmkt/logstash/pipeline/logstash-pipeline.conf
  
    ```yaml
    input {  
       beats {
         host => "0.0.0.0"
         port => 5044
       }
    }  
    filter {
      mutate{
            remove_field => ["path","ecs","host","@version","@timestamp"]
        }
        
        if [fields][source] == "actionType" {
            grok {
              match => {
                  "message" => "(?<message>({).*?(}))"
                }
              overwrite => ["message"] 
          }
      }
      if "_grokparsefailure" in [tags] { drop { } }
    }
    
    
    output {
    
        if [fields][source] == "actionType" {
          kafka {
          codec => plain {
            format => "%{message}"
          }
          bootstrap_servers => "172.23.16.72:6667" #kafka服务器地址
          topic_id => "MARKET_BURY"
          batch_size => 5
        }
        }
    
        if [fields][source] == "word" {
          elasticsearch {
            hosts => "http://172.23.16.110:9200"
            index => "hmkt-search-log"
            pipeline =>"search-word-pipeline"
          }
        }
    
    
        if [fields][source] == "functionAudit" {
           elasticsearch {
            hosts => "http://172.23.16.110:9200"
            index => "hmkt-function-audit"
            pipeline =>"function-audit-pipeline"
          }
        }
        
    }
    
    
    ```
  
    
  
    2、启动
  
    ```shell
    docker run --rm -it -p 5044:5044 -v /root/hmkt/logstash/logstash.yml:/usr/share/logstash/config/logstash.yml -v /root/hmkt/logstash/pipeline:/usr/share/logstash/conf.d/ docker.elastic.co/logstash/logstash:7.4.2
    ```
  
    
  
  + 集群环境（注意各个环境namespace、output的区别）
  
    使用/root/hmkt/logstash/logstash-Deployment.yaml部署
  
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: logstash
      namespace: hmkt-dev
    spec:
      selector:
        matchLabels:
            k8s-app: logstash
      template:
        metadata: 
          labels:
             k8s-app: logstash
        spec:
          containers:
          - image: docker.elastic.co/logstash/logstash:7.4.2
            name: logstash
            securityContext:
              runAsUser: 0
            args: [
              #"-c","/usr/share/filebeat.yml",
              #"-e",
              #"-strict.perms=false"
            ]
            volumeMounts:
            - name: data
              mountPath: /usr/share/logstash/data
            - name: logstash-config
              subPath: logstash.yml
              mountPath: /usr/share/logstash/config/logstash.yml
            - name: logstash-config
              subPath: logstash-pipeline.conf
              mountPath: /usr/share/logstash/conf.d/logstash-pipeline.conf
          volumes:
          - name: data
            emptyDir: {}
          - name: logstash-config
            configMap:
              name: logstash-config
    
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: logstash-config
      namespace: hmkt-dev
    data:
      logstash.yml: |-
        path.config: /usr/share/logstash/conf.d/*.conf
        path.logs: /var/log/logstash
      logstash-pipeline.conf: |-
        input {  
           beats {
             host => "0.0.0.0"
             port => 5044
           }
        }  
        filter {
          mutate{
                remove_field => ["path","ecs","host","@version","@timestamp"]
            }
            if [fields][source] == "actionType" {
                grok {
                  match => {
                      "message" => "(?<text>({).*?(}))"
                    }
                  overwrite => ["message"] 
              }
          }
          if "_grokparsefailure" in [tags] { drop { } }
        }
        output {
            stdout {}
            if [fields][source] == "actionType" {
              kafka {
              codec => plain {
                format => "%{text}"
              }
              bootstrap_servers => "kafka:9092"
              topic_id => "MARKET_BURY"
              batch_size => 5
              }
            }
            if [fields][source] == "payparam" {
              elasticsearch {
                hosts => "http://192.168.17.184:9207"
                index => "hmkt-callback-log"
              }
            }
            if [fields][source] == "word" {
              elasticsearch {
                hosts => "http://192.168.17.184:9207"
                index => "hmkt-search-log"
                pipeline =>"search-word-pipeline"
              }
            }
            if [fields][source] == "functionAudit" {
              elasticsearch {
                hosts => "http://192.168.17.184:9207"
                index => "hmkt-function-audit"
                pipeline =>"function-audit-pipeline"
              }
            } 
        }
    
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: logstash
      namespace: hmkt-dev
    spec:
      ports:
      - name: tcp-client
        port: 5044
        protocol: TCP
      selector:
        k8s-app: logstash
      sessionAffinity: None
      type: ClusterIP
    ```
  
    

