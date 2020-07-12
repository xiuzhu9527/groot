#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import json
import urllib
import urllib2
import gzip
import tarfile
import shutil

import config
import log
import xml_util

reload(sys)
sys.setdefaultencoding('utf-8')


cm = config.ConfigManager('groot_conf.ini')
logger = log.Logger()

def download(url, dist):
    target_file = dist + os.sep + url.split(os.sep)[-1]
    logger.info('download package from %s to %s', url, target_file)
    data = urllib2.urlopen(url).read()
    open(target_file, 'wb').write(data)
    return target_file

def unzip(gz_file_path, unzip_file_path):
    gz_file = gzip.open(gz_file_path, 'rb')
    unzip_file = open(unzip_file_path, 'wb')
    unzip_file.write(gz_file.read())
    os.remove(gz_file_path)
    gz_file.close()
    unzip_file.close()

def untar(tar_file_path, untar_dir_path):
    tar = tarfile.open(tar_file_path)
    tar.extractall(path=untar_dir_path)
    tar_file_home = tar.getnames()[0].split('/')[0]
    untar_path = untar_dir_path + os.sep + tar_file_home
    os.remove(tar_file_path)
    return untar_path

def zookeeper(software_path):
    logger.info('install zookeeper start!')
    version = cm.get('zookeeper', 'version')
    logger.info('zookeeper version is %s', version)

    # download zookeeper package
    zk_url = 'http://archive.apache.org/dist/zookeeper/zookeeper-%s/apache-zookeeper-%s-bin.tar.gz' % (version, version)
    target_file = download(zk_url, software_path)
    logger.info('unzip zookeeper package')
    zk_home = '%s/zookeeper-%s' % (software_path, version)
    if os.path.exists(zk_home):
        shutil.rmtree(zk_home)
    unzip_path = untar(target_file, software_path)
    os.rename(unzip_path, zk_home)
    logger.info(zk_home)

    # create data dir and logs
    data_path = '%s/data' % zk_home
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    logs_path = '%s/logs' % zk_home
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    # set zoo.cfg
    zoo_cfg = '%s/conf/zoo.cfg' % zk_home
    zoo_sample_cfg = '%s/conf/zoo_sample.cfg' % zk_home
    os.rename(zoo_sample_cfg, zoo_cfg)
    open(zoo_cfg, 'a').write('dataDir=%s\n' % data_path)
    open(zoo_cfg, 'a').write('dataLogDir=%s\n' % logs_path)
    open(zoo_cfg, 'a').write('server.1=localhost:2888:3888\n')

    # set myid
    myid_file = '%s/myid' % data_path
    open(myid_file, 'w').write('1')

    # start zookeeper
    start_server = cm.get('zookeeper', 'start_server')
    if start_server == 'true':
        start_cmd = 'cd %s/bin && ./zkServer.sh start' % zk_home
        logger.info('start_cmd: %s', start_cmd)
        res = os.system(start_cmd)
        logger.info('server start: %s', res)
    logger.info('install zookeeper finish!')

def hbase(software_path):
    logger.info('install hbase start!')
    version = cm.get('hbase', 'version')
    logger.info('hbase version is %s', version)

    # download hbase package
    hbase_url = 'http://archive.apache.org/dist/hbase/%s/hbase-%s-bin.tar.gz' % (version, version)
    target_file = download(hbase_url, software_path)
    hbase_home = '%s/hbase-%s' % (software_path, version)
    if os.path.exists(hbase_home):
        shutil.rmtree(hbase_home)
    logger.info('unzip hbase package')
    unzip_path = untar(target_file, software_path)
    os.rename(unzip_path, hbase_home)
    logger.info(hbase_home)

    # create data dir
    hbase_data_path = 'file://%s/data/hbase' % hbase_home
    if not os.path.exists(hbase_data_path):
        os.makedirs(hbase_data_path)
    zk_data_path = 'file://%s/data/zookeeper' % hbase_home
    if not os.path.exists(zk_data_path):
        os.makedirs(zk_data_path)
    
    # set java home
    logger.info('set hbase-env.sh')
    hbase_env_file = '%s/conf/hbase-env.sh' % hbase_home
    ex_java_home = 'export JAVA_HOME=%s' % os.getenv('JAVA_HOME')
    open(hbase_env_file, 'a').write(ex_java_home + '\n')
    open(hbase_env_file, 'a').write('export HBASE_MANAGES_ZK=false' + '\n')

    # set hbase-site.xml
    logger.info('set hbase-site.xml')
    hbase_site = '%s/conf/hbase-site.xml' % hbase_home
    xp = xml_util.XmlParse(hbase_site)
    xp.create_prop_node('hbase.rootdir', hbase_data_path)
    xp.create_prop_node('hbase.zookeeper.quorum', 'localhost:2181')
    xp.create_prop_node('hbase.cluster.distributed', 'true')
    xp.write_out()

    start_server = cm.get('hbase', 'start_server')
    if start_server == 'true':
        start_cmd = 'cd %s/bin && ./start-hbase.sh' % hbase_home
        logger.info('start_cmd: %s', start_cmd)
        res = os.system(start_cmd)
        logger.info('hbase server start: %s', res)

    logger.info('install hbase finish!')
    

def install():
    groot_home = os.path.dirname(os.getcwd())
    logger.info('groot home: %s', groot_home)
    rw = os.access(groot_home, os.W_OK)
    if not rw:
        logger.error('groot home[%s] 没有读写权限！', groot_home)
        sys.exit(-1)

    software_path = '%s/software' % groot_home
    if not os.path.exists(software_path):
        os.mkdir(software_path)

    for section in cm.sections():
        on_off = cm.get(section, 'on-off')
        if on_off != 'true':
            continue
        method = "%s('%s')" % (section, software_path)
        eval(method)

def main():
    logger.info('start setup!')
    install()

if __name__ == '__main__':
    main()

