
# hbase 单节点安装

### step1

* 下载hbase安装包，选择对应的版本，http://archive.apache.org/dist/hbase/

* 解压安装包，tar -zxvf hbase-xxx.tar.gz


### step2

* 修改conf文件夹下的hbase-env.sh, 配置JAVA_HOME

```
export JAVA_HOME=xxx
```

### step3

* 修改conf文件夹下的hbase-site.xml

```
<property>
  <name>hbase.rootdir</name>
  <value>file://xxx</value>
</property>

<property>
  <name>hbase.zookeeper.property.dataDir</name>
  <value>file://xxx</value>
</property>

<property>
  <name>hbase.cluster.distributed</name>
  <value>false</value>
</property>

```

### step4

* 启动服务, web ui http://localhost:60010

```
./bin/start_hbase.sh
```

