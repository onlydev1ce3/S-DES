import itertools
import concurrent.futures
import time
import random
import matplotlib.pyplot as plt
#S-DES置换和S盒等设置
IP = (2, 6, 3, 1, 4, 8, 5, 7)
IP_INVERSE = (4, 1, 3, 5, 7, 2, 8, 6)
P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)
LEFT_SHIFT_1 = (2, 3, 4, 5, 1)
LEFT_SHIFT_2 = (3, 4, 5, 1, 2)
EP_BOX = (4, 1, 2, 3, 2, 3, 4, 1)
S_BOX_1 = [[(1, 0, 3, 2), (3, 2, 1, 0), (0, 2, 1, 3), (3, 1, 0, 2)],
           [(0, 1, 2, 3), (2, 3, 1, 0), (3, 0, 1, 2), (2, 1, 0, 3)]]
S_BOX_2 = [[(0, 1, 2, 3), (2, 3, 1, 0), (3, 0, 1, 2), (2, 1, 0, 3)],
           [(1, 0, 3, 2), (3, 2, 1, 0), (0, 2, 1, 3), (3, 1, 0, 2)]]
P4 = (2, 4, 3, 1)

#辅助函数
def permute(data, table):
    return ''.join(data[i - 1] for i in table)

def expand_permute(data, table):
    return ''.join(data[i - 1] for i in table)

def xor(data1, data2):
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(data1, data2))

def sbox(data, sbox_table):
    row = int(data[0] + data[3], 2)
    col = int(data[1] + data[2], 2)
    return bin(sbox_table[row][col][0])[2:].zfill(2) + bin(sbox_table[row][col][1])[2:].zfill(2)

def decrypt(ciphertext, key):
    """执行S-DES解密操作"""
    #执行初始置换IP
    ciphertext = permute(ciphertext, IP)

    #生成子密钥
    subkeys = generate_subkeys(key)

    #初始轮
    ciphertext, right_half = ciphertext[:4], ciphertext[4:]
    expanded_right = expand_permute(right_half, EP_BOX)
    xor_result = xor(expanded_right, subkeys[1])
    sbox_result = sbox(xor_result, S_BOX_2)
    p4_result = permute(sbox_result, P4)
    new_right_half = xor(ciphertext, p4_result)

    #第二轮
    left_half = right_half
    right_half = new_right_half
    expanded_right = expand_permute(right_half, EP_BOX)
    xor_result = xor(expanded_right, subkeys[0])
    sbox_result = sbox(xor_result, S_BOX_1)
    p4_result = permute(sbox_result, P4)
    new_right_half = xor(left_half, p4_result)

    #最终置换
    plaintext = new_right_half + right_half
    plaintext = permute(plaintext, IP_INVERSE)

    return plaintext

def generate_subkeys(key):
    key = permute(key, P10)
    subkeys = [key]
    for i in range(2):
        key = left_shift(key[:5], LEFT_SHIFT_1) + left_shift(key[5:], LEFT_SHIFT_1)
        subkeys.append(permute(key, P8))
    return subkeys

def left_shift(data, shift_table):
    return ''.join(data[i - 1] for i in shift_table)

def encrypt(plaintext, key):
    plaintext = permute(plaintext, IP)
    subkeys = generate_subkeys(key)
    plaintext, right_half = plaintext[:4], plaintext[4:]
    expanded_right = expand_permute(right_half, EP_BOX)
    xor_result = xor(expanded_right, subkeys[0])
    sbox_result = sbox(xor_result, S_BOX_1)
    p4_result = permute(sbox_result, P4)
    new_right_half = xor(plaintext, p4_result)
    left_half = right_half
    right_half = new_right_half
    expanded_right = expand_permute(right_half, EP_BOX)
    xor_result = xor(expanded_right, subkeys[1])
    sbox_result = sbox(xor_result, S_BOX_2)
    p4_result = permute(sbox_result, P4)
    new_right_half = xor(left_half, p4_result)
    ciphertext = new_right_half + right_half
    ciphertext = permute(ciphertext, IP_INVERSE)
    return ciphertext

def generate_all_possible_keys():
    return [''.join(key) for key in itertools.product("01", repeat=10)]

def brute_force_decrypt(ciphertext, possible_keys, start, end):
    for i in range(start, end):
        key = possible_keys[i]
        try:
            plaintext = decrypt(ciphertext, key)
            if plaintext == known_plaintext:
                return key
        except Exception:
            pass
    return None

if __name__ == "__main__":
    #已知的明文和密文对
    known_plaintext = "10101010"
    known_ciphertext = "00100110"

   # 记录每个密钥的暴力破解时间
key_times = []

def brute_force_decrypt(ciphertext, possible_keys, start, end):
    start_time = time.time()
    for i in range(start, end):
        key = possible_keys[i]
        try:
            plaintext = decrypt(ciphertext, key)
            if plaintext == known_plaintext:
                end_time = time.time()
                key_times.append(end_time - start_time)
                return key
        except Exception:
            pass
    return None

if __name__ == "__main__":
    # 生成所有可能的密钥
    possible_keys = generate_all_possible_keys()

    # 设置线程池和线程数
    num_threads = 4
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        chunk_size = len(possible_keys) // num_threads
        for i in range(num_threads):
            start = i * chunk_size
            end = start + chunk_size if i < num_threads - 1 else len(possible_keys)
            futures.append(executor.submit(brute_force_decrypt, known_ciphertext, possible_keys, start, end))

        correct_key = None
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                correct_key = result
                break

    if correct_key:
        print(f"找到正确的密钥: {correct_key}，花费的时间为：{key_times}")
    else:
        print("未找到匹配的密钥")

    