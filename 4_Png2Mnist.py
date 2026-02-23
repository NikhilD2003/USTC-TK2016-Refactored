# -*- coding: utf-8 -*-
# Wei Wang (ww8137@mail.ustc.edu.cn)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file, You
# can obtain one at http://mozilla.org/MPL/2.0/.
# ==============================================================================

import os
import errno
from PIL import Image
from array import *
from random import shuffle
import gzip    # Added native gzip for Windows compatibility
import shutil  # Added for native gzip

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# Load from and save to
mkdir_p('5_Mnist')

# FIX 1: Added 'r' (raw string) to fix the \T warning, and added the Test directory back
Names = [[r'4_Png\Train', r'5_Mnist\train'], [r'4_Png\Test', r'5_Mnist\test']]

for name in Names:	
    data_image = array('B')
    data_label = array('B')

    FileList = []
    
    # Quick check to ensure the directory exists before trying to read it
    if not os.path.exists(name[0]):
        print(f"Directory {name[0]} not found. Skipping...")
        continue

    for dirname in os.listdir(name[0]): 
        path = os.path.join(name[0],dirname)
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                FileList.append(os.path.join(name[0],dirname,filename))

    shuffle(FileList) # Useful for further segmenting the validation set

    for filename in FileList:
        # FIX 2: Added parentheses to the print statement
        print(filename)
        
        # Using os.sep makes the folder splitting work safely on Windows
        label = int(filename.split(os.sep)[2])
        Im = Image.open(filename)
        pixel = Im.load()
        width, height = Im.size
        for x in range(0,width):
            for y in range(0,height):
                data_image.append(pixel[y,x])
        data_label.append(label) # labels start (one unsigned byte each)
        
    hexval = "{0:#0{1}x}".format(len(FileList),6) # number of files in HEX
    hexval = '0x' + hexval[2:].zfill(8)
    
    # header for label array
    header = array('B')
    header.extend([0,0,8,1])
    header.append(int('0x'+hexval[2:][0:2],16))
    header.append(int('0x'+hexval[2:][2:4],16))
    header.append(int('0x'+hexval[2:][4:6],16))
    header.append(int('0x'+hexval[2:][6:8],16))	
    data_label = header + data_label

    # additional header for images array	
    if max([width,height]) <= 256:
        header.extend([0,0,0,width,0,0,0,height])
    else:
        raise ValueError('Image exceeds maximum size: 256x256 pixels')

    header[3] = 3 # Changing MSB for image data (0x00000803)	
    data_image = header + data_image
    
    output_file = open(name[1]+'-images-idx3-ubyte', 'wb')
    data_image.tofile(output_file)
    output_file.close()
    
    output_file = open(name[1]+'-labels-idx1-ubyte', 'wb')
    data_label.tofile(output_file)
    output_file.close()

# FIX 3: Replaced Linux os.system('gzip') with Python's native gzip library for Windows
for name in Names:
    # Compress images
    if os.path.exists(name[1]+'-images-idx3-ubyte'):
        with open(name[1]+'-images-idx3-ubyte', 'rb') as f_in:
            with gzip.open(name[1]+'-images-idx3-ubyte.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(name[1]+'-images-idx3-ubyte') # Clean up raw file
        
    # Compress labels
    if os.path.exists(name[1]+'-labels-idx1-ubyte'):
        with open(name[1]+'-labels-idx1-ubyte', 'rb') as f_in:
            with gzip.open(name[1]+'-labels-idx1-ubyte.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(name[1]+'-labels-idx1-ubyte') # Clean up raw file

print("Dataset successfully packed into MNIST format!")