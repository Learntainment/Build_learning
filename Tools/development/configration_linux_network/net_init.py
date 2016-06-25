#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys


if __name__ == "__main__":

    print ("Get uninitialized network name")

    ip_address = sys.argv[1]
    string = os.popen('ifconfig -a').read()
    list_str = string.split('\n')
    list_number = 0
    flag = 0
    for list_pre_str in list_str:
        list_number = list_number + 1
        if list_pre_str.strip().find('BROADCAST') == 0:
            string_list = list_str[list_number - 2].split()
            network_name = string_list[0]
            flag = 1
            break
    if flag == 1:
        flag = 0
    else:
        raise Exception("Invalid flag! Not find valid network adapter ", flag)

    print ("Configure proxy setting for system")

    bashrc_file = open('/home/e/.bashrc', 'a+')
    bashrc_proxy_list = ["export http_proxy=http://child-prc.intel.com:913",\
                        "\nexport https_proxy=http://child-prc.intel.com:913"]
    bashrc_file.writelines(bashrc_proxy_list)
    bashrc_file.close()
    os.system('chown e:e /home/e/.bashrc')

    print ("Fill in network interfaces for system")

    network_file = open('/etc/network/interfaces', 'a+')
    network_file.write('# the host only network adapter network interface')
    network_file.write('\nauto ')
    network_file.write(network_name)
    network_file.write('\niface ')
    network_file.write(network_name)
    network_list1 = [' inet', ' static', '\naddress ']
    network_file.writelines(network_list1)
    network_file.write(ip_address)
    network_list2 = ['\nnetmask', ' 255.255.255.0']
    network_file.writelines(network_list2)
    network_file.close()
    os.system('/etc/init.d/networking restart')
    network_str = os.popen('ifconfig').read()
    network_info_list = network_str.split('\n')
    for network_pre_str in network_info_list:
        if network_pre_str.strip().find(network_name) == 0:
            flag = 1
            break
    if flag == 1:
        flag = 0
    else:
        raise Exception("Invalid flag! Failed network adapter restart ", flag)

    print ("Configure ssh server setting")

    ssh_config = open('/home/e/.ssh/config', 'w')
    ssh_config_list = ["host a", "\nhostname a", "\nuser huia",\
                      "\nhost b", "\nhostname b", "\nuser huib",\
                      "\nhost c", "\nhostname c", "\nuser huic",\
                      "\nhost d", "\nhostname d", "\nuser d",\
                      "\nhost x", "\nhostname x", "\nuser x",\
                      "\nhost e", "\nhostname e", "\nuser e"]
    ssh_config.writelines(ssh_config_list)
    ssh_config.close()
    os.system('chown e:e /home/e/.ssh/config')
    os.system('chmod g+w /home/e/.ssh/config')

    print ("Configure ssh host name setting")

    host_name = open('/etc/hosts', 'a+')
    host_name_list = ["10.239.158.22 x", "\n192.168.56.101 a",\
                     "\n192.168.56.102 b", "\n192.168.56.103 c",\
                     "\n192.168.56.104 d", "\n192.168.56.105 e"]
    host_name.writelines(host_name_list)
    host_name.close()

    print ("Finish the all configuration")
