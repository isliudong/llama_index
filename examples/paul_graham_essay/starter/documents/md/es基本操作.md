GET _search
{
  "query": {
    "match_all": {}
  }
}

GET  story-docs/_search
{

  "query": {
    "match": {
      "content": "咣咭"
      

    }

  }
}

GET _cat/indices

GET com-doc6/_mapping

//查看mapping
GET suggest-com-doc/_mapping
GET com-doc7/_settings
GET com-doc/_count

GET suggest-com-doc/_search

POST _bulk/?refresh=true
{ "index": { "_index": "suggest-com-doc" }}
{ "suggest": "ceshi"}

index {[suggest-com-doc][completion][null], source[{"suggest":}]}

POST users/_doc/1
{
  "name":"ld",
  "sex":"大浪"
}

GET story-docs/_search

POST com-doc2/_bulk/?refresh=true
{ "index" : {} }
{ "description": "中国很强","title":"中国很强啊"}


"suggest_mode":"always popular missing"

// 单词建议
GET com-doc6/_search
{
  "suggest": {
    "description_suggest": {
      "text": "Jave",
      "term": {
        "field": "description",
        "suggest_mode":"missing"
      }
    }
  }
}

// 直接单词补全(丢失该字段分词效果)
GET com-doc2/_search
{
  "suggest": {
    "title_prefix_suggest": {
      "prefix": "h",
      "completion":{
        "field":"description"
      }
    }
  }
}

// 新建suggest字段用于补全，导入分词库到该字段

GET _analyze
{
  "text": "万里长城是中国的象征",
  "analyzer": "ik_smart"
}
PUT suggest-com-doc

PUT suggest-com-doc
{
  "mappings" : {
      "properties" : {
        "suggest" : {
          "analyzer": "ik_smart",
          "type" : "completion",
          "search_analyzer": "ik_smart" 
      },
      "weight" : {
          "type" : "integer"
        }
    }
  }
}

PUT suggest-com-doc
{
   "mappings" : {
      "properties" : {
        "suggest" : {
          "type" : "completion",
          "analyzer": "ik_smart",
          "search_analyzer": "ik_smart"
        }
      }
    }
}


//新建可自动补全的索引
PUT com-doc7
{
  "mappings" : {
      "properties" : {
        "associationId" : {
          "type" : "long"
        },
        "commentCount" : {
          "type" : "long"
        },
        "creator" : {
          "type" : "long"
        },
        "description" : {
          "analyzer": "ik_smart", 
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
          

        },
        "gmtCreate" : {
          "type" : "long"
        },
        "gmtModified" : {
          "type" : "long"
        },
        "id" : {
          "type" : "long"
        },
        "imgUrl" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "likeCount" : {
          "type" : "long"
        },
        "tag" : {
          "analyzer": "ik_smart",
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "title" : {
          "analyzer": "ik_smart",
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "title_suggest" : {
          "analyzer": "ik_smart",
          "type" : "completion",
          "search_analyzer": "ik_smart" 
        },
        "type" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "viewCount" : {
          "type" : "long"
        }
      }
    }

}

GET com-doc7/_mapping



DELETE /suggest-com-doc

//复制索引数据
POST _reindex
{
  "source": {
  "index": "com-doc"
  },
  "dest": {
  "index": "com-doc7",
  "op_type": "create"
  }
}