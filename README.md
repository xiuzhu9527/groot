
# groot

大数据开发一键部署本地开发环境, 基于python 2开发，不兼容window部署。本着以学习为目的，希望能与众多优秀开发者多多交流。

### 支持部署组件

* [hbase](doc/hbase.md)


### quick start

* 下载项目
```
git clone https://github.com/xiuzhu9527/groot.git
```

* 切换到项目的setup目录下，执行安装命令

```
python groor.py
```

### groot_conf.ini配置项解释

* \[xxx\]: 组件名

* version: 组件版本

* start_server: 安装完后是否启动组件

* on-off: 是否安装该组件 

示例：
```
[hbase]
version=2.2.4
start_server=true
on-off=true
```

