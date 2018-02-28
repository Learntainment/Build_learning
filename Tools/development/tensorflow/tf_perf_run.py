#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


def inference_perf_test():
    
    cpu_info = os.popen('lscpu').read()
    cpu_info_list = cpu_info.split()
    cpu_info_flag = 0
    for per_cpu_info_list in cpu_info_list:
        if per_cpu_info_list.strip().find('22') == 0:
            cpu_type = "bdw"
            cpu_info_flag = 1
            break
        elif per_cpu_info_list.strip().find('28') == 0:
            cpu_type = "skl"
            cpu_info_flag = 1
            break
    if (cpu_info_flag == 1):
        batch_size_list = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        model_list = ["vgg16", "resnet50", "inception3"]
        for per_model_list in model_list:
            for per_batch_size_list in batch_size_list:
                cmd = 'python run_single_node_benchmark.py -nb 1000 -nw 1000 --forward_only true' + ' -c ' + cpu_type + ' -m ' + per_model_list + ' -b ' + str(per_batch_size_list)
                result = subprocess.check_output(cmd, shell=True)
                result_list = result.split("\n")
                for per_result_list in result_list:
                    if per_result_list.strip().find('total') == 0:
                        total_result = per_result_list
                        break
                perf_result = "cpu: " + cpu_type + " modle: " + per_model_list + " batch size: " + str(per_batch_size_list) + " result: " + total_result
                print "--------", perf_result
                with open('inference_perf_test.txt', 'a') as fp:
                    fp.write(perf_result)
                    fp.write("\n")
    else:
        print "Test CPU not match Please change it!"
        assert(0)

def training_perf_test():
    
    cpu_info = os.popen('lscpu').read()
    cpu_info_list = cpu_info.split()
    cpu_info_flag = 0
    for per_cpu_info_list in cpu_info_list:
        if per_cpu_info_list.strip().find('22') == 0:
            cpu_type = "bdw"
            cpu_info_flag = 1
            break
        elif per_cpu_info_list.strip().find('28') == 0:
            cpu_type = "skl"
            cpu_info_flag = 1
            break
    if (cpu_info_flag == 1):
        batch_size_list = [1, 2, 4, 8, 16, 32, 64, 128, 256]
        model_list = ["vgg16", "resnet50", "inception3"]
        for per_model_list in model_list:
            for per_batch_size_list in batch_size_list:
                cmd = 'python run_single_node_benchmark.py -nb 1000 -nw 1000' + ' -c ' + cpu_type + ' -m ' + per_model_list + ' -b ' + str(per_batch_size_list)
                result = subprocess.check_output(cmd, shell=True)
                result_list = result.split("\n")
                for per_result_list in result_list:
                    if per_result_list.strip().find('total') == 0:
                        total_result = per_result_list
                        break
                perf_result = "cpu: " + cpu_type + " modle: " + per_model_list + " batch size: " + str(per_batch_size_list) + " result: " + total_result
                print "--------", perf_result
                with open('train_perf_test.txt', 'a') as fp:
                    fp.write(perf_result)
                    fp.write("\n")
    else:
        print "Test CPU not match Please change it!"
        assert(0)

if __name__ == "__main__":
    print "Start TF Performance Test"
    training_perf_test()
    inference_perf_test()
