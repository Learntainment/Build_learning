# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
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

"""A binary to train CIFAR-10 using multiple GPU's with synchronous updates.

Accuracy:
cifar10_multi_gpu_train.py achieves ~86% accuracy after 100K steps (256
epochs of data) as judged by cifar10_eval.py.

Speed: With batch_size 128.

System        | Step Time (sec/batch)  |     Accuracy
--------------------------------------------------------------------
1 Tesla K20m  | 0.35-0.60              | ~86% at 60K steps  (5 hours)
1 Tesla K40m  | 0.25-0.35              | ~86% at 100K steps (4 hours)
2 Tesla K20m  | 0.13-0.20              | ~84% at 30K steps  (2.5 hours)
3 Tesla K20m  | 0.13-0.18              | ~84% at 30K steps
4 Tesla K20m  | ~0.10                  | ~84% at 30K steps

Usage:
Please see the tutorial and website for how to download the CIFAR-10
data set, compile the program and train the model.

http://tensorflow.org/tutorials/deep_cnn/
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.client import timeline
from datetime import datetime
import os.path
import re
import time

import numpy as np
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
import cifar10
import os

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('train_dir', 'cifar10_train',
                           """Directory where to write event logs """
                           """and checkpoint.""")
tf.app.flags.DEFINE_integer('max_steps', 1000,
                            """Number of batches to run.""")
tf.app.flags.DEFINE_integer('num_gpus', 1,
                            """How many GPUs to use.""")
tf.app.flags.DEFINE_boolean('log_device_placement', False,
                            """Whether to log device placement.""")
tf.app.flags.DEFINE_string('job_name', '', 'One of "ps", "worker"') 
tf.app.flags.DEFINE_string('ps_hosts', '', 
                           """Comma-separated list of hostname:port for the """ 
                           """parameter server jobs. e.g. """ 
                           """'machine1:2222,machine2:1111,machine2:2222'""") 
tf.app.flags.DEFINE_string('worker_hosts', '', 
                           """Comma-separated list of hostname:port for the """ 
                           """worker jobs. e.g. """ 
                           """'machine1:2222,machine2:1111,machine2:2222'""") 
tf.app.flags.DEFINE_string('subset', 'train', 'Either "train" or "validation".') 
# Task ID is used to select the chief and also to access the local_step for 
# each replica to check staleness of the gradients in SyncReplicasOptimizer. 
tf.app.flags.DEFINE_integer( 
    'task_id', 0, 'Task ID of the worker/replica running the training.') 
# More details can be found in the SyncReplicasOptimizer class: 
# tensorflow/python/training/sync_replicas_optimizer.py 
tf.app.flags.DEFINE_integer('num_replicas_to_aggregate', -1, 
                            """Number of gradients to collect before """ 
                            """updating the parameters.""") 
tf.app.flags.DEFINE_integer('save_interval_secs', 10 * 60, 
                            'Save interval seconds.') 
tf.app.flags.DEFINE_integer('save_summaries_secs', 180, 
                            'Save summaries interval seconds.') 
tf.app.flags.DEFINE_float('initial_learning_rate', 0.045, 
                          'Initial learning rate.') 
tf.app.flags.DEFINE_float('num_epochs_per_decay', 2.0, 
                          'Epochs after which learning rate decays.') 
tf.app.flags.DEFINE_float('learning_rate_decay_factor', 0.94, 
                          'Learning rate decay factor.') 


def tower_loss(scope):
  """Calculate the total loss on a single tower running the CIFAR model.

  Args:
    scope: unique prefix string identifying the CIFAR tower, e.g. 'tower_0'

  Returns:
     Tensor of shape [] containing the total loss for a batch of data
  """
  # Get images and labels for CIFAR-10.
  images, labels = cifar10.distorted_inputs()

  # Build inference Graph.
  logits = cifar10.inference(images)

  # Build the portion of the Graph calculating the losses. Note that we will
  # assemble the total_loss using a custom function below.
  _ = cifar10.loss(logits, labels)

  # Assemble all of the losses for the current tower only.
  losses = tf.get_collection('losses', scope)

  # Calculate the total loss for the current tower.
  total_loss = tf.add_n(losses, name='total_loss')

  # Attach a scalar summary to all individual losses and the total loss; do the
  # same for the averaged version of the losses.
  for l in losses + [total_loss]:
    # Remove 'tower_[0-9]/' from the name in case this is a multi-GPU training
    # session. This helps the clarity of presentation on tensorboard.
    loss_name = re.sub('%s_[0-9]*/' % cifar10.TOWER_NAME, '', l.op.name)
    tf.summary.scalar(loss_name, l)

  return total_loss


def average_gradients(tower_grads):
  """Calculate the average gradient for each shared variable across all towers.

  Note that this function provides a synchronization point across all towers.

  Args:
    tower_grads: List of lists of (gradient, variable) tuples. The outer list
      is over individual gradients. The inner list is over the gradient
      calculation for each tower.
  Returns:
     List of pairs of (gradient, variable) where the gradient has been averaged
     across all towers.
  """
  average_grads = []
  for grad_and_vars in zip(*tower_grads):
    # Note that each grad_and_vars looks like the following:
    #   ((grad0_gpu0, var0_gpu0), ... , (grad0_gpuN, var0_gpuN))
    grads = []
    for g, _ in grad_and_vars:
      # Add 0 dimension to the gradients to represent the tower.
      expanded_g = tf.expand_dims(g, 0)

      # Append on a 'tower' dimension which we will average over below.
      grads.append(expanded_g)

    # Average over the 'tower' dimension.
    grad = tf.concat(axis=0, values=grads)
    grad = tf.reduce_mean(grad, 0)

    # Keep in mind that the Variables are redundant because they are shared
    # across towers. So .. we will just return the first tower's pointer to
    # the Variable.
    v = grad_and_vars[0][1]
    grad_and_var = (grad, v)
    average_grads.append(grad_and_var)
  return average_grads


def train(target, cluster_spec):
  """Train CIFAR-10 for a number of steps."""

  # Number of workers and parameter servers are inferred from the workers and ps 
  # hosts string. 
  num_workers = len(cluster_spec.as_dict()['worker']) 
  num_parameter_servers = len(cluster_spec.as_dict()['ps']) 
  # If no value is given, num_replicas_to_aggregate defaults to be the number of 
  # workers. 
  if FLAGS.num_replicas_to_aggregate == -1: 
    num_replicas_to_aggregate = num_workers 
  else: 
    num_replicas_to_aggregate = FLAGS.num_replicas_to_aggregate 
 
 
   # Both should be greater than 0 in a distributed training. 
  assert num_workers > 0 and num_parameter_servers > 0, (' num_workers and ' 
                                                        'num_parameter_servers' 
                                                        ' must be > 0.') 

																												
  print ('num of replicas %d' %num_replicas_to_aggregate)
  #with tf.Graph().as_default(), tf.device('/cpu:0'):
  #with tf.device('/job:worker/task:%d' % FLAGS.task_id):  
  # with tf.device(tf.train.replica_device_setter(cluster=cluster_spec)):
  #with tf.device(tf.train.replica_device_setter(ps_tasks=num_parameter_servers, worker_device='/job:worker/task:%d' % FLAGS.task_id)):#, ps_strategy=tf.contrib.training.GreedyLoadBalancingStrategy(num_parameter_servers, tf.contrib.training.byte_size_load_fn))):
  with tf.device(tf.train.replica_device_setter(ps_tasks=num_parameter_servers, worker_device="/job:worker/task:%d/cpu:%d" % (FLAGS.task_id, 0), cluster=cluster_spec)):
		# Create a variable to count the number of train() calls. This equals the
		# number of batches processed * FLAGS.num_gpus.
    global_step = tf.get_variable(
        'global_step', [],
        initializer=tf.constant_initializer(0), trainable=False, collections=['_variables_to_restore_', tf.GraphKeys.GLOBAL_VARIABLES, tf.GraphKeys.GLOBAL_STEP])

    # Calculate the learning rate schedule.
    num_batches_per_epoch = (cifar10.NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN /
                             FLAGS.batch_size)
                             
    decay_steps = int(num_batches_per_epoch * cifar10.NUM_EPOCHS_PER_DECAY)

    # Decay the learning rate exponentially based on the number of steps.
    lr = tf.train.exponential_decay(cifar10.INITIAL_LEARNING_RATE,
                                   global_step,
                                    decay_steps,
                                    cifar10.LEARNING_RATE_DECAY_FACTOR,
                                    staircase=True)

    is_chief = (FLAGS.task_id == 0)

    # Calculate the gradients for each model tower.
    tower_grads = []
    #with tf.device('/job:worker/task:%d' % FLAGS.task_id):
    with tf.variable_scope(tf.get_variable_scope()):
      for i in xrange(1):
        with tf.name_scope('%s_%d' % (cifar10.TOWER_NAME, i)) as scope:

          # Create an optimizer that performs gradient descent.
          opt = tf.train.GradientDescentOptimizer(lr)
          opt = tf.train.SyncReplicasOptimizer(opt, 
                                           replicas_to_aggregate=num_replicas_to_aggregate,
                                           total_num_replicas=num_workers,
                                           variable_averages=None,
                                           variables_to_average=None)
          # Calculate the loss for one tower of the CIFAR model. This function
          # constructs the entire CIFAR model but shares the variables across
          # all towers.
          loss = tower_loss(scope)

          # Reuse variables for the next tower.
          tf.get_variable_scope().reuse_variables()

          # Retain the summaries from the final tower.
          summaries = tf.get_collection(tf.GraphKeys.SUMMARIES, scope)

          # Calculate the gradients for the batch of data on this CIFAR tower.
          grads = opt.compute_gradients(loss)

          # Keep track of the gradients across all towers.
          tower_grads.append(grads)

    # We must calculate the mean of each gradient. Note that this is the
    # synchronization point across all towers.
    grads = average_gradients(tower_grads)

    # Add a summary to track the learning rate.
    summaries.append(tf.summary.scalar('learning_rate', lr))

    # Add histograms for gradients.
    for grad, var in grads:
      if grad is not None:
        summaries.append(tf.summary.histogram(var.op.name + '/gradients', grad))

    # Apply the gradients to adjust the shared variables.
    apply_gradient_op = opt.apply_gradients(grads, global_step=global_step)

    # Add histograms for trainable variables.
    for var in tf.trainable_variables():
      summaries.append(tf.summary.histogram(var.op.name, var))

    # Track the moving averages of all trainable variables.
    variable_averages = tf.train.ExponentialMovingAverage(
        cifar10.MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())

    #variables_to_average = (tf.trainable_variable() + tf.moving_average_variables())


    # Group all updates to into a single train op.
    train_op = tf.group(apply_gradient_op, variables_averages_op)

    #get chief queue_runner
    chief_queue_runners = [opt.get_chief_queue_runner()]
    init_tokens_op = opt.get_init_tokens_op()

    # Create a saver.
    saver = tf.train.Saver(tf.global_variables())

    # Build the summary operation from the last tower summaries.
    summary_op = tf.summary.merge(summaries)

    # Build an initialization operation to run below.
    init_op = tf.global_variables_initializer()

    #Initi supervisor
    sv = tf.train.Supervisor(is_chief=is_chief,
                             logdir=FLAGS.train_dir,
                             init_op=init_op,
                             summary_op=None,
                             global_step=global_step,
                             saver=saver,
                             save_model_secs=FLAGS.save_interval_secs)

    # Start running operations on the Graph. allow_soft_placement must be set to
    # True to build towers on GPU, as some of the ops do not have GPU
    # implementations.
    sess_config=tf.ConfigProto(allow_soft_placement=False,
                               log_device_placement=FLAGS.log_device_placement, inter_op_parallelism_threads=4,intra_op_parallelism_threads=34)
    sess=sv.prepare_or_wait_for_session(target, config=sess_config)

    queue_runners = tf.get_collection(tf.GraphKeys.QUEUE_RUNNERS)
    sv.start_queue_runners(sess, queue_runners);

    if is_chief:
      sv.start_queue_runners(sess, chief_queue_runners)
      sess.run(init_tokens_op)

    tf.logging.info('Started %d queues for processing input data.', 
                    len(queue_runners)) 

    #summary_writer = tf.summary.FileWriter(FLAGS.train_dir, sess.graph)

    step =0
    sum_examples_per_sec = 0
    sum_sec_per_batch = 0
    #for step in xrange(FLAGS.max_steps):
    while not sv.should_stop():
      #print ('I am worker %d and I started my queue' %FLAGS.task_id)
      step = step + 1;
      start_time = time.time()
      # run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
      # run_metadata = tf.RunMetadata()	
      _, loss_value, gstep = sess.run([train_op, loss, global_step])#,options=run_options, run_metadata=run_metadata)
      # tl = timeline.Timeline(run_metadata.step_stats)
      # ctf = tl.generate_chrome_trace_format()
      # filename='timeline' + `step` + '.json'
      # with open(filename, 'w') as f:
        # f.write(ctf)
      duration = time.time() - start_time

      assert not np.isnan(loss_value), 'Model diverged with loss = NaN'
      num_examples_per_step = FLAGS.batch_size * FLAGS.num_gpus
      examples_per_sec = num_examples_per_step / duration
      sec_per_batch = duration / FLAGS.num_gpus
      
      sum_examples_per_sec = sum_examples_per_sec + examples_per_sec
      sum_sec_per_batch = sum_sec_per_batch + sec_per_batch
      
      if step % 100 == 0:
        format_str = ('Worker%d: %s: step %d, loss = %.2f (%.1f examples/sec; %.3f '
                    'sec/batch)')
        print (format_str % (FLAGS.task_id, datetime.now(), step, loss_value,
                             sum_examples_per_sec/100, sum_sec_per_batch/100))
        sum_examples_per_sec = 0
        sum_sec_per_batch = 0

      # if step % 100 == 0:
        # summary_str = sess.run(summary_op)
        # summary_writer.add_summary(summary_str, step)

      # Save the model checkpoint periodically.
      # if step % 1000 == 0 or (step + 1) == FLAGS.max_steps:
        # checkpoint_path = os.path.join(FLAGS.train_dir, 'model.ckpt')
        # saver.save(sess, checkpoint_path, global_step=step)


def main(argv=None):  # pylint: disable=unused-argument

  assert FLAGS.job_name in ['ps', 'worker'], 'job_name must be ps or worker' 
	
  # Extract all the hostnames for the ps and worker jobs to construct the 
  # cluster spec. 
  ps_hosts = FLAGS.ps_hosts.split(',') 
  worker_hosts = FLAGS.worker_hosts.split(',') 
  tf.logging.info('PS hosts are: %s' % ps_hosts) 
  tf.logging.info('Worker hosts are: %s' % worker_hosts) 

  cluster_spec = tf.train.ClusterSpec({'ps': ps_hosts, 
                                       'worker': worker_hosts}) 
  server = tf.train.Server( 
      {'ps': ps_hosts, 
       'worker': worker_hosts}, 
      job_name=FLAGS.job_name, 
      task_index=FLAGS.task_id, protocol='grpc+mpi') 

  if FLAGS.job_name == 'ps': 
    # `ps` jobs wait for incoming connections from the workers. 
    server.join() 
  else:
    os.environ["KMP_BLOCKTIME"] = "1"
    os.environ["KMP_SETTINGS"] = "1"
    os.environ["KMP_AFFINITY"]= "granularity=fine,verbose,compact,1,0"
    os.environ["OMP_NUM_THREADS"]= "34" 
    os.environ["MKL_NUM_THREADS"]= "50" 
    # cifar10.maybe_download_and_extract()
    if FLAGS.job_name == 'ps':
      if tf.gfile.Exists(FLAGS.train_dir):
        tf.gfile.DeleteRecursively(FLAGS.train_dir)
      tf.gfile.MakeDirs(FLAGS.train_dir)

    train(server.target, cluster_spec)


if __name__ == '__main__':
  tf.app.run()
