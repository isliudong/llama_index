## 一、yaml资源编排示例

```yaml
# 定义控制器
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
  labels:
{{ include "service.labels.standard" . | indent 4 }}
{{ include "service.logging.deployment.label" . | indent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
{{ include "service.labels.standard" . | indent 6 }}
# 被控制对象
  template:
    metadata:
      labels:
{{ include "service.labels.standard" . | indent 8 }}
{{ include "service.microservice.labels" . | indent 8 }}
        NODE_GROUP_ID: {{ .Values.hzero.HZERO_NODE_GROUP_ID | quote }}
        PRODUCT_CODE: {{ .Values.hzero.HZERO_PRODUCT_CODE | quote }}
        PRODUCT_VERSION_CODE: {{ .Values.hzero.HZERO_PRODUCT_VERSION_CODE | quote }}
        PRODUCT_ENV_CODE: {{ .Values.hzero.HZERO_PRODUCT_ENV_CODE | quote }}
        SERVICE_CODE: {{ .Chart.Name | quote }}
        SERVICE_VERSION_CODE: {{ .Values.hzero.HZERO_SERVICE_VERSION_CODE | quote }}
      annotations:
{{ include "service.monitoring.pod.annotations" . | indent 8 }}
    spec:
      containers:
        - name: {{ .Release.Name }}
          image: "{{ .Values.image.repository }}:{{ .Chart.Version }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          env:
{{- range $name, $value := .Values.env.open }}
{{- if not (empty $value) }}
          - name: {{ $name | quote }}
            value: {{ $value | quote }}
{{- end }}
{{- end }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          # readinessProbe:
          #   httpGet:
          #     path: /health
          #     port: {{ .Values.deployment.managementPort }}
          #     scheme: HTTP
          readinessProbe:
            exec:
              command:
              - curl
              - localhost:{{ .Values.deployment.managementPort }}/health
            failureThreshold: 3
            initialDelaySeconds: 60
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 10
          resources:
{{ toYaml .Values.resources | indent 12 }}
          volumeMounts:
          - mountPath: /Charts
            name: data
{{- if not (empty .Values.persistence.subPath) }}
            subPath: {{ .Values.persistence.subPath }}
{{- end }}
        - image: docker.elastic.co/beats/filebeat:7.4.2
          imagePullPolicy: IfNotPresent
          name: filebeat
          volumeMounts:
            - name: data
              mountPath: /Charts
            {{- range $path, $config := .Values.filebeatConfig }}
            - name: filebeat-config
              mountPath: /usr/share/filebeat/{{ $path }}
              readOnly: true
              subPath: {{ $path }}
      {{- end }}
      volumes:
      - name: data
        {{- if .Values.persistence.enabled }}
        persistentVolumeClaim:
          claimName: {{ .Values.persistence.existingClaim | default ( .Release.Name ) }}
        {{- else }}
        emptyDir: {}
        {{- end }}
      - name: filebeat-config
        configMap:
          name: filebeat-config


```

## 基本属性解释

![image-20210308143804728](C:\Users\liudong\Documents\mdDocument\k8s\deployment示例.assets\image-20210308143804728.png)

## 快速编写yaml文件

### 1、使用kubectl create命令生成 yaml文件，再修改

+  kubectl create deployment web --image=nginx -o yaml --dry-run

  ![image-20210308144805697](C:\Users\liudong\Documents\mdDocument\k8s\deployment示例.assets\image-20210308144805697.png)

### 2、kubectl  get导出已有资源的yaml文件

+ kubectl get deploy nginx -o=yaml

kubectl create -f .\filebeat.yaml 运行yaml

 kubectl delete -f .\filebeat.yaml 删除yaml所属资源