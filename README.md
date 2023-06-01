# backend
A django Backend to deal with multiple apis.

# requirment
```
pip install django
pip install django-rest-framework
pip install django-cors-headers
cnpm install axios
```
# User Module 用户模块
## POST  用户注册
- /api/user/register
## POST 用户登录
- /api/user/login

# Post Module 发帖模块
## GET 查询帖子
- /api/post
## POST 创建帖子
- /api/post
## PUT 更新帖子
- /api/post/{post_id}
## GET 显示某个帖子的具体信息
- /api/post/{post_id}
# Comment Module 评论模块
## GET 查看评论
- /api/comment
## POST创建评论
- /api/comment

# Schemas 数据库类
## User 用户类
- id
- username
- password
- is_manager
## Post 帖子类
- id
- title
- content_type
- text
- media_url
- location_x
- location_y
## Comment 评论类
- id
- content_type
- media_url
- text
