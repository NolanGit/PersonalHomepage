## 使用Vue.js+Flask实现的个人主页
国内搜索引擎的信息流着实用不到，个人想关注的信息又过于分散，因此决定自己写一个主页，整合自己所需要的功能。
采用前后端分离的架构，前端使用Vue.js、Element UI，后端使用Flask提供接口、Sqlite作为数据库、Peewee作为ORM。
### Done：
- 多用户登录
- 搜索引擎
- 天气
- 书签
- 后台管理页面（定时任务脚本统一驱动和管理）
### Working on:
- 股票
- 基金
- AppStore价格监控
### To Do
- 黄金
- 新闻
- 便签
- 智能家居？
- 常用ip绑定
### 实例（更新于2020-1-9）
#### 主页
![image](https://user-images.githubusercontent.com/27627484/71998100-fae58980-3279-11ea-806e-8a1a9c09df51.png)
#### 搜索：使用百度的自动补全功能，增加引擎的话是在数据库中增加数据(search_engines)
- 自动提示和切换搜索引擎
![image](https://user-images.githubusercontent.com/27627484/71998812-3f255980-327b-11ea-9e6d-7ad97cd5c18d.png)
#### 天气：登录后可以进行自定义，如不登录则展示IP所在地的天气信息
- 增加城市
![image](https://user-images.githubusercontent.com/27627484/71998875-53695680-327b-11ea-99ce-28e75fd20675.png)
#### 书签：登陆后可以自定义，不登录时展示的书签是在数据库中修改（bookmarks.user_id==0）
- 修改展示顺序
![image](https://user-images.githubusercontent.com/27627484/71998914-6c720780-327b-11ea-84a1-d4c5efeceaee.png)
- 修改书签详情
![image](https://user-images.githubusercontent.com/27627484/71998951-7ac02380-327b-11ea-8249-d48f6aa21adb.png)
- 修改书签图标
![image](https://user-images.githubusercontent.com/27627484/71999000-90354d80-327b-11ea-8fe1-15c9901eb24d.png)
#### 控制台：用于后台定时程序的同一驱动，需要配置\backend\app\console\console_script_schedule_monitor.py为定时运行，步长需小于一小时
##### 控制台主页：如需增加模块，需要配置数据库（console）
![image](https://user-images.githubusercontent.com/27627484/71999094-c4a90980-327b-11ea-97ae-7e683663aa50.png)
##### 脚本运行平台：可以通过配置生成前端页面表单，然后通过填写表单来提交脚本至后端运行并展示运行结果，可以定时运行、参数回放、记录运行时间、记录运行日志、通过配置生成运行结果表格、运行额外脚本动态参数化前端组件
- 首页：左侧为脚本所属系统页
![image](https://user-images.githubusercontent.com/27627484/72076975-6dfe0700-3331-11ea-9253-717766654a2d.png)
- 首页：右侧为具体脚本，通过右上角的"+"可以增加脚本，增加脚本会增加tab
![image](https://user-images.githubusercontent.com/27627484/72077181-ca612680-3331-11ea-9a88-37c6ead5e6f9.png)
- 编辑脚本：

  - 脚本名称：展示在tab上
  - 起始文件夹：配置在此处的文件夹会使用cd命令打开
  
![image](https://user-images.githubusercontent.com/27627484/72078174-95ee6a00-3333-11ea-9d24-be5e4ff41309.png)
![image](https://user-images.githubusercontent.com/27627484/72077217-d947d900-3331-11ea-97ce-6a7cbda6e09d.png)
![image](https://user-images.githubusercontent.com/27627484/72077227-df3dba00-3331-11ea-9e03-b82439f5cda8.png)
