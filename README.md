# spider-man

蜘蛛侠-数据采集服务

## 项目结构
* core：项目核心代码
* configs：项目基础配置。包括本地环境、开发环境和生产环境的 MongoDB 数据库配置、日志配置
* local_logs：本地调试时的日志输出默认目录。包括 INFO 和 ERROR 级别的日志类型
* tests：单元测试所在目录。包括测试代码文件 (如：global_spider_test.py) 和测试输出结果文件 (GlobalSpiderTest.test_parse.json)
* flake8：python 代码静态检查配置文件。在此可以配置代码静态检查的规则。
* application.py：项目启动执行入口
* Pipfile 和 Pipfile.lock：pipenv 虚拟环境条件下依赖包的管理
* scrapy.cfg：python 爬虫框架 scrapy 的默认配置
    * scrapy 官方文档：https://doc.scrapy.org/en/latest/topics/settings.html

## pipenv
### pipenv 是 Python 项目的依赖管理器
### 安装依赖：pipenv install module_name
### 项目本地启动：pipenv run python application.py
### 本地启动单元测试：pipenv run py.test

   	
