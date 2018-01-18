"""
  Licensed Materials - Property of Intel
  (C) Copyright Intel Corp. 1968, 2017 All Rights Reserved
------------------------------------------------------------------------------------------------------------------------
File Name: read_tensor.py
Description: Display part of data from dumped file.
Usage: read_tensor.py [-f] --file FILE_NAME [-c] --count NUM_OF_DATA

Author: Tian, Shilei (shilei.tian@intel.com)
Change Activity:
        Tian, Shilei: 2018-01-05 First work
-----------------------------------------------------------------------------------------------------------------------
"""
import argparse
import numpy as np
import os
import struct

if __name__ == '__main__':
    # Parse the opts and args
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--file', '-f', help='The file name dumped.')
    parser.add_argument('--count', '-c', type=int, default=10, help='The number of data displayed.')


    args = parser.parse_args()

    filename = os.path.abspath(args.file)

    with open(filename, 'rb') as f:
        # Read the data size
        size = int(f.readline())

        # Read the data from binary file and unpack to float32
        data = struct.unpack('f' * size, f.read(4 * size))

        # Pack to numpy ndarray
        data = np.asarray(data)

        print('size:{0}, data: {1}'.format(size, data[:min(args.count, size)]))
