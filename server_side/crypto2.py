
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]


PI = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

S_BOX = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
     ],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
     ],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
     ],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
     ],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
     ],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
     ],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
     ],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
     ]
]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

CP_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]


CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]


E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

rounds = 16


def to_binary(string):
    result = ""
    string = string.encode()
    for i in range(len(string)):
        binary = str(bin(string[i])[2:])
        if len(binary) < 8:
            while len(binary) < 8:
                binary = '0'+binary
        result += binary
    return result


def init_key(first_key):
    # first turn the key to 64 bits
    first_key = to_binary(first_key)
    result = CP_1.copy()
    return ''.join(map(lambda x: first_key[x - 1], result))


def cut(string):
    n = 8
    temp = [string[i:i+n] for i in range(0, len(string), n)]
    temp = list(map(lambda x: to_binary(x), temp))
    if len(temp[-1]) < 64:
        while len(temp[-1]) < 64:
            temp[-1] =  temp[-1] + '0'
    return list(map(lambda x: pi(x), temp))


def pi(string):
    result = PI.copy()
    return ''.join(map(lambda x: string[x-1], result))


# hare is the end of the begging

def Xor(string,massge,n):
    string=bin(int(string, 2) ^ int(massge, 2))
    binary = str(string)[2:]
    if len(binary) < n:
        while len(binary) < n:
            binary = '0'+binary
    return binary


def per(string):
    p = P.copy()
    return ''.join(map(lambda x: string[x - 1], p))


def magic_is_hare(string, index):
    row = int("0b"+(string[0]+string[5]), 2)
    col = int("0b"+(string[1:5]), 2)
    string = bin(S_BOX[index][row][col])
    binary = str(string)[2:]
    if len(binary) < 4:
        while len(binary) < 4:
            binary = '0'+binary
    return binary


def S_Boxes(string):
    n = 6
    temp = [string[i:i + n] for i in range(0, len(string), n)]
    result=''
    for i in range(len(temp)):
        result += magic_is_hare(temp[i],i)
    return result


def the_f(string,key):
    # בלוק שמאל
    left_block = string[0:32]
    # בלוק ימין
    right_block = string[32:64]
    extnsion=E.copy()
    new_left_block= right_block # this new left

    # extend the old right block from 32bits to 48 bits
    new_right_block = ''.join(map(lambda x: right_block[x - 1], extnsion))

    # xor oparasion on key and new right half after parmitasion
    xor_key_new_right = Xor(new_right_block, key, 48)

    # s-box substitution
    magic_boxes_result = S_Boxes(xor_key_new_right)

    parmitated_data_after_magic_box=per(magic_boxes_result)


    new_right_block = Xor(parmitated_data_after_magic_box, left_block, 32)

    new_block=new_right_block+new_left_block

    return new_block


def leftshift(string):
    string=list(string)
    temp = string[0]
    for i in range(1,len(string)):
        string[i-1]=string[i]
    string[-1]=temp
    result=""
    for i in string:
        result+=i
    return result




def key_scudeula(string):
    left_block_key = string[0:28]
    right_block_key = string[28:56]
    return leftshift(left_block_key)+leftshift(right_block_key)


def genrate_16_keys(key):
    new_keys=[0]*16
    key = init_key(key)
    new_keys[0] = key_scudeula(key)
    for i in range(2, 17):
        if i in [1, 2, 9, 16]:
            new_keys[i-1] = key_scudeula(new_keys[i-2])
        else:
            new_keys[i-1] = key_scudeula(key_scudeula(new_keys[i-2]))
    for i in range(16):
        parmate = CP_2.copy()
        new_keys[i] = "".join(map(lambda x: new_keys[i][x - 1], parmate))
    return new_keys


def pc_2(string):
    pi_2 = PI_1.copy()
    return ''.join(map(lambda x: string[x - 1], pi_2))


def des(plaintext,key):
    while len(plaintext)% 8!=0:
        plaintext += " "
    new_keys=genrate_16_keys(key)
    new_blocks=cut(plaintext)
   #works
    for block in range(len(new_blocks)):
        for round in range(rounds):
            new_blocks[block] = the_f(new_blocks[block],new_keys[round])
        new_blocks[block]=reverse_from_bit(pc_2(new_blocks[block]))
    return "".join(new_blocks)


def reverse_from_bit(string):
    n = 8
    temp = [string[i:i + n] for i in range(0, len(string), n)]
    result=""
    for i in range(8):
        result += chr(int(temp[i], 2))
    return result


def des_dicrypte(plaintext,key):
    new_keys=genrate_16_keys(key)
    new_keys=list(map(lambda x: new_keys[x], range(rounds-1, -1, -1)))
    new_blocks=cut(plaintext)
    for block in range(len(new_blocks)):
        for round in range(rounds):
            new_blocks[block] = the_f(new_blocks[block], new_keys[round])
        new_blocks[block]=reverse_from_bit(pc_2(new_blocks[block]))
    return "".join(new_blocks)

def listTOstring(list):
    string=""
    for i in list:
        string += str(i)
    return string





