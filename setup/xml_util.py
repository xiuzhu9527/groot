#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
from xml.dom.minidom import parse


class XmlParse():
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.dom_tree = parse(self.xml_file)
        self.root_node = self.dom_tree.documentElement

    def create_node(self, key, value=''):
        key_et = self.dom_tree.createElement(key)
        if value:
            value_tt = self.dom_tree.createTextNode(value)
            key_et.appendChild(value_tt)
        return key_et

    def create_prop_node(self, name, value):
        prop_node = self.dom_tree.createElement('property')
        name_node = self.dom_tree.createElement('name')
        name_value = self.dom_tree.createTextNode(name)
        name_node.appendChild(name_value)
        value_node = self.dom_tree.createElement('value')
        value_value = self.dom_tree.createTextNode(value)
        value_node.appendChild(value_value)
        prop_node.appendChild(name_node)
        prop_node.appendChild(value_node)
        self.root_node.appendChild(prop_node)

    def chain_node(self, parent_node, child_node):
        parent_node.appendChild(child_node)

    def write_out(self, dist=''):
        f = open(self.xml_file, 'w')
        if dist:
            f = open(dist, 'w')
        self.dom_tree.writexml(f, addindent='  ', newl='\n', encoding='utf-8')


def test():
    xp = XmlParse('/opt/hbase-2.2.4/conf/hbase-site.xml')
    property = xp.create_node('property')
    value_node = xp.create_node('value', 'tom')
    xp.chain_node(property, value_node)
    xp.chain_node(xp.root_node, property)
    xp.write_out()

if __name__ == '__main__':
    test()

