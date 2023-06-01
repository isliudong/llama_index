GET suggest_products/_search
{
  "query": {
    "simple_query_string": {
      "query": "have hzero",
      "fields": ["suggest"]
    }
  },
  "sort" : [
    { "weight": { "order": "asc","unmapped_type" : "long"}}
  ]
}
GET _cat/indices

# 模拟管道
POST _ingest/pipeline/_simulate
{
  "pipeline" :
  {
    "description": "_description",
    "processors" : [
        {
            "grok": {
              "field": "message",
              "patterns": ["%{TIMESTAMP_ISO8601:time}"]
            }
    },{
      "grok": {
              "field": "message",
              "patterns": ["(?<word>(?<=search word:)(.*)/?)"]
            },"remove": {
              "field": ["message"]
            }
    }
    ]
  },
  "docs": [
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "message": "2021-02-24 14:27:25.843  INFO 9844 --- [  XNIO-3 task-3] o.h.h.p.a.s.open.OpenProductService      : search word:hzero"
      }
    },
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "message": "search word:hzero"
      }
    },
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "message": "rab"
      }
    }
  ]
}


# 模拟管道2
POST _ingest/pipeline/_simulate
{
  "pipeline" :
  {
    "description": "_description",
    "processors" : [
        {
            "grok": {
              "field": "message",
              "patterns": ["%{TIMESTAMP_ISO8601:log_time}"]
            },"remove": {
              "field": "message"
            },
    	"date": {
    		"field": "log_time",
    		"formats": ["yyyy-MM-dd HH:mm:ss:SSS"],
    		"timezone": "Asia/Shanghai",
    		"target_field": "@timestamp"
    	}
    }
    ]
  },
  "docs": [
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "message": "2021-02-24 13:54:53.002  INFO 9844 --- [freshExecutor-0] com.netflix.discovery.DiscoveryClient    : search word:hzero"
      }
    }
  ]
}
DELETE _ingest/pipeline/search-word-pipeline
GET _ingest/pipeline

# 添加管道

PUT _ingest/pipeline/search-word-pipeline
{
	"description" : "search word logs pipeline",
    "processors" : [
        {
            "grok": {
              "field": "message",
              "patterns": ["%{TIMESTAMP_ISO8601:time}"]
            }
        },
        {
            "grok": {
              "field": "message",
              "patterns": ["(?<word>(?<=search word:)(.*)/?)"]
              },
              "remove": {
              "field": ["message"]
            }
        }
    ]
}


GET suggest_products/_search
{
  "query": {
    "match_all": {}
  }
}

GET hmkt-search-log/_mapping
DELETE suggest_products
POST suggest_products/_delete_by_query
{
  "query": { 
    "term": {
      "suggest": "have"
    }
  }
}

PUT /hmkt-search-log
{
    "settings" : {
        "number_of_shards" : 1
    },
    "mappings" : {
        "properties" : {
            "time" : {"type" : "date","format": "yyyy-MM-dd HH:mm:ss.SSS||yyyy-MM-dd||epoch_millis"},
            "word" : {"type" : "keyword"}
        }
    }
}

POST suggest_products/_search
{

  "suggest": {
    "article-suggester": {
      "prefix": "汉",
      "completion": {
        "field": "suggest",
        "size": 10
      }
    }
  }
}

# 热词统计
POST hmkt-search-log/_search?size=0
{
  "aggs": {
    "per_count": {
      "terms": {
        "field": "word",
        "min_doc_count": 1,
        "size": 2,
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}