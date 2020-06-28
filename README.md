# 使用Vue.js+Flask实现的个人主页
国内搜索引擎的信息流着实用不到，个人想关注的信息又过于分散，因此决定自己写一个主页，整合自己所需要的功能。
采用前后端分离的架构，前端使用Vue.js、Element UI，后端使用Flask提供接口、MariaDB作为数据库、Peewee作为ORM。
### Done：
- 多用户登录
- 搜索引擎
- 天气
- 书签
- 脚本管理（异步任务脚本统一驱动和管理）
- 权限控制（包括用户新建修改、角色新建修改、权限新建修改、用户角色权限三者对应关系）
- AppStore价格监控
### Working on:
- 黄金价格
### To Do
- 股票
- 基金
- 新闻
- 便签
## 部署

  使用python3运行根目录下的start.py并根据提示进行操作
  
## 目录结构

  后端代码位于/backend，后端入口文件位于/backend/run.py，前端代码位于/frontend，前端编译的产物位于/dist
  
  同时需要本地安装MySQL（测试时使用的是MariaDB）和Redis

## 介绍（更新于2020-1-9）
### 主页：
![image](https://user-images.githubusercontent.com/27627484/71998100-fae58980-3279-11ea-806e-8a1a9c09df51.png)
### 搜索：使用百度的自动补全接口，增加引擎的话是在数据库中增加数据(search_engines)
- 自动提示和切换搜索引擎
![image](https://user-images.githubusercontent.com/27627484/71998812-3f255980-327b-11ea-9e6d-7ad97cd5c18d.png)
### 天气：登录后可以进行自定义，如不登录则展示IP所在地的天气信息
- 增加城市
![image](https://user-images.githubusercontent.com/27627484/71998875-53695680-327b-11ea-99ce-28e75fd20675.png)
### 书签：登陆后可以自定义，不登录时展示的书签是在数据库中修改（bookmarks.user_id==0）
- 拖动修改展示顺序
![image](https://user-images.githubusercontent.com/27627484/71998914-6c720780-327b-11ea-84a1-d4c5efeceaee.png)
- 修改书签详情
![image](https://user-images.githubusercontent.com/27627484/71998951-7ac02380-327b-11ea-8249-d48f6aa21adb.png)
- 修改书签图标
![image](https://user-images.githubusercontent.com/27627484/71999000-90354d80-327b-11ea-8fe1-15c9901eb24d.png)
### 控制台：如需增加模块，需要配置数据库（console）
![image](https://user-images.githubusercontent.com/27627484/71999094-c4a90980-327b-11ea-97ae-7e683663aa50.png)
### 脚本运行平台：可以通过配置生成前端页面表单，然后通过填写表单来提交脚本至后端运行并展示运行结果，可以定时运行、参数回放、记录运行时间、记录运行日志、通过配置生成运行结果表格、运行额外脚本动态参数化前端组件，用于后台程序的统一驱动，定时任务需要配置\backend\app\script\schedule_monitor.sh为定时运行，步长需小于一小时
- 首页：左侧为脚本所属系统页，右侧为具体脚本，通过右上角的"+"可以增加脚本，增加脚本会增加tab
![image](https://user-images.githubusercontent.com/27627484/72076975-6dfe0700-3331-11ea-9253-717766654a2d.png)
- 按钮区域：
  依次为：回放我上一次运行的参数（回填到表单中）、展示我上一次运行的日志、展示最近50条运行记录、配置定时运行、编辑脚本和删除按钮（此系统中所有删除和更新操作都为逻辑删除）
![image](https://user-images.githubusercontent.com/27627484/72077181-ca612680-3331-11ea-9a88-37c6ead5e6f9.png)
- 编辑脚本：

  初始选项：
  - 脚本名称：展示在tab上
  - 起始文件夹：配置在此处的文件夹会使用cd命令打开
  - 起始脚本：配置在此处的脚本会作为初始命令
  - 组合方式：提供两种组合方式-顺序和替换，顺序将起始脚本和参数顺序组合提交，替换则类似Jenkins的处理方式
  
   组件选项：
  - 组件名称：前端展示的label
  - 组件类型：提供四种类型-输入框、选择器、日期选择器和日期范围选择器，根据用户配置展示为相应的组件
  - 默认值：组件默认值
  - 是否只读：前端是否只读
  - 占位文字：前端展示的placeHolder
  - 备注：备注将以组件后一个icon的方式展现，鼠标悬浮即可展示
  - 是否有额外按钮：配置为是时，组件后方会展示一个按钮，运行按钮可以运行小型脚本，适用于动态提醒用户参数，如下方图片所示。有两种数据的展示模式，一种是脚本内直接使用`print()`来打印需要输出的文字；此外，通过一定的数据格式，可以选择器组件的选项进行初始化，见下方实例：
  ```python
  import json
  d = {
      'code': 200,                                # 状态码，非必填，无实际作用
      'data': {
          'msg': 'hello\nworld qwe\nqewqweewqwe', # 展示的文本，非必须，会被解析为html，使用"\n"换行
          'value': '123',                         # 非必须，当传递value时，会将组件内的值替换成传回的值
          'options': [                            # 非必须，当传递options时，会将选择器组件内的选项替换成传回的选项
              {
                  'label': '234',                 # 标签，用于展示
                  'value': '234'                  # 值，用于实际传递
              },
          ]
      }
  }
  print(json.dumps(d))
  ```
  - 是否在列表展示：配置为是时，在运行列表中会以单独一列的方式呈现运行时提交的参数
  - 是否显示：配置为否时前端不展示
  
  ![image](https://user-images.githubusercontent.com/27627484/72078174-95ee6a00-3333-11ea-9d24-be5e4ff41309.png)
  ![image](https://user-images.githubusercontent.com/27627484/72077217-d947d900-3331-11ea-97ce-6a7cbda6e09d.png)
- 运行列表：默认展示运行人、操作、运行开始时间、耗时、运行ID五列，其中操作列包含三个按钮：参数、日志和回放，参数按钮悬浮可以展示参数，日志按钮点击可以展示日志、回放按钮点击可以将所选运行记录的参数回填至当前表单上。运行列表可以通过配置组件的"是否在列表展示"选项来自定义列，但不建议设置过多。
![image](https://user-images.githubusercontent.com/27627484/72077227-df3dba00-3331-11ea-9e03-b82439f5cda8.png)
- 定时任务：最小颗粒度为一小时，实际上更小也可以，但是没有试过，如果调小颗粒度，则需要减小定时任务扫库脚本的运行步长。定时任务驱动的脚本，在列表中会在运行人后方加上"(定时)"字样
![image](https://user-images.githubusercontent.com/27627484/72083322-90e1e880-333c-11ea-9995-774f0faeae73.png)

