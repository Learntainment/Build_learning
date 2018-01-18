"""
  Licensed Materials - Property of Intel
  (C) Copyright Intel Corp. 1968, 2017 All Rights Reserved
------------------------------------------------------------------------------------------------------------------------
File Name: single_comparison.py
Description: Run the comparison between two dump files.
Usage: general_cosim_tf.py [-x] --xile file 1 [-y] --yfile file 2
                           --rtol RTOL --atol ATOL

Author: Tian, Shilei (shilei.tian@intel.com)
Change Activity:
        Tian, Shilei: 2018-01-11 First work
-----------------------------------------------------------------------------------------------------------------------
"""
import argparse
import numpy as np
import os
import struct

if __name__ == '__main__':
    # Parse the opts and args
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--xfile', '-x', help='The x file name dumped.')
    parser.add_argument('--yfile', '-y', help='The y file name dumped.')
    parser.add_argument('--rtol', type=float, default=1e-2, help='The rtol')
    parser.add_argument('--atol', type=float, default=1e-3, help='The atol')

    args = parser.parse_args()

    xfilename = os.path.abspath(args.xfile)
    yfilename = os.path.abspath(args.yfile)

    rtol = float(args.rtol)
    atol = float(args.atol)

    with open(xfilename, 'rb') as f_x, open(yfilename, 'rb') as f_y:
        # Read the data size
        size_x = int(f_x.readline())
        size_y = int(f_y.readline())

        assert size_x == size_y

        size = size_x

        # Read the data from binary file and unpack to float32
        data_x = struct.unpack('f' * size, f_x.read(4 * size))
        data_y = struct.unpack('f' * size, f_y.read(4 * size))

        # Pack to numpy ndarray
        data_x = np.asarray(data_x)
        data_y = np.asarray(data_y)

        np.testing.assert_allclose(data_x, data_y, rtol=rtol, atol=atol, equal_nan=True)
