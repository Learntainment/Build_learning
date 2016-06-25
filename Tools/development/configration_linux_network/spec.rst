=====================
Spec Documentation
=====================

**Purpose**: It will configure your linux network automatically
=====================

**Run**: python 'net_init.py'_ ip_address
=====================
.. _net_init.py: ./net_init.py

**Parameter**: ip_address    需要设置网卡的ip
===================

**Detail**:
====================
通常情况下我会建立这样的一个环境：
>>>>>>>>>>>>>>>>>>>>
1. 通过vitual box 建立多台VM 比如：A B C
#. 众所周知，VBOX 建立的虚拟机需要设置第二块网卡为Host-only 并且指定好一个网段的ip地址才能与其他的机器通过SSH的方式通信，访问。
具体参见：'VBox虚拟机网络设置'_.

.. _VBox虚拟机网络设置: http://luokr.com/p/12

#. 所以此工具的设计分成几个部分来完成的
    - 获得未初始化的网卡信息。具体通过python的os.popen来向vm发shell命令。从而解析获得的字符串并匹配出需要的网卡的名字和信息。
    - 配置当前环境下的网络proxy,由于我的环境是需要用proxy才能上网的，所以我配置了当前用户下的.bashrc文件。
    - 配置host-only网卡信息，这一步的操作是在/etc/network/interfaces中完成的。
    - 配置ssh configuration file 设置好A B C 的host和hostname和user就可以完成在这三台机器之间随便的SSH访问了。

本文版权归个人所有，如需转载，请注明出处
========================
