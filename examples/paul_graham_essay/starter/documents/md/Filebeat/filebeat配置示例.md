```yml
filebeat.inputs:
- type: log
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
- type: log
  enabled: true
  paths:
    - /applogs/hmkt-service-*.log
  include_lines: ['接口审计']
  fields:
    source: functionAudit
  multiline.pattern: '^\d{4}-\d{2}-\d{2}'
  multiline.negate: true
  multiline.match: after
output.elasticsearch:
  hosts: ["http://192.168.17.184:9207"]
  indices:
    - index: "hmkt-search-log"
      when.equals:
        fields:
          source: "word"
    - index: "hmkt-function-audit"
      when.equals:
        fields:
          source: "functionAudit"
  pipelines:
        - pipeline: "search-word-pipeline"
          when.equals:
            fields:
              source: "word"
        - pipeline: "function-audit-pipeline"
          when.equals:
            fields:
              source: "functionAudit"
setup.dashboards.enabled: false
json.keys_under_root: false
```

