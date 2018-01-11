#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import json

def get_tensorflow():

    '''err_code = subprocess.call("rm -rf tensorflow; git clone https://github.com/tensorflow/tensorflow.git", shell=True)
    if (err_code != 0):
        return err_code
    err_code = subprocess.call("cd tensorflow/; git checkout -B unittest", shell=True)
    if (err_code != 0):
        return err_code'''
    return 0

def build_mkl_mode():

    err_clean_code = subprocess.call("cd tensorflow/; bazel clean", shell=True)
    if (err_clean_code != 0):
        return err_clean_code
    err_cfg_code = subprocess.call("cd tensorflow/; echo '\n\nn\nn\nn\nn\nn\nn\nn\nn\nn\nn\n\nn\n' | ./configure", shell=True)
    if (err_cfg_code != 0):
        return err_cfg_code
    err_mkl_code = subprocess.call("cd tensorflow/; bazel build --copt=-DINTEL_MKL_DNN --copt -O3 --config=mkl -c opt --host_copt=-DINTEL_MKL_DNN ./tensorflow/tools/pip_package:build_pip_package", shell=True)
    if (err_mkl_code != 0):
        return err_mkl_code
    subprocess.call("mkdir -p ~/tmp/; rm -rf ~/tmp/*.whl", shell=True)
    err_pag_code = subprocess.call("cd tensorflow/; ./bazel-bin/tensorflow/tools/pip_package/build_pip_package ~/tmp/", shell=True)
    if (err_pag_code != 0):
        return err_pip_code
    whl_name = os.popen('ls ~/tmp/').read()
    list_file = whl_name.split('\n')
    for list_per_file in list_file:
        if (list_per_file.strip().find('tensorflow-') == 0):
            whl_file = list_per_file
    whl_list = ['~/tmp/', whl_file]
    whl_list_name = ''
    err_pip_code = subprocess.call(["pip", "install", whl_list_name.join(whl_list)])
    if (err_pip_code != 0):
        return err_pip_code
    return 0

def build_eigen_mode():

    err_clean_code = subprocess.call("cd tensorflow/; bazel clean", shell=True)
    if (err_clean_code != 0):
        return err_clean_code
    err_cfg_code = subprocess.call("cd tensorflow/; echo '\n\nn\nn\nn\nn\nn\nn\nn\nn\nn\nn\n\nn\n' | ./configure", shell=True)
    if (err_cfg_code != 0):
        return err_cfg_code
    err_eigen_code = subprocess.call("cd tensorflow/; bazel build --copt -DEIGEN_USE_VML --copt -O3 -s -c opt //tensorflow/tools/pip_package:build_pip_package", shell=True)
    if (err_eigen_code != 0):
        return err_eigen_code
    subprocess.call("mkdir -p ~/tmp/; rm -rf ~/tmp/*.whl", shell=True)
    err_pag_code = subprocess.call("cd tensorflow/; ./bazel-bin/tensorflow/tools/pip_package/build_pip_package ~/tmp/", shell=True)
    if (err_pag_code != 0):
        return err_pip_code
    whl_name = os.popen('ls ~/tmp/').read()
    list_file = whl_name.split('\n')
    for list_per_file in list_file:
        if (list_per_file.strip().find('tensorflow-') == 0):
            whl_file = list_per_file
    whl_list = ['~/tmp/', whl_file]
    whl_list_name = ''
    err_pip_code = subprocess.call(["pip", "install", whl_list_name.join(whl_list)])
    if (err_pip_code != 0):
        return err_pip_code
    return 0

if __name__ == "__main__":

    print ("start test build")
    build_mode = sys.argv[1]
    if (build_mode == "mkldnn"):
        resource_check = get_tensorflow()
        if (resource_check == 0):
            mkl_check = build_mkl_mode()
            if (mkl_check == 0):
                mkl_result = [{"sub_case_name": "<tensorflow_build.py>",
                               "result": "<PASSED>",
                               "case_name": "<build_mkl_mode>"}]
                mkl_json_result = json.dumps(mkl_result)
                print ("Test completed.")
                print ("Test Result:")
                print ("{")
                print ("  \"sub_cases\":"),mkl_json_result
                print ("}")
            else:
                mkl_result = [{"sub_case_name": "<tensorflow_build.py>",
                               "result": "<FAILED>",
                               "case_name": "<build_mkl_mode>"}]
                mkl_json_result = json.dumps(mkl_result)
                print ("Test completed.")
                print ("Test Result:")
                print ("{")
                print ("  \"sub_cases\":"),mkl_json_result
                print ("}")
        else:
            resource_result = [{"sub_case_name": "<tensorflow_build.py>",
                               "result": "<FAILED>",
                               "case_name": "<get_tensorflow>"}]
            resource_json_result = json.dumps(resource_result)
            print ("Test completed.")
            print ("Test Result:")
            print ("{")
            print ("   \"sub_cases\":"),resource_json_result
            print ("}")
    elif (build_mode== "eigen"):
        resource_check = get_tensorflow()
        if (resource_check == 0):
            eigen_check = build_eigen_mode()
            if (eigen_check == 0):
                eigen_result = [{"sub_case_name": "<tensorflow_build.py>",
                               "result": "<PASSED>",
                               "case_name": "<build_eigen_mode>"}]
                eigen_json_result = json.dumps(eigen_result)
                print ("Test completed.")
                print ("Test Result:")
                print ("{")
                print ("  \"sub_cases\":"),eigen_json_result
                print ("}")
            else:
                eigen_result = [{"sub_case_name": "<tensorflow_build.py>",
                               "result": "<FAILED>",
                               "case_name": "<build_eigen_mode>"}]
                eigen_json_result = json.dumps(eigen_result)
                print ("Test completed.")
                print ("Test Result:")
                print ("{")
                print ("  \"sub_cases\":"),eigen_json_result
                print ("}")
        else:
            resource_result = [{"sub_case_name": "<tensorflow_build.py>",
                               "result": "<FAILED>",
                               "case_name": "<get_tensorflow>"}]
            resource_json_result = json.dumps(resource_result)
            print ("Test completed.")
            print ("Test Result:")
            print ("{")
            print ("   \"sub_cases\":"),resource_json_result
            print ("}")









