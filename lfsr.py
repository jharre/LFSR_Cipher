import sys
FEEDBACK_VALUE = 0x87654321

#in challenge specification
def lsfr(data):
    data_is_odd = data % 2 == 1
    shifted = data >> 1
    if data_is_odd:
        shifted ^= FEEDBACK_VALUE
    return shifted
# wrote next key function to handle stepping 8 times for a new key
def next_key(key):
    new_key = key
    for i in range(8):
        new_key = lsfr(new_key)
    
    return new_key
  

def cipher(data, initial_value):
    key = initial_value
    slashes = '\\'
    output = slashes
    padding = 2
    count = 1
    output_list = []

    for byte in data:
        key = next_key(key)
        as_hex_string = hex(key)[-2:]
        #checks for single hex ie. \x8 vs \x08
        if as_hex_string[0] == 'x':
            as_hex_string = as_hex_string[1]
        as_hex_int = int(as_hex_string,16)
        xord = byte ^ as_hex_int
        output_list.append(xord)
        count = count + 1
    return bytes(output_list)
def main():        
    data = []
    with open("input.bin", "rb") as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            data.append(int(byte.hex(),16))

    output = cipher(data, 0x12345678)

    #joining to print and encoding in latin-1 to read bytes 1 at a time and then decoding to ascii
    #toScreen = ''.join([chr(int(c,16)) for c in output])
    #print(toScreen.encode('latin-1', 'ignore').decode('ascii', 'ignore'))
    print(output)

if __name__ == "__main__":
    main()