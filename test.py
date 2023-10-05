#密钥key、明文p、各个置换、S盒
key = "1010101010"
p10_table = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
p8_table = (6, 3, 7, 4, 8, 5, 10, 9)
p4_table = (2, 4, 3, 1)
p = "11111111"
ip_table = (2, 6, 3, 1, 4, 8, 5, 7)
ep_table = (4, 1, 2, 3, 2, 3, 4, 1)
ip_ni_table = (4, 1, 3, 5, 7, 2, 8, 6)
sbox0 = [
    [1, 0, 2, 3],
    [2, 3, 0, 1],
    [0, 1, 3, 2],
    [3, 2, 1, 0]
]

sbox1 = [
    [0, 1, 2, 3],
    [2, 0, 3, 1],
    [1, 3, 0, 2],
    [3, 2, 1, 0]
]

#辅助函数
def permute(input_str, table):
    output_str = ""
    for bit_position in table:
        output_str += input_str[bit_position - 1]
    return output_str


#循环左移
def ls(key, n):
    left_half = key[:5]
    right_half = key[5:]
    shifted_left = left_half[n:] + left_half[:n]
    shifted_right = right_half[n:] + right_half[:n]
    return shifted_left + shifted_right


#子密钥生成
def generate_key(k, p10_table, p8_table):
    p10_key = permute(k, p10_table)
    k1 = permute(ls(p10_key, 1), p8_table)
    k2 = permute(ls(ls(p10_key, 1), 2), p8_table)
    return k1, k2


#S-DES的F函数
def F(right_half, k):
    expanded = permute(right_half, ep_table)
    xored = '{0:08b}'.format(int(expanded, 2) ^ int(k, 2))
    s0_input = xored[:4]
    s1_input = xored[4:]
    s0_row = int(s0_input[0] + s0_input[-1], 2)
    s0_col = int(s0_input[1:-1], 2)
    s1_row = int(s1_input[0] + s1_input[-1], 2)
    s1_col = int(s1_input[1:-1], 2)
    s0_output = '{0:02b}'.format(sbox0[s0_row][s0_col])
    s1_output = '{0:02b}'.format(sbox1[s1_row][s1_col])
    s_output = s0_output + s1_output
    return permute(s_output, p4_table)


#加密
def encrypt(p, k1, k2):
    p = permute(p, ip_table)
    l0 = p[:4]
    r0 = p[4:]
    l1 = r0
    f_result = F(r0, k1)
    r1 = '{0:04b}'.format(int(l0, 2) ^ int(f_result, 2))
    f_result = F(r1, k2)
    r2 = '{0:04b}'.format(int(l1, 2) ^ int(f_result, 2))
    return permute(r2 + r1, ip_ni_table)


#解密
def decrypt(c, k1, k2):
    c = permute(c, ip_table)
    r2 = c[:4]
    l2 = c[4:]
    f_result = F(l2, k2)
    l1 = '{0:04b}'.format(int(r2, 2) ^ int(f_result, 2))
    f_result = F(l1, k1)
    r1 = '{0:04b}'.format(int(l2, 2) ^ int(f_result, 2))
    return permute(r1 + l1, ip_ni_table)




#生成子密钥 K1 和 K2
k1, k2 = generate_key(key, p10_table, p8_table)

#明文进行加密
ciphertext = encrypt(p, k1, k2)
#密文进行解密
plaintext = decrypt(ciphertext, k1, k2)

import random

#生成随机的 10 位密钥
def generate_random_key():
    return ''.join(random.choice('01') for _ in range(10))

#生成随机的明文
def generate_random_plaintext():
    return ''.join(random.choice('01') for _ in range(8))

#碰撞测试
num_tests = 1000  # 可以根据需要设置测试次数
success_count = 0
successful_combinations = []  # 用于存储成功的明文和密钥组合

for _ in range(num_tests):
    key1 = generate_random_key()
    key2 = generate_random_key()
    plaintext = generate_random_plaintext()
    
    #生成子密钥
    k1, k2 = generate_key(key1, p10_table, p8_table)
    
    #加密明文
    ciphertext1 = encrypt(plaintext, k1, k2)
    
    #生成不同的子密钥
    k1, k2 = generate_key(key2, p10_table, p8_table)
    
    #加密同样的明文
    ciphertext2 = encrypt(plaintext, k1, k2)
    
    try:
        #解密密文1
        decrypted_text1 = decrypt(ciphertext1, k1, k2)
        #解密密文2
        decrypted_text2 = decrypt(ciphertext2, k1, k2)
        
        #检查解密后的明文是否与原始明文相同
        if decrypted_text1 == plaintext and decrypted_text2 == plaintext:
            success_count += 1
            successful_combinations.append((plaintext, key1, key2))
        else:
            print("测试失败：不同的密钥产生了不同的解密结果")
            print("明文P:", plaintext)
            print("密钥K1:", key1)
            print("密钥K2:", key2)
            print("密文1:", ciphertext1)
            print("解密后的明文1:", decrypted_text1)
            print("密文2:", ciphertext2)
            print("解密后的明文2:", decrypted_text2)
    except Exception as e:
        print(f"测试失败：发生异常 - {e}")
        continue  #如果发生异常，跳过当前测试

print(f"成功通过 {success_count} 组测试，失败 {num_tests - success_count} 组测试")

#打印成功的明文和密钥组合
print("\n成功的明文和密钥组合：")
for combo in successful_combinations:
    print(f"明文: {combo[0]}, 密钥1: {combo[1]}, 密钥2: {combo[2]}")