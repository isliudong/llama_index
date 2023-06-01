```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: filebeat
  namespace: hmkt
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
  namespace: hmkt
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

