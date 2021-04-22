import sys
import os
import mmap
import hashlib
from kdb import kdb_parse

FEEDBACK_VALUE = 0x4F574154
entries_dict = {}
blocks_dict = {}
data_dict = {}
JPEG_END = b'\xFF\xD9'

if (len(sys.argv) != 3):
     print("Error: Wrong number of arguments")
     print("Example of correct usage: python ch3.py *magic_file* *obf_file")
     sys.exit()
magic_file = str(sys.argv[1])
obf_file = str(sys.argv[2])

data_dict = kdb_parse(magic_file)
magic = ''.join(chr(x) for x in data_dict['MAGIC']['decrypted'])
magic_b = bytes(magic, 'latin-1') # bytes string of magic

f = open(obf_file, 'rb')
data = bytearray(f.read())
f.close()

jpeg_starts = []
jpeg_ends = []

for i in range(len(data) - 3):
     if magic_b in data[i:i+3]:
          jpeg_starts.append(i)
     if JPEG_END in data[i:i+2]:
          jpeg_ends.append(i)

#fixing custom magic bytes
for i in jpeg_starts:
     data[i:i+3] = b'\xFF\xD8\xFF'
     
#create directory for jpegs
temp_name = obf_file.split('.')[0]
repaired_dir = temp_name + '_Repaired'
if not os.path.exists(repaired_dir):
     os.makedirs(repaired_dir)
#output to directory and standard out
for i in range(len(jpeg_starts)):
     start = jpeg_starts[i]
     end = jpeg_ends[i]
     path_name = os.path.join(repaired_dir, str(jpeg_starts[i]) + '.jpeg')
     
     with open(path_name, 'wb') as f:
          f.write(data[start:end])

     md5 = hashlib.md5(data[start:end])
     print('JPEG ' + str(i+1) + ' Detected at offset: ' + str(start))
     print('Size: ' + str(end - start))
     print('MD5 Hash: ' + str(md5.digest()))
     print('Path of repaired file: ' + path_name)
     print('\n')
