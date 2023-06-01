```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logstash
  namespace: hmkt
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
  namespace: hmkt
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
          bootstrap_servers => "172.23.32.111:9092"
          topic_id => "MARKET_BURY"
          batch_size => 5
          }
        }
        if [fields][source] == "payparam" {
          elasticsearch {
            hosts => "http://172.23.32.118:9200"
            index => "hmkt-callback-log"
          }
        }
        if [fields][source] == "word" {
          elasticsearch {
            hosts => "http://172.23.32.118:9200"
            index => "hmkt-search-log"
            pipeline =>"search-word-pipeline"
          }
        }
        if [fields][source] == "functionAudit" {
          elasticsearch {
            hosts => "http://172.23.32.118:9200"
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
  namespace: hmkt
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





```
# Default values for api-gateway.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: registry.choerodon.com.cn/hzero-hcop/hzero-front-ecological

# preJob:
#   preConfig:
#     mysql:
#       host: localhost
#       port: 3306
#       username: choerodon
#       password: 123456
#       dbname: iam_service

service:
  enable: false
  type: ClusterIP
  port: 80
  name: hzero-front-ecological

ingress:
  enable: false

env:
  open:
    BUILD_BASE_PATH: /
    BUILD_PUBLIC_URL: /
    PUBLIC_URL: /
    BUILD_CLIENT_ID: client
    BUILD_WEBSOCKET_HOST: http://172.23.40.64:8080/hpfm/sock-js
    PLATFORM_VERSION: SAAS
    IM_ENABLE: false
    BUILD_IM_WEBSOCKET_HOST: ws://172.23.40.64:9876
    SKIP_NO_CHANGE_MODULE: true
    BUILD_TOP_MENU_LABELS: HZERO_MENU
    BUILD_API_HOST: http://172.23.40.64:8080
    PUPPETEER_SKIP_CHROMIUM_DOWNLOAD: true
    BUILD_MULTIPLE_SKIN_ENABLE: false
    BUILD_TOP_MENU_UNION_LABEL: false
    BUILD_INVALID_TIME: 120
    BUILD_CUSTOMIZE_ICON_NAME: customize-icon
    BUILD_HISTORY_ENABLE: false
    BUILD_SVG_ICON_ENABLE: true
    API_HOST: http://172.23.40.64:8080

logs:
  parser: nginx

resources:
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources,such as Minikube. If you do want to specify resources,uncomment the following
  # lines,adjust them as necessary,and remove the curly braces after 'resources:'.
  limits:
    # cpu: 100m
    # memory: 2Gi
  requests:
    # cpu: 100m
    # memory: 1Gi
```

