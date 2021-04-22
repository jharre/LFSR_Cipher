import os
import mmap
from lfsr import cipher, next_key, lsfr
FEEDBACK_VALUE = 0x4F574154
entries_dict = {}
blocks_dict = {}
data_dict = {}

def kdb_parse(filename):
    f = open(filename, "r+b")
    FILE_SIZE = os.stat(filename).st_size
    os.chmod(filename, 0o777)   #needed to ensure access to mapping file to memory in order to easily slice
    data = mmap.mmap(f.fileno(), 0) #mapping of the data to memory
    f.close()
    magic = data[:6]
    entry_list_ptr = data[6:10]
    entry_list_ptr = int.from_bytes(entry_list_ptr,"little")
    tmp = entry_list_ptr #creating temporary variable to save entry_list_ptr due to incrementing

    while True:
        end = data[tmp:(tmp+4)] #variable to check if it is the end of the list
        try:
            end = int.from_bytes(end,"little")
        except:
            print()
        if end == 4294967295:
            # checks for int value of 0xFFFFFFFF and breaks out of loop
            break
        
        end_of_name = tmp + 16
        end_of_data = end_of_name + 3
        entries_dict[data[tmp:end_of_name].decode('unicode_escape').rstrip('\x00')] =   {
                                                                    'name': data[tmp:end_of_name].decode('unicode_escape').rstrip('\x00'),
                                                                    'block_list': int.from_bytes(data[end_of_name:end_of_data], "little")
                                                                   }
        tmp += 20 #increment by 20 because len(int32) + len(char * 16) is 20

    for key, value in entries_dict.items():
        block_start = value['block_list']
        block_end = block_start + 6 #inc 6 for len(int16) + len(int32)
        blocks_dict[key] = {'size': int.from_bytes(data[block_start:block_start + 1], "little"),
                            'data_ptr': int.from_bytes(data[block_start + 2:block_end], "little")}

    for key, value in blocks_dict.items():
        bytes_start = value['data_ptr']
        size = value['size']
        temp_array = []
        temp = bytes_start
        bytes_end = bytes_start + size

        while temp != bytes_end:
            temp_array.append(data[temp])
            temp += 1
            data_check = data[temp]
        decrypted_array = cipher(temp_array, FEEDBACK_VALUE) # call to cipher in lsfr.py
        data_dict[key] = {  'encrypted': temp_array,
                            'decrypted': decrypted_array
                            }
    return data_dict

def print_output():
    #fout = open('kdb_output.txt', 'a')
    for key, value in data_dict.items():
        toScreen = ''.join([chr(c) for c in value['decrypted']])
        #encode in latin-1 to read byte by byte as teh default utf-8 does it up to 6 bytes and decode in ascii
        print(key, ":", toScreen.encode('latin-1').decode('ascii'))
        #fout.write(key + ":" + toScreen.encode('latin-1').decode('ascii') + "\n")
    #fout.close()


def main():        
    filename = input("Enter KDB File: ")
    kdb_parse(filename)
    print_output()
if __name__ == "__main__":
    main()