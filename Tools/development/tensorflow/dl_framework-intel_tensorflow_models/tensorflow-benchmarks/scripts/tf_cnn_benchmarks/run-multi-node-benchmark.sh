# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

result_dir="results/"
python_script="run_single_node_benchmark.py"

if [ -z "$result_dir" ]; then
  echo "Error: path to result directory cannot be empty. Please add it in the shell script."
  exit 1
fi

if [ -z "$python_script" ]; then
  echo "Error: path to run_single_node_mode.py script cannot be empty. Please add it in the shell script."
  exit 1
fi

if [ -z "$LSB_HOSTS" ]; then
  echo "Error: no available nodes were found"
  exit 1
fi

if [ -z "$LSB_MAX_NUM_PROCESSORS" ]; then
  total_num_of_available_nodes=0
else
  total_num_of_available_nodes=$LSB_MAX_NUM_PROCESSORS
fi

echo "Total num of available nodes: "$total_num_of_available_nodes

read -p $'Please specify the model you would like to run: 
[0] alexnet 
[1] googlenet 
[2] vgg11
[3] inception3 
[4] resnet50\n>' usrMODEL

case $usrMODEL in
  0) MODEL="alexnet";;
  1) MODEL="googlenet";;
  2) MODEL="vgg11";;
  3) MODEL="inception3";;
  4) MODEL="resnet50";;
esac

if [ -z $MODEL ]; then
  echo "Error: no model was specified"
  exit 1
fi

read -p $'Please specify the CPU you would like to run on: 
[0] BDW 
[1] KNL 
[2] SKL
[3] KNM\n>' usrCPU

case $usrCPU in
  0) CPU="bdw";;
  1) CPU="knl";;
  2) CPU="skl";;
  3) CPU="knm";;
esac

if [ -z $CPU ]; then
  echo "Error: no CPU was specified"
  exit 1
fi

case $CPU in
  "bdw") if [ $MODEL == "alexnet" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "googlenet" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "vgg11" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "inception3" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "resnet50" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         ;;
  "knl") if [ $MODEL == "alexnet" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "googlenet" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "vgg11" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "inception3" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "resnet50" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         ;;
  "skl") if [ $MODEL == "alexnet" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "googlenet" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "vgg11" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "inception3" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         if [ $MODEL == "resnet50" ]; then
           default_PS_INTER_OP_NUM_THREADS=""
           default_PS_INTRA_OP_NUM_THREADS=""
         fi 
         ;;
esac

read -p "Please enter batch size. [Enter for default]:>" BATCH_SIZE

read -p $'Please specify the data format. [Enter for default]:
[0] NHWC
[1] NCHW\n>' usrDATA_FORMAT

case $usrDATA_FORMAT in
  0) DATA_FORAMT="NHWC";;
  1) DATA_FORMAT="NCHW";;
esac

read -p "Please specify OMP_NUM_THREADS value. [Enter for default]:>" OMP_NUM

read -p "Please enter number of PS inter-op threads.[Default is $default_PS_INTER_OP_NUM_THREADS]:>" PS_INTER_OP_NUM_THREADS
read -p "Please enter number of PS intra-op threads.[Default is $default_PS_INTRA_OP_NUM_THREADS]:>" PS_INTRA_OP_NUM_THREADS
read -p "Please enter number of worker inter-op threads. [Enter for default]:>" WORKER_INTER_OP_NUM_THREADS
read -p "Please enter number of worker intra-op threads. [Enter for default]:>" WORKER_INTRA_OP_NUM_THREADS

if [ -z "$PS_INTER_OP_NUM_THREADS" ]; then
  PS_INTER_OP_NUM_THREADS=$default_PS_INTER_OP_NUM_THREADS
fi

if [ -z "$PS_INTRA_OP_NUM_THREADS" ]; then
  PS_INTRA_OP_NUM_THREADS=$default_PS_INTRA_OP_NUM_THREADS
fi

read -p "Please specify the path to data directory. [Enter for default]:>" DATA_DIR

read -p "Please enter the the training data name. [Enter for default]:>" DATA_NAME

read -p "Enable distortions. [True/False, Enter for default]:>" DISTORTIONS

read -p "Pleae enter a name for the trace file. [Enter for default]:>" TRACE_FILE

read -p "Please enter the number of parameter servers:>" NUM_PS

read -p "Please enter the number of workers:>" NUM_WORKER

CONNECTION="Ethernet"
read -p $"Please specify the network connection. [Default is $CONNECTION]:
[0] Ethernet
[1] OPA
>" usrCONNECTION

if [ ! -z $usrCONNECTION ]; then
  case $usrCONNECTION in
    0) CONNECTION="Ethernet";;
    1) CONNECTION="OPA";;
  esac
else
  usrCONNECTION=0
fi

read -p "Please specify the server protocol. [Enter for default]:>" SERVER_PROTOCOL

read -p "Enable cross replica Sync. [True/False, Enter for default]:>" CROSS_REPLICA_SYNC

read -p "Enter optional description about this run:>" RUN_INFO

num_of_nodes_to_run_on=`expr "$NUM_PS" + "$NUM_WORKER"`

if [ "$num_of_nodes_to_run_on" -gt "$total_num_of_available_nodes" ]; then
  echo "Error: there is no enough available nodes to run on"
  exit 1
fi

#index all nodes
icount=0
icount2=0
ps_list=""
worker_list=""
port=":2222"
for i in $(echo $LSB_HOSTS | sed "s/\ /\\n/g")
 do 

  if [ $icount -ge ${num_of_nodes_to_run_on} ]; then
    break
  fi
  
  if [ $usrCONNECTION -eq 1 ]; then # OPA is 1
    i=$i"hib0"
  fi

  if [ "$HOSTNAME" = "$i" ]; then
    cur_node_indx=$icount 
  fi

  if [ "$icount" -lt "$NUM_PS" ]; then
    if [ "$ps_list" = "" ]; then
      ps_list="$i$port"
    else
      ps_list="$ps_list,$i$port"
    fi
  else
    if [ "$worker_list" = "" ]; then
      worker_list="$i$port" 
    else
      worker_list="$worker_list,$i$port" 
    fi
  fi

  host_array[icount]=$i
  icount=$((icount+1))
 done

output_dir_name=$CPU"_"$MODEL"_"$NUM_PS"_PS_"$NUM_WORKER"_workers_"$CONNECTION"_"`date +%Y-%m-%d-%H-%M-%S`

if [ ! -d $result_dir ]; then
  mkdir -p $result_dir
fi
result_dir=`readlink -f $result_dir`/
mkdir ${result_dir}${output_dir_name}
python_script=`readlink -f $python_script`

common_args="--model $MODEL --cpu $CPU "
if [ ! -z $BATCH_SIZE ]; then
  common_args=$common_args"--batch_size $BATCH_SIZE "
fi
if [ ! -z $DATA_FORMAT ]; then
  common_args=$common_args"--data_format $DATA_FORMAT "
fi
if [ ! -z $DATA_DIR ]; then
  common_args=$common_args"--data_dir $DATA_DIR "
fi
if [ ! -z $DATA_NAME ]; then
  common_args=$common_args"--data_name $DATA_NAME "
fi
if [ ! -z $DISTORTIONS ]; then
  common_args=$common_args"--distortions $DISTORTIONS "
fi
if [ ! -z "$TRACE_FILE" ]; then
  common_args=$common_args"--trace_file ${result_dir}${output_dir_name}/${TRACE_FILE} "
fi
if [ ! -z $SERVER_PROTOCOL ]; then
  common_args=$common_args"--server_protocol $SERVER_PROTOCOL "
fi
if [ ! -z $CROSS_REPLICA_SYNC ]; then
  common_args=$common_args"--cross_replica_sync $CROSS_REPLICA_SYNC "
fi

worker_args=$common_args
if [ ! -z $WORKER_INTRA_OP_NUM_THREADS ]; then
  worker_args=$worker_args"--num_intra_threads $WORKER_INTRA_OP_NUM_THREADS "
fi
if [ ! -z $WORKER_INTER_OP_NUM_THREADS ]; then
  worker_args=$worker_args"--num_inter_threads $WORKER_INTER_OP_NUM_THREADS "
fi
if [ ! -z $OMP_NUM ]; then
  worker_args=$worker_args"--num_omp_threads $OMP_NUM "
fi

PS_args=$common_args
if [ ! -z $PS_INTRA_OP_NUM_THREADS ]; then
  PS_args=$PS_args"--num_intra_threads $PS_INTRA_OP_NUM_THREADS "
fi
if [ ! -z $PS_INTER_OP_NUM_THREADS ]; then
  PS_args=$PS_args"--num_inter_threads $PS_INTER_OP_NUM_THREADS"
fi

echo "Run info: "$RUN_INFO >> ${result_dir}${output_dir_name}/run-info
echo "Worker args: "$worker_args >> ${result_dir}${output_dir_name}/run-info
echo "PS args: "$PS_args >> ${result_dir}${output_dir_name}/run-info
echo "No-of-PSs: "$NUM_PS >> ${result_dir}${output_dir_name}/run-info
echo "No-of-workers: "$NUM_WORKER >> ${result_dir}${output_dir_name}/run-info
echo "Connection type: "$CONNECTION >> ${result_dir}${output_dir_name}/run-info

#Run the model
first_pass=0
set -x
while [ $icount2 -lt $num_of_nodes_to_run_on ] 
  do
    out_file_name="${host_array[icount2]}.out" 
    err_file_name="${host_array[icount2]}.err"
    if [ $icount2 -lt $NUM_PS ]; then
      #boot a parameter server
      ssh ${host_array[icount2]} "nohup unbuffer python ${python_script} $PS_args --job_name ps \
--task_index ${icount2} --ps_hosts $ps_list --worker_hosts $worker_list \
> ${result_dir}${output_dir_name}/${out_file_name} 2> ${result_dir}${output_dir_name}/${err_file_name} < /dev/null &" &
    else
      if [ $first_pass -eq 0 ]; then
        sleep 20
        first_pass=1
      fi
      #boot a worker
      ssh ${host_array[icount2]} "numactl -H >> ${result_dir}${output_dir_name}/${out_file_name}; \
nohup unbuffer python ${python_script} $worker_args --job_name worker \
--task_index $((icount2-NUM_PS)) --ps_hosts $ps_list --worker_hosts $worker_list \
>> ${result_dir}${output_dir_name}/${out_file_name} 2>> ${result_dir}${output_dir_name}/${err_file_name} << /dev/null &" &
    fi
    icount2=$((icount2+1))
  done
  