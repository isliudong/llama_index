针对k8s启动filebeat
docker run -d  --restart=always --name=filebeat -v /var/log/containers/:/applogs/ -v /root/config/filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml -v /var/log/pods/:/var/log/pods/ -v /var/lib/docker/containers:/var/lib/docker/containers docker.elastic.co/beats/filebeat:7.4.2



docker run -d  --restart=always --name=filebeat  -v E:\docker-disk\filebeat\filebeat.yml:/usr/share/filebeat/filebeat.yml  filebeat:7.4.2

修改文件权限
chown -R 1000:1000 /var/lib/docker/containers/

日志路径问题、多了一个默认命名空间filebeat


SPRINF_LOGGING_FILE: Charts/hmkt-service.log

filebeatConfig:
  filebeat.yml: |
    filebeat.inputs:
      - type: log
        enabled: true
        paths:
          - /Charts/hmkt-service.log
        include_lines: ['search word:']
        ##配置多行日志合并规则，已时间为准，一个时间发生的日志为一个事件
        multiline.pattern: '^\d{4}-\d{2}-\d{2}'
        multiline.negate: true
        multiline.match: after
    output.elasticsearch:
      hosts: ["http://192.168.17.184:9207"]
      index: "hmkt-search-log"
      pipelines:
        - pipeline: "search-word-pipeline"
    setup.dashboards.enabled: false
    setup.template.name: "hmkt-search-log"
    setup.template.pattern: "hmkt-search-log-*"
    setup.ilm.enabled: false
    json.keys_under_root: false
    json.overwrite_keys: true