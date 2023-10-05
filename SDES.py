import tkinter as tk
from tkinter import messagebox

#S-DES置换和S盒等设置
IP = (2, 6, 3, 1, 4, 8, 5, 7)  # 初始置换表
IP_INVERSE = (4, 1, 3, 5, 7, 2, 8, 6)  #逆初始置换表
P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)  #P10置换表
P8 = (6, 3, 7, 4, 8, 5, 10, 9)  #P8置换表
LEFT_SHIFT_1 = (2, 3, 4, 5, 1)  #密钥左移1位的置换表
LEFT_SHIFT_2 = (3, 4, 5, 1, 2)  #密钥左移2位的置换表
EP_BOX = (4, 1, 2, 3, 2, 3, 4, 1)  #扩展置换表
S_BOX_1 = [[(1, 0, 3, 2), (3, 2, 1, 0), (0, 2, 1, 3), (3, 1, 0, 2)],
           [(0, 1, 2, 3), (2, 3, 1, 0), (3, 0, 1, 2), (2, 1, 0, 3)]]  #S盒1
S_BOX_2 = [[(0, 1, 2, 3), (2, 3, 1, 0), (3, 0, 1, 2), (2, 1, 0, 3)],
           [(1, 0, 3, 2), (3, 2, 1, 0), (0, 2, 1, 3), (3, 1, 0, 2)]]  #S盒2
P4 = (2, 4, 3, 1)  #P4置换表


#辅助函数

def permute(data, table):
    """根据指定的置换表进行数据置换"""
    return ''.join(data[i - 1] for i in table)

def expand_permute(data, table):
    """根据指定的扩展置换表进行数据扩展置换"""
    return ''.join(data[i - 1] for i in table)

def xor(data1, data2):
    """执行数据的异或操作"""
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(data1, data2))

def sbox(data, sbox_table):
    """执行S盒替代操作"""
    row = int(data[0] + data[3], 2)
    col = int(data[1] + data[2], 2)
    return bin(sbox_table[row][col][0])[2:].zfill(2) + bin(sbox_table[row][col][1])[2:].zfill(2)

def generate_subkeys(key):
    """生成S-DES的子密钥"""
    key = permute(key, P10)
    subkeys = [key]
    for i in range(2):
        key = left_shift(key[:5], LEFT_SHIFT_1) + left_shift(key[5:], LEFT_SHIFT_1)
        subkeys.append(permute(key, P8))
    return subkeys

def left_shift(data, shift_table):
    """执行密钥的左移操作"""
    return ''.join(data[i - 1] for i in shift_table)

def encrypt(plaintext, key):
    """执行S-DES加密操作"""
    #执行初始置换IP
    plaintext = permute(plaintext, IP)

    #生成子密钥
    subkeys = generate_subkeys(key)

    #初始轮
    plaintext, right_half = plaintext[:4], plaintext[4:]
    expanded_right = expand_permute(right_half, EP_BOX)
    xor_result = xor(expanded_right, subkeys[0])
    sbox_result = sbox(xor_result, S_BOX_1)
    p4_result = permute(sbox_result, P4)
    new_right_half = xor(plaintext, p4_result)

    #第二轮
    left_half = right_half
    right_half = new_right_half
    expanded_right = expand_permute(right_half, EP_BOX)
    xor_result = xor(expanded_right, subkeys[1])
    sbox_result = sbox(xor_result, S_BOX_2)
    p4_result = permute(sbox_result, P4)
    new_right_half = xor(left_half, p4_result)

    #最终置换
    ciphertext = new_right_half + right_half
    ciphertext = permute(ciphertext, IP_INVERSE)

    return ciphertext

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



window = tk.Tk()
window.title("S-DES加密解密工具")
window.geometry("500x400")
frame = tk.Frame(window)
frame.pack(pady=20)
input_output_mode = tk.IntVar()
input_output_mode.set(0)

plaintext_label = tk.Label(frame, text="明文 (8位二进制或1字符ASCII):")
plaintext_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
plaintext_entry = tk.Entry(frame)
plaintext_entry.grid(row=0, column=1, padx=10, pady=5)

ciphertext_label = tk.Label(frame, text="密文 (8位二进制或1字符ASCII):")
ciphertext_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
ciphertext_entry = tk.Entry(frame)
ciphertext_entry.grid(row=1, column=1, padx=10, pady=5)

key_label = tk.Label(frame, text="密钥 (10位二进制):")
key_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
key_entry = tk.Entry(frame)
key_entry.grid(row=2, column=1, padx=10, pady=5)

mode_label = tk.Label(frame, text="选择输入/输出模式:")
mode_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

binary_mode_radio = tk.Radiobutton(frame, text="二进制模式", variable=input_output_mode, value=0)
binary_mode_radio.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

ascii_mode_radio = tk.Radiobutton(frame, text="ASCII模式", variable=input_output_mode, value=1)
ascii_mode_radio.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

encrypt_button = tk.Button(frame, text="加密", command=lambda: encrypt_button_click())
encrypt_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

decrypt_button = tk.Button(frame, text="解密", command=lambda: decrypt_button_click())
decrypt_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)


result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack(pady=10)


window.resizable(True, True)



#加密
def encrypt_button_click():
    plaintext = plaintext_entry.get()
    key = key_entry.get()
    mode = input_output_mode.get()

    if mode == 0:
        if len(plaintext) != 8 or len(key) != 10:
            messagebox.showerror("错误", "请输入正确长度的明文和密钥（8位和10位）")
            return

        try:
            ciphertext = encrypt(plaintext, key)
        except Exception as e:
            messagebox.showerror("错误", f"加密失败: {str(e)}，该明文无法被该密钥加密")
            return

        ciphertext_entry.delete(0, tk.END)
        ciphertext_entry.insert(0, ciphertext)
        result_label.config(text=f"加密结果: {ciphertext}")
    else:
        #在ASCII模式下，将ASCII字符转换为8位二进制进行加密
        if len(plaintext) != 1 or len(key) != 10:
            messagebox.showerror("错误", "请输入正确长度的ASCII字符和密钥（1字符和10位）")
            return

        ascii_binary_plaintext = format(ord(plaintext), '08b')

        try:
            ciphertext = encrypt(ascii_binary_plaintext, key)
            ciphertext = chr(int(ciphertext, 2))
        except Exception as e:
            #如果加密失败，显示错误消息
            messagebox.showerror("错误", f"加密失败: {str(e)}，该字符无法被该密钥加密")
            return

        ciphertext_entry.delete(0, tk.END)
        ciphertext_entry.insert(0, ciphertext)
        result_label.config(text=f"加密结果: {ciphertext}")
#解密
def decrypt_button_click():
    ciphertext = ciphertext_entry.get()
    key = key_entry.get()
    mode = input_output_mode.get()

    if mode == 0:
        if len(ciphertext) != 8 or len(key) != 10:
            messagebox.showerror("错误", "请输入正确长度的密文和密钥（8位和10位）")
            return

        try:
            plaintext = decrypt(ciphertext, key)
        except Exception as e:
            #如果解密失败，显示错误消息
            messagebox.showerror("错误", f"解密失败: {str(e)}，该密文无法被该密钥解密")
            return

        plaintext_entry.delete(0, tk.END)
        plaintext_entry.insert(0, plaintext)
        result_label.config(text=f"解密结果: {plaintext}")
    else:

        if len(key) != 10:
            messagebox.showerror("错误", "请输入正确长度的密钥（10位）")
            return

        try:
            #将ASCII字符转换为8位二进制
            ascii_binary_ciphertext = format(ord(ciphertext), '08b')
            plaintext_binary = decrypt(ascii_binary_ciphertext, key)
            plaintext = ''.join(chr(int(plaintext_binary[i:i+8], 2)) for i in range(0, len(plaintext_binary), 8))
        except Exception as e:
            #如果解密失败，显示错误消息
            messagebox.showerror("错误", f"解密失败: {str(e)}，该字符无法被该密钥解密")
            return

        plaintext_entry.delete(0, tk.END)
        plaintext_entry.insert(0, plaintext)
        result_label.config(text=f"解密结果: {plaintext}")


window.mainloop()