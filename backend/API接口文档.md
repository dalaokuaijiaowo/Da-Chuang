# API接口文档

## 1. 分析评论接口

### 接口地址

`/api/analyze`

### 请求方法

`POST`

### 请求参数

- **file**: 文件（CSV格式），包含评论数据

### 响应数据

```json
{
  "success": true,
  "results": [
    {
      "序号": 1,
      "用户名": "用户名1",
      "评论内容": "评论内容1",
      "ai_prob": 0.95,
      "human_prob": 0.05,
      "conclusion": "AI生成"
    },
    // 更多评论...
  ],
  "stats": {
    "total": 100,
    "ai_count": 30,
    "human_count": 70,
    "ai_ratio": 30.0
  }
}
```

## 2. 爬取B站视频评论接口

### 接口地址

`/api/crawl/video`

### 请求方法

`POST`

### 请求参数

```json
{
  "bv": "BV1GYAwzJEza",
  "is_second": true
}
```

### 响应数据

```json
{
  "success": true,
  "message": "视频评论爬取完成",
  "output": "爬取过程的输出信息"
}
```

## 3. 爬取B站动态评论接口

### 接口地址

`/api/crawl/dynamic`

### 请求方法

`POST`

### 请求参数

```json
{
  "opus": "123456789",
  "is_second": true
}
```

### 响应数据

```json
{
  "success": true,
  "message": "动态评论爬取完成",
  "output": "爬取过程的输出信息"
}
```

## 4. 爬取知乎回答评论接口

### 接口地址

`/api/crawl/zhihu`

### 请求方法

`POST`

### 请求参数

```json
{
  "answer_id": "2018449337789719535",
  "max_count": 500
}
```

### 响应数据

```json
{
  "success": true,
  "message": "知乎评论爬取完成",
  "output": "爬取过程的输出信息"
}
```

## 5. 爬取网易云音乐评论接口

### 接口地址

`/api/crawl/netease`

### 请求方法

`POST`

### 请求参数

```json
{
  "song_id": 2122308127
}
```

### 响应数据

```json
{
  "success": true,
  "message": "网易云音乐评论爬取完成",
  "output": "爬取过程的输出信息"
}
```

## 6. 爬取豆瓣月度热书接口

### 接口地址

`/api/crawl/douban`

### 请求方法

`POST`

### 请求参数

```json
{
  "max_books": 5
}
```

- **max_books**：可选，指定爬取的书籍数量

### 响应数据

```json
{
  "success": true,
  "message": "豆瓣月度热书爬取完成",
  "output": "爬取过程的输出信息"
}
```

## 7. 获取已爬取文件列表接口

### 接口地址

`/api/files`

### 请求方法

`GET`

### 响应数据

```json
{
  "files": [
    "BV1GYAwzJEza_评论.csv",
    "zhihu_comments_2018449337789719535.csv",
    // 更多文件...
  ]
}
```

## 8. 获取文件内容接口

### 接口地址

`/api/files/content/<filename>`

### 请求方法

`GET`

### 响应数据

```json
{
  "success": true,
  "filename": "BV1GYAwzJEza_评论.csv",
  "data": [
    {
      "序号": 1,
      "用户名": "用户名1",
      "评论内容": "评论内容1"
    },
    // 更多评论...
  ]
}
```

### 错误响应

```json
{
  "error": "文件不存在"
}
```

```json
{
  "error": "文件格式不兼容"
}
```

## 9. 下载文件接口

### 接口地址

`/api/files/download/<filename>`

### 请求方法

`GET`

### 响应

文件下载

## 10. 健康检查接口

### 接口地址

`/api/health`

### 请求方法

`GET`

### 响应数据

```json
{
  "status": "ok",
  "message": "服务正常运行"
}
```
