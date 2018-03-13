#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time

if __name__ == "__main__":
    print "start TF COSIM test"
    eigen_dir = sys.argv[1]
    mkldnn_dir = sys.argv[2]
    eigen_dir_layer = sys.argv[3]
    cmd_flag = 1
    #cmd = 'python general_cosim.py -e ../../data/resnet/dummy/data_dump_eigen_step11/ -m ../../data/resnet/dummy/data_dump_mkldnn_step11/ -l ../../data/resnet/dummy/data_dump_eigen_step11/layers.txt'
    while (cmd_flag):
        cmd = 'python general_cosim.py -e ' + eigen_dir + ' -m ' + mkldnn_dir + ' -l ' + eigen_dir_layer + ' 1>>result.out 2>>result.err'
        cmd_flag = subprocess.call(cmd, shell=True)
        #print "cmd_flag:   ", cmd_flag
        if (cmd_flag == 1):
            with open("result.err") as fp:
                line_list = fp.readline()
                while line_list:
                    per_line_list = line_list.split()
                    for single_per_line_list in per_line_list:
                        if (single_per_line_list == "node"):
                            #print "single_per_line_list ------", per_line_list[5]
                            slash_line_list = per_line_list[5].split('/')
                            for single_slash_line_list in slash_line_list:
                                if (single_slash_line_list == "Direction_Session"):
                                    ban_layer = per_line_list[5]
                                    break
                    line_list = fp.readline()
                #print "ban_layer--------", ban_layer
            ban_layer_list = ban_layer.split('/')
            reorganization_ban_layer_line = ''
            for single_ban_layer_list in ban_layer_list:
                if (single_ban_layer_list == "v"):
                    reorganization_ban_layer_line = 'Direction_Session/' + single_ban_layer_list
                    continue
                reorganization_ban_layer_line = reorganization_ban_layer_line + '#' + single_ban_layer_list
            reorganization_ban_layer_line = reorganization_ban_layer_line + '.dat\n'
            print "reorganization_ban_layer_line-----", reorganization_ban_layer_line

            #with open(eigen_dir_layer) as fs:
            with open('test_layers.txt') as fs:
                layer_line_list = fs.readlines()
                layer_num = 0
                for each in layer_line_list:
                    #print "reorganization_ban_layer_line-----", reorganization_ban_layer_line
                    if (each == reorganization_ban_layer_line):
                        layer_line_list[layer_num] = '#' + reorganization_ban_layer_line
                        print "ban_layer ----", layer_line_list[layer_num]
                        with open('new_layers.txt', 'w') as ft:
                            ft.writelines(layer_line_list)
                        break
                    layer_num = layer_num + 1
            with open('result.err', 'r') as f1:
                with open('result.txt', 'a') as f2:
                    f2.write('\n')
                    f2.write(f1.read())
            rm_cmd = subprocess.call("rm result.err result.out", shell=True)
            cp_cmd = subprocess.call("cp new_layers.txt test_layers.txt", shell=True)
        else:
            cmd_flag = 0
        #result = subprocess.check_output(cmd, shell=True)
        #result_list = result.split("\n")
        #for per_result_list in result_list:
        #    if per_result_list.strip().find('Traceback') == 0:
        #        print "TEST RESULT-------------------", per_result_list
        #        break




