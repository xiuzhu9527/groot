
# zookeeper 单节点安装

### step1

* 下载zookeeper安装包，选择对应的版本，http://archive.apache.org/dist/zookeeper/

* 解压安装包，tar -zxvf zookeeper-xxx.tar.gz


### step2

* 拷贝conf文件夹下的zoo_sample.cfg 为zoo.cfg

* 设置zookeeper数据存取路径dataDir
```
dataDir=xxx
```

* 设置zookeeper日志文件夹dataLogDir
```
dataLogDir=xxx
```

* 设置server.1=localhost:2888:3888

### step3

* 在dataDir文件夹下添加myid文件，并写入1

### step4

* 启动服务

```
./bin/zkServer.sh start
```

