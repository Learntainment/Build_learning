# -*- coding: utf-8 -*-

import os
import sys
import subprocess


def run_mkl_mode():
    module = sys.argv[2]
    if (module == "inception3"):
        dataset = sys.argv[3]
        if (dataset == "dummy"):
            step = sys.argv[4]
            if (step == "1"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m inception3 -c skl -o 112 -b 128 --num_batches 1 --dump_after_steps -1", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/dummy/data_dump_mkldnn_step1", shell=True)
                subprocess.call("mv data_dump_mkldnn /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/dummy/data_dump_mkldnn_step1", shell=True)

            elif (step == "11"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m inception3 -c skl -o 112 -b 128 --num_batches 11 --dump_after_steps 10", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/dummy/data_dump_mkldnn_step11", shell=True)
                subprocess.call("mv data_dump_mkldnn /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/dummy/data_dump_mkldnn_step11", shell=True)
        elif (dataset == "mini"):
            step = sys.argv[4]
            if (step == "1"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m inception3 -c skl -o 112 -b 128 --data_dir=/mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/dl_framework-intel_tensorflow_models/tf_mini_imagenet_data --data_name=imagenet --num_batches=1 --dump_after_steps=-1", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/mini/data_dump_mkldnn_step1", shell=True)
                subprocess.call("mv data_dump_mkldnn /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/mini/data_dump_mkldnn_step1", shell=True)

            elif (step == "11"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m inception3 -c skl -o 112 -b 128 --data_dir=/mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/dl_framework-intel_tensorflow_models/tf_mini_imagenet_data --data_name=imagenet --num_batches=11 --dump_after_steps=10", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/mini/data_dump_mkldnn_step11", shell=True)
                subprocess.call("mv data_dump_mkldnn /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/mini/data_dump_mkldnn_step11", shell=True)
    elif (module == "resnet50"):
        dataset = sys.argv[3]
        if (dataset == "dummy"):
            step = sys.argv[4]
            if (step == "1"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m resnet50 -c skl -o 112 -b 128 --num_batches 1 --dump_after_steps -1", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/dummy/data_dump_mkldnn_step1", shell=True)
                subprocess.call("mv data_dump_mkldnn /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/dummy/data_dump_mkldnn_step1", shell=True)

            elif (step == "11"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m resnet50 -c skl -o 112 -b 128 --num_batches 11 --dump_after_steps 10", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/dummy/data_dump_mkldnn_step11", shell=True)
                subprocess.call("mv data_dump_mkldnn /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/dummy/data_dump_mkldnn_step11", shell=True)
        elif (dataset == "mini"):
            step = sys.argv[4]
            if (step == "1"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m resnet50 -c skl -o 112 -b 128 --data_dir=/mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/dl_framework-intel_tensorflow_models/tf_mini_imagenet_data --data_name=imagenet --num_batches=1 --dump_after_steps=-1", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/mini/data_dump_mkldnn_step1", shell=True)
                subprocess.call("mv data_dump_mkldnn /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/mini/data_dump_mkldnn_step1", shell=True)

            elif (step == "11"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m resnet50 -c skl -o 112 -b 128 --data_dir=/mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/dl_framework-intel_tensorflow_models/tf_mini_imagenet_data --data_name=imagenet --num_batches=11 --dump_after_steps=10", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/mini/data_dump_mkldnn_step11", shell=True)
                subprocess.call("mv data_dump_mkldnn /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/mini/data_dump_mkldnn_step11", shell=True)
            

def run_eigen_mode():
    module = sys.argv[2]
    if (module == "inception3"):
        dataset = sys.argv[3]
        if (dataset == "dummy"):
            step = sys.argv[4]
            if (step == "1"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m inception3 -c skl -o 112 -b 128 --num_batches 1 --dump_after_steps -1", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/dummy/data_dump_eigen_step1", shell=True)
                subprocess.call("mv data_dump_eigen /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/dummy/data_dump_eigen_step1", shell=True)

            elif (step == "11"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m inception3 -c skl -o 112 -b 128 --num_batches 11 --dump_after_steps 10", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/dummy/data_dump_eigen_step11", shell=True)
                subprocess.call("mv data_dump_eigen /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/dummy/data_dump_eigen_step11", shell=True)
        elif (dataset == "mini"):
            step = sys.argv[4]
            if (step == "1"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m inception3 -c skl -o 112 -b 128 --data_dir=/mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/dl_framework-intel_tensorflow_models/tf_mini_imagenet_data --data_name=imagenet --num_batches=1 --dump_after_steps=-1", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/mini/data_dump_eigen_step1", shell=True)
                subprocess.call("mv data_dump_eigen /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/mini/data_dump_eigen_step1", shell=True)

            elif (step == "11"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m inception3 -c skl -o 112 -b 128 --data_dir=/mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/dl_framework-intel_tensorflow_models/tf_mini_imagenet_data --data_name=imagenet --num_batches=11 --dump_after_steps=10", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/mini/data_dump_eigen_step11", shell=True)
                subprocess.call("mv data_dump_eigen /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/inception/mini/data_dump_eigen_step11", shell=True)
    elif (module == "resnet50"):
        dataset = sys.argv[3]
        if (dataset == "dummy"):
            step = sys.argv[4]
            if (step == "1"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m resnet50 -c skl -o 112 -b 128 --num_batches 1 --dump_after_steps -1", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/dummy/data_dump_eigen_step1", shell=True)
                subprocess.call("mv data_dump_eigen /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/dummy/data_dump_eigen_step1", shell=True)

            elif (step == "11"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m resnet50 -c skl -o 112 -b 128 --num_batches 11 --dump_after_steps 10", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/dummy/data_dump_eigen_step11", shell=True)
                subprocess.call("mv data_dump_eigen /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/dummy/data_dump_eigen_step11", shell=True)
        elif (dataset == "mini"):
            step = sys.argv[4]
            if (step == "1"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m resnet50 -c skl -o 112 -b 128 --data_dir=/mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/dl_framework-intel_tensorflow_models/tf_mini_imagenet_data --data_name=imagenet --num_batches=1 --dump_after_steps=-1", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/mini/data_dump_eigen_step1", shell=True)
                subprocess.call("mv data_dump_eigen /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/mini/data_dump_eigen_step1", shell=True)

            elif (step == "11"):
                err_code = subprocess.call("python run_single_node_benchmark.py -f NHWC -m resnet50 -c skl -o 112 -b 128 --data_dir=/mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/dl_framework-intel_tensorflow_models/tf_mini_imagenet_data --data_name=imagenet --num_batches=11 --dump_after_steps=10", shell=True)
                if (err_code != 0):
                    return err_code
                subprocess.call("rm -rf /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/mini/data_dump_eigen_step11", shell=True)
                subprocess.call("mv data_dump_eigen /mnt/aipg_tensorflow_shared/wangwei3_shared/yuanhui/data/resnet/mini/data_dump_eigen_step11", shell=True)
 



if __name__ == "__main__":
    subprocess.call("rm -rf /tmp/resnet50_model/ /tmp/inception3_model/", shell=True)
    run_mode = sys.argv[1]
    if (run_mode == "mkl"):
        run_mkl_mode()
    elif (run_mode == "eigen"):
        run_eigen_mode()


        

