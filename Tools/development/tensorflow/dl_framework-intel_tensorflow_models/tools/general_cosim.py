"""
  Licensed Materials - Property of Intel
  (C) Copyright Intel Corp. 1968, 2017 All Rights Reserved
------------------------------------------------------------------------------------------------------------------------
File Name: general_cosim_tf.py
Description: Run the general cosim comparison.
Usage: general_cosim_tf.py [-m] --mkl_dir MKL_DUMP_DIR [-e] --eigen_dir EIGEN_DUMP_DIR
                           [-l] --layer_file EIGEN_LAYER_FILE
                           --actol ACTOL --rtol RTOL --atol ATOL

Author: Tian, Shilei (shilei.tian@intel.com)
Change Activity:
        Tian, Shilei: 2017-12-14 First work
        Tian, Shilei: 2017-12-20 Improve the comparison strategy
        Tian, Shilei: 2018-01-11 Added the skipping feature
        Tian, Shilei: 2018-01-17 Added the IOError handler
-----------------------------------------------------------------------------------------------------------------------
"""
import argparse
import numpy as np
import os
import struct

if __name__ == '__main__':
    # Parse the opts and args
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--mkl_dir', '-m', default='data_dump_mkl', help='The directory of mkl dump')
    parser.add_argument('--eigen_dir', '-e', default='data_dump_eigen', help='The directory of eigen dump')
    parser.add_argument('--layer_file', '-l', default='layers.txt', help='The *eigen* layer file')
    parser.add_argument('--actol', type=float, default=1.0, help='*actol* is for accumulative error')
    parser.add_argument('--rtol', type=float, default=1e-2, help='The rtol')
    parser.add_argument('--atol', type=float, default=1e-3, help='The atol')
    parser.add_argument('--start', type=int, default=-1, help='Starting line, -1 by default.')

    args = parser.parse_args()

    mkl_dir = os.path.abspath(args.mkl_dir)
    eigen_dir = os.path.abspath(args.eigen_dir)
    layer_file = os.path.abspath(args.layer_file)

    rtol = float(args.rtol)
    atol = float(args.atol)
    actol = float(args.actol)

    # Read the eigen layers from file
    with open(layer_file, 'r') as f:
        graph = f.read()
        graph = graph.splitlines()

    # Accumulative error
    accumulative_error = 0.0

    # Line count
    line = 0

    # General cosim comparison
    for node in graph:
        line += 1
        print('Check file: {0}...'.format(node)),
        if node.startswith('#') or (args.start != -1 and line < args.start):
            print('[\033[93mIgnore\033[0m]')
            continue

        mkl_file = os.path.join(mkl_dir, node)
        eigen_file = os.path.join(eigen_dir, node)

        try:
            with open(mkl_file, 'rb') as f_mkl, open(eigen_file, 'rb') as f_eigen:
                # Read the data size
                mkl_size = int(f_mkl.readline())
                eigen_size = int(f_eigen.readline())

                assert mkl_size == eigen_size, \
                    'The data size of the same node should be equal.\n' \
                    'mkl_size: {0}, eigen_size: {1}'.format(mkl_size, eigen_size)

                size = int(mkl_size)

                # Read the data from binary file and unpack to float32
                mkl_data = struct.unpack('f' * size, f_mkl.read(4 * size))
                eignen_data = struct.unpack('f' * size, f_eigen.read(4 * size))

                # Pack to numpy ndarray for `assert_allclose`
                mkl_data = np.asarray(mkl_data)
                eignen_data = np.asarray(eignen_data)

                np.testing.assert_allclose(mkl_data, eignen_data, rtol=rtol, atol=atol, equal_nan=True)
        except IOError:
            print('[\033[93mNOFILE\033[0m]')
            continue

        print('[\033[94mOK\033[0m]')
