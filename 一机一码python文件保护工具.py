from datetime import datetime
import tkinter as tk
from tkinter import messagebox
# pip install windnd
from windnd import hook_dropfiles
import random
# pip install pycryptodome
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA384
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
import os
import base64
# pip install pyperclip
import pyperclip
import re


mid_font = ('Noto Sans Mono', 13)
font = ('Noto Sans Mono', 11)
activate_window = tk.Tk()
activate_window.title('软件保护工具')
activate_window.geometry("404x414")
colors = ['blue', 'red', 'black', 'green', 'purple', 'orange']
ind = 0
frm = tk.Frame(activate_window)
frm.pack()


def create_rsa_key(length: int):
    clean_all_widget(frm)
    label = tk.Label(frm, text='程序正在进行中，请稍候……', font=mid_font)
    label.pack()
    activate_window.update()
    label.destroy()
    label1 = tk.Label(frm, text=f'{length}位密钥生成成功', font=mid_font)
    label1.pack()
    random_generator = Random.new(random.random()).read
    rsa = RSA.generate(length, random_generator)
    # 生成私钥
    private_key = rsa.exportKey()
    # 生成公钥（从私钥中推导）
    public_key = rsa.publickey().exportKey()
    label2 = tk.Label(frm, text='公钥：' + public_key.decode('utf-8')[26: 37] + '...' + public_key.decode('utf-8')[-40: -24], font=mid_font)
    label2.pack()
    label3 = tk.Label(frm, text='私钥：' + private_key.decode('utf-8')[31: 42] + '...' + private_key.decode('utf-8')[-45: -29], font=mid_font)
    label3.pack()
    # 保存公私钥
    current_path = os.getcwd()
    key_path = current_path + '\\keys'
    if not os.path.exists(key_path):
        os.mkdir(key_path)
    with open(key_path + f'\\public_key_{length}.pem', 'wb+') as pubfile:
        pubfile.write(public_key)
    with open(key_path + f'\\private_key_{length}.pem', 'wb+') as prifile:
        prifile.write(private_key)
    label4 = tk.Label(frm, text='公私钥已经保存至', font=mid_font)
    label4.pack()
    entry1 = tk.Entry(frm, width=44, font=mid_font)
    entry1.pack()
    entry1.insert(0, key_path)
    label5 = tk.Label(frm, text='文件夹中的.pem文件内', font=mid_font)
    label5.pack()


def create_rsa_key_1024():
    create_rsa_key(1024)


def create_rsa_key_2048():
    create_rsa_key(2048)


def create_rsa_key_3072():
    create_rsa_key(3072)


def create_rsa_key_4096():
    create_rsa_key(4096)


def clean_all_widget(frame: tk.Frame):
    for widget in frame.winfo_children():
        widget.destroy()


def dragged_files(files, entry):
    file = files[0].decode("GBK")  # 用户拖入多个文件时，只取第一个
    entry.delete(0, 'end')
    entry.insert('end', file)


def reset(text_or_entry):
    if isinstance(text_or_entry, tk.Text):
        text_or_entry.delete(1.0, 'end')
    if isinstance(text_or_entry, tk.Entry):
        text_or_entry.delete(0, 'end')


def copy(text5: tk.Text, button6):
    global ind
    pyperclip.copy(text5.get(1.0, 'end').rstrip("\n"))
    ind = (ind + 1) % 6
    button6.config(fg=colors[ind])


def change_entry_show(var2, entry1):
    if var2.get() == '1':
        entry1.config(show='*')
    elif var2.get() == '0':
        entry1.config(show='')


def activation():
    clean_all_widget(frm)
    name = tk.Label(frm, text='管理员激活用户', fg=colors[4], font=mid_font)
    name.pack()

    def drag1(files):
        dragged_files(files, entry1)

    def change_entry1_show():
        change_entry_show(var1, entry1)

    def enter_length(*args):
        if validity.get() == '其他':
            entry2.grid(row=1, column=3)
            label4.grid(row=1, column=4)
        else:
            entry2.grid_forget()
            label4.grid_forget()

    def _reset():
        reset(text1)

    def _copy():
        copy(text2, button3)

    def process():
        # 先处理用于签名的私钥
        key_path = entry1.get().strip().strip('\"').strip('“').rstrip('”')
        if os.path.exists(key_path) and '.pem' in key_path:
            with open(key_path, 'rb') as keyfile:
                p = keyfile.read()
            try:
                key = RSA.importKey(p)
                if bytes("-----BEGIN RSA PRIVATE KEY-----".encode('utf-8')) in p:
                    privkey_signer = PKCS1_signature.new(key)
                else:
                    tk.messagebox.showerror(title='密钥错误', message="输入的密钥不是私钥")
                    return 0
            except Exception:
                tk.messagebox.showerror(title='密钥错误', message='读取到的.pem文件不是密钥')
                return 0
        else:
            tk.messagebox.showerror(title='密钥错误', message='密钥文件路径错误')
            return 0
        # 再将要签名的文字变为哈希，注意这里要签名的内容为 用户身份标识符 + 激活时间 + 有效期
        activation_code = {"激活时间": str(datetime.now()), "有效期限": ..., "数字签名": ...}
        try:
            if validity.get() != '其他':
                activation_code["有效期限"] = validity.get()
            elif validity.get() == '其他' and isinstance(eval(entry2.get()), int) and eval(entry2.get()) >= 1:
                activation_code["有效期限"] = entry2.get() + '天'
            else:
                tk.messagebox.showerror(title='格式错误', message='有效期的天数应为正整数')
                return 0
        except Exception:
            tk.messagebox.showerror(title='格式错误', message='有效期的天数应为正整数')
            return 0
        hasher = SHA384.new()
        hasher.update('/'.join([text1.get(1.0, 'end').rstrip("\n").strip(), activation_code["激活时间"], activation_code["有效期限"]]).encode('utf-8'))
        # 最后进行签名
        try:
            signature = base64.b64encode(privkey_signer.sign(hasher))
        except Exception:
            tk.messagebox.showerror(title='密钥错误', message='这不是一个正确的私钥')
            return 0
        activation_code["数字签名"] = str(signature).lstrip("b'").rstrip("'")
        text2.delete(1.0, 'end')
        text2.insert(1.0, str(activation_code))

    frm1 = tk.Frame(frm)
    frm1.pack()
    label1 = tk.Label(frm1, text='请输入私钥所在的绝对路径：', font=mid_font)
    label1.grid(row=1, column=1, padx=5)
    var1 = tk.StringVar()
    var1.set('0')
    cb1 = tk.Checkbutton(frm1, text='隐藏', variable=var1, onvalue='1', offvalue='0', command=change_entry1_show, font=mid_font)
    cb1.grid(row=1, column=2, padx=5)
    entry1 = tk.Entry(frm, font=mid_font, width=44)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)
    label2 = tk.Label(frm, text='请输入用户的身份标识符：', font=mid_font)
    label2.pack()
    text1 = tk.Text(frm, width=44, height=5, font=mid_font)
    text1.pack()
    frm2 = tk.Frame(frm)
    frm2.pack()
    label3 = tk.Label(frm2, text='请设置有效期：', font=mid_font)
    label3.grid(row=1, column=1, padx=15)
    validity = tk.StringVar()
    validity.set('7天')
    option_menu = tk.OptionMenu(frm2, validity, *('7天', '30天', '永久', '其他'), command=enter_length)
    option_menu.config(font=('Noto Sans Mono', 11))
    option_menu.grid(row=1, column=2)
    entry2 = tk.Entry(frm2, width=5, font=mid_font)
    label4 = tk.Label(frm2, text='天', font=mid_font)
    frm3 = tk.Frame(frm)
    frm3.pack()
    button1 = tk.Button(frm3, text='重置用户', font=mid_font, command=_reset)
    button1.grid(row=1, column=1, padx=10)
    button2 = tk.Button(frm3, text='开始激活', font=mid_font, command=process)
    button2.grid(row=1, column=2, padx=10)
    button3 = tk.Button(frm3, text='复制结果', font=mid_font, command=_copy)
    button3.grid(row=1, column=3, padx=10)
    label5 = tk.Label(frm, text='该用户的激活码为：', font=mid_font)
    label5.pack()
    text2 = tk.Text(frm, width=44, height=8, font=mid_font)
    text2.pack()


def pack_main():
    clean_all_widget(frm)
    name = tk.Label(frm, text='为主程序添加一机一码功能', fg=colors[4], font=mid_font)
    name.pack()

    def drag1(files):
        dragged_files(files, entry1)

    def read_environment_of_entry2(*args):
        reset(text1)
        path = entry2.get().strip().strip('\"').lstrip('“').rstrip('”')
        if os.path.exists(path) and path.endswith(".py"):
            with open(path, 'r', encoding='utf-8') as f:
                while True:
                    line = f.readline()
                    if line.startswith('from') or line.startswith('import'):
                        text1.insert('end', line)
                    elif line.startswith('#') or line.startswith('\n'):
                        ...
                    else:
                        break

    def drag2(files):
        dragged_files(files, entry2)
        read_environment_of_entry2()

    def _reset():
        reset(text1)

    def process():
        label5.config(text='正在加壳中，请稍候...')
        activate_window.update()

        # 先把主程序写入软件所在文件中的demonstration.py
        main_path = entry2.get().strip().strip('\"').lstrip('“').rstrip('”')
        if os.path.exists(main_path):
            with open('demonstration.py', 'wb') as outfile, open(main_path, 'rb') as infile:
                outfile.write(infile.read())
        else:
            label5.config(text='')
            messagebox.showerror('路径错误', '主程序的路径不存在')
            return 0

        # 再把start.py写入主程序所在文件夹中的start.py
        dir_of_main_py = os.path.dirname(main_path)
        # 下面是start.py的源码（不包含头部的调用库）
        start_code = r'''
pubkey_verifier = PKCS1_signature.new(RSA.importKey(pubkey_bytes))
c = wmi.WMI()
# 获取CPU序列号
for index, cpu in enumerate(c.Win32_Processor()):
    cpu_id = cpu.ProcessorId.strip()
# 本机 id: BFEBFBFF000806EC


def login():
    colors = ['blue', 'red', 'black', 'green', 'purple', 'orange']
    ind = 0

    def copy():
        nonlocal ind
        pyperclip.copy(cpu_id)
        ind = (ind + 1) % 6
        button1.config(fg=colors[ind])

    def reset():
        text1.delete(1.0, 'end')

    def activate():
        nonlocal ind
        ind = (ind + 1) % 6
        label4.config(text='', fg=colors[ind])
        # 再处理身份标识符和数字签名
        try:
            activation_code = eval(text1.get(1.0, 'end').rstrip('\n'))
            signature = base64.b64decode(activation_code["数字签名"])
            hasher = SHA384.new()
            hasher.update('/'.join([cpu_id, activation_code["激活时间"], activation_code["有效期限"]]).encode('utf-8'))
            # 注意一下，这里的 activation_code 的来源是用户输入的信息，而不是保存在文件中的
        except Exception:
            label4.config(text='激活码格式错误')
        else:
            if pubkey_verifier.verify(hasher, signature) and (activation_code["有效期限"] == '永久' or eval(activation_code["有效期限"].rstrip('天')) - (datetime.now() - datetime.strptime(activation_code['激活时间'], "%Y-%m-%d %H:%M:%S.%f")).days >= 0):
                label4.config(text='激活成功，3秒后软件将自动启动，请勿关闭窗口')
                activate_window.update()
                with open("system_resource/activation_code.txt", 'w', encoding='utf-8') as f:
                    f.write(str(activation_code))
                time.sleep(3)
                activate_window.destroy()
                import demonstration
            else:
                label4.config(text='激活失败')

    activate_window = tk.Tk()
    activate_window.title('产品激活')
    activate_window.geometry(width_and_height)
    label1 = tk.Label(activate_window, text='请将下方身份标识符发送给销售客服进行产品激活', font=mid_font)
    label1.pack()
    label2 = tk.Label(activate_window, text=f'或联系管理员 {contact}', font=mid_font)
    label2.pack()
    frm1 = tk.Frame(activate_window)
    frm1.pack()
    label5 = tk.Label(frm1, font=mid_font, text='身份标识符：')
    label5.grid(row=1, column=1)
    entry1 = tk.Entry(frm1, font=mid_font)
    entry1.grid(row=1, column=2, padx=10)
    entry1.insert(0, cpu_id)
    entry1.config(state='readonly')
    button1 = tk.Button(frm1, text='复制', fg=colors[ind], command=copy, font=mid_font)
    button1.grid(row=1, column=3, padx=10)
    label3 = tk.Label(activate_window, text='请输入您的专属激活码：', font=mid_font)
    label3.pack()
    text1 = tk.Text(activate_window, width=44, height=8, font=mid_font)
    text1.pack()
    frm2 = tk.Frame(activate_window)
    frm2.pack()
    button2 = tk.Button(frm2, text='重置', command=reset, font=mid_font)
    button2.grid(row=1, column=1, padx=20)
    button3 = tk.Button(frm2, text='激活', command=activate, font=mid_font)
    button3.grid(row=1, column=2, padx=20)
    label4 = tk.Label(activate_window, text='', font=mid_font)
    label4.pack()

    activate_window.mainloop()


mid_font = ('Noto Sans Mono', 13)
if not os.path.exists("system_resource"):
    os.mkdir("system_resource")
try:
    with open("system_resource/activation_code.txt", 'r', encoding='utf-8') as f:
        activation_code = eval(f.read())
    signature = base64.b64decode(activation_code["数字签名"])
    hasher = SHA384.new()
    hasher.update('/'.join([cpu_id, activation_code["激活时间"], activation_code["有效期限"]]).encode('utf-8'))
    # 注意一下，这里的 activation_code 的来源是保存在文件中的信息，而不是用户输入的
    if pubkey_verifier.verify(hasher, signature):
        if activation_code["有效期限"] == '永久':
            import demonstration

        elif 0 <= eval(activation_code['有效期限'].rstrip('天')) - (datetime.now() - datetime.strptime(activation_code['激活时间'], "%Y-%m-%d %H:%M:%S.%f")).days <= 7:
            # 剩余有效期小于等于7天，大于等于0天
            prompt_window = tk.Tk()
            prompt_window.geometry('350x80')
            prompt_window.title('激活即将到期')
            label1 = tk.Label(prompt_window, text=f"激活剩余有效期：{eval(activation_code['有效期限'].rstrip('天')) - (datetime.now() - datetime.strptime(activation_code['激活时间'], '%Y-%m-%d %H:%M:%S.%f')).days}天", font=mid_font)
            label1.pack()
            label2 = tk.Label(prompt_window, text='请联系客服或管理员及时续费', font=mid_font)
            label2.pack()
            frm1 = tk.Frame(prompt_window)
            frm1.pack()

            def renew():
                prompt_window.destroy()
                login()

            def not_yet():
                prompt_window.destroy()
                import demonstration

            button1 = tk.Button(frm1, text='立即续费', font=mid_font, command=renew)
            button1.grid(row=1, column=1, padx=10)
            button2 = tk.Button(frm1, text='暂不续费', font=mid_font, command=not_yet)
            button2.grid(row=1, column=2, padx=10)

            prompt_window.mainloop()

        elif eval(activation_code["有效期限"].rstrip('天')) - (datetime.now() - datetime.strptime(activation_code['激活时间'], "%Y-%m-%d %H:%M:%S.%f")).days < 0:
            # 剩余有效期小于0天（已经过期）
            prompt_window = tk.Tk()
            prompt_window.geometry('350x80')
            prompt_window.title('激活已到期')
            label1 = tk.Label(prompt_window, text='您的激活码已经到期', font=mid_font)
            label1.pack()
            label2 = tk.Label(prompt_window, text='请联系客服或管理员重新激活', font=mid_font)
            label2.pack()

            def renew():
                prompt_window.destroy()
                login()

            button1 = tk.Button(prompt_window, text='重新激活', font=mid_font, command=renew)
            button1.pack()

            prompt_window.mainloop()

        else:  # 剩余期限大于7天
            import demonstration
    else:  # 验证失败
        login()
except Exception:  # 上面的任何一个环节报错都会要求重新激活
    login()
'''

        pubkey_path = entry1.get().strip().strip('\"').lstrip('“').rstrip('”')
        if os.path.exists(pubkey_path) and '.pem' in pubkey_path:
            with open(pubkey_path, 'rb') as infile, open(f'{dir_of_main_py}\\start.py', 'w', encoding='utf-8') as outfile:
                environment_of_main = text1.get(1.0, 'end').strip('\n')
                environment_items_of_main = environment_of_main.split('\n')
                environment_of_start = '''
import os
import wmi
import time
from datetime import datetime
import base64
import tkinter as tk
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA384
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
import pyperclip'''
                environment_items_of_start = environment_of_start.strip('\n').split('\n')
                res_of_environment_of_main = []
                # res_of_environment_of_main 是去除掉和environment中重复的库后，剩下的
                for main_items in environment_items_of_main:
                    if 'import tkinter' in main_items:
                        ...  # 如果主程序有import tkinter的，就要去掉
                    else:
                        if main_items in environment_items_of_start:
                            ...  # 如果跟start调用一样的库，就去掉
                        else:
                            res_of_environment_of_main.append(main_items)  # 跟start调用不一样的库才用写入
                outfile.write('\n'.join(res_of_environment_of_main))
                # 写完主程序需要的库后，再写启动程序需要的库
                outfile.write(environment_of_start)
                outfile.write(f"\n\n\npubkey_bytes = {str(infile.read())}\n")
                outfile.write(f"contact = \"{entry3.get()}\"\n")
                width_and_height = "404x320" if 'pyautogui' not in text1.get(1.0, 'end') else "606x480"
                outfile.write(f"width_and_height = \"{width_and_height}\"")
                outfile.write(start_code)
        else:
            label5.config(text='')
            messagebox.showerror('路径错误', '公钥的路径不存在')
            return 0

        info_window = tk.Toplevel()
        info_window.title('编译信息显示框')
        info_window.geometry('808x700')
        text2 = tk.Text(info_window, width=88, font=mid_font, height=40)
        text2.pack()
        activate_window.update()

        # 再用 cython 把 py 文件编译成 pyd
        if choice_of_cython.get() == '1':
            text2.insert('end', f'正在使用 Cython 编译 {os.path.basename(main_path)}...\n\n')
            activate_window.update()
            with open('temp_setup.py', 'w', encoding='utf-8') as f:
                f.write('''
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules=cythonize(["demonstration.py"]))  # 这里填要设置的文件名称，方括号里也可以放多个文件名''')
            res = os.popen("python temp_setup.py build_ext")
            try:
                res = res.buffer.read().decode('gbk')
                print(res)
                pyd_path = re.findall('/OUT:.+?\.pyd', res)[0][5:]
            except Exception:
                text2.insert('end', 'Cython 编译结果读取失败，程序结束。')
                label5.config(text='')
                return 0
            # cython 编译结果被正确读取，且正则找到pyd的路径后，才继续
            text2.insert('end', res)
            text2.insert('end', f'''\nCython 编译主程序已完成，
{os.path.basename(main_path)} 的 pyd 文件保存在源码所在目录下，
即“{dir_of_main_py}”文件夹中的 {os.path.basename(pyd_path)} 文件。''')
            activate_window.update()
            with open(pyd_path, 'rb') as infile, open(f'{dir_of_main_py}\\{os.path.basename(pyd_path)}', 'wb') as outfile:
                outfile.write(infile.read())
            os.remove("demonstration.py")
            os.remove("temp_setup.py")
            os.remove(pyd_path)
        else:
            with open('demonstration.py', 'r', encoding='utf-8') as infile, open(f'{dir_of_main_py}\\demonstration.py', 'w', encoding='utf-8') as outfile:
                outfile.write(infile.read())
            text2.insert('end', f'''主程序的源码被复制了一份至主程序所在文件夹下，
即“{dir_of_main_py}”文件夹中的 demonstration.py 文件，
目的是为了让启动程序调用这个 demonstration.py 文件''')

        text2.insert('end', f'''\n\n主程序的启动文件已经生成完成，启动文件保存在源码所在目录下，
即“{dir_of_main_py}”文件夹中的 start.py 文件。\n
注意：启动文件的运行依赖于主程序（原始的py文件或pyd文件都行），两个文件要放于同一目录下。''')
        label5.config(text='加壳完毕，结果保存在源码目录下')

    label1 = tk.Label(frm, text='请输入管理员公钥所在的绝对路径：', font=mid_font)
    label1.pack()
    entry1 = tk.Entry(frm, font=mid_font, width=44)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)
    label2 = tk.Label(frm, text='请输入源码文件的绝对路径：', font=mid_font)
    label2.pack()
    entry2 = tk.Entry(frm, width=44, font=mid_font)
    entry2.pack()
    entry2.bind('<KeyRelease>', read_environment_of_entry2)
    hook_dropfiles(entry2, func=drag2)
    label3 = tk.Label(frm, text='请按照示例写入源码调用的所有环境：', font=mid_font)
    label3.pack()
    text1 = tk.Text(frm, width=44, height=9, font=mid_font)
    text1.pack()
    text1.insert(1.0, '''import binascii
import hashlib
import random
import os
import re
import shutil
from math import ceil
import zlib
from random import randint
from tkinter import messagebox
from tkinter import ttk
from Crypto import Random
from Crypto.Hash import MD4
from Crypto.Hash import RIPEMD160
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Cipher import AES
from windnd import hook_dropfiles
from pynput import keyboard
from threading import Thread''')
    label4 = tk.Label(frm, text='请输入客户联系您的方式：', font=mid_font)
    label4.pack()
    entry3 = tk.Entry(frm, width=44, font=mid_font)
    entry3.pack()
    frm1 = tk.Frame(frm)
    frm1.pack()
    button1 = tk.Button(frm1, text='清空环境', font=mid_font, command=_reset)
    button1.grid(row=1, column=1, padx=10)
    button2 = tk.Button(frm1, text='开始加壳', font=mid_font, command=process)
    button2.grid(row=1, column=2, padx=10)
    choice_of_cython = tk.StringVar()
    choice_of_cython.set('1')
    cb1 = tk.Checkbutton(frm1, text='使用Cython编译原文件', variable=choice_of_cython, onvalue='1', offvalue='0', font=font)
    cb1.grid(row=1, column=3, padx=10)
    label5 = tk.Label(frm, text='', font=mid_font)
    label5.pack()


interval = 25


def intro_pack_main():
    clean_all_widget(frm)
    label1 = tk.Label(frm, text='源码加壳介绍', font=mid_font)
    label1.place(x=200, y=10, anchor='center')
    label2 = tk.Label(frm, text='该功能是在原文件的基础上增加一个启动文件', font=mid_font)
    label2.place(x=10, y=10 + interval * 1, anchor='nw')
    label9 = tk.Label(frm, text="该启动文件具有一机一码的授权激活功能。", font=mid_font)
    label9.place(x=10, y=10 + interval * 2, anchor='nw')
    label3 = tk.Label(frm, text='此外，你还可以选择将原文件进行Cython编译', font=mid_font)
    label3.place(x=10, y=10 + interval * 3, anchor='nw')
    label4 = tk.Label(frm, text="如此，该原文件会变得运行更快且更难破解。", font=mid_font)
    label4.place(x=10, y=10 + interval * 4, anchor='nw')
    label5 = tk.Label(frm, text="不过，你需要在编译前，安装Cython库，", font=mid_font)
    label5.place(x=10, y=10 + interval * 6, anchor='nw')
    label6 = tk.Label(frm, text="方法为：打开cmd，", font=mid_font)
    label6.place(x=10, y=10 + interval * 7, anchor='nw')
    label7 = tk.Label(frm, text="输入 pip install Cython 即可。", font=mid_font)
    label7.place(x=10, y=10 + interval * 8, anchor='nw')
    label8 = tk.Label(frm, text="(end)", font=mid_font)
    label8.place(x=10, y=10 + interval * 9, anchor='nw')


def intro_activation():
    clean_all_widget(frm)
    label1 = tk.Label(frm, text='激活软件介绍', font=mid_font)
    label1.place(x=200, y=10, anchor='center')
    label2 = tk.Label(frm, text='该功能够让你帮助客户激活软件，', font=mid_font)
    label2.place(x=10, y=10 + interval * 1, anchor='nw')
    label3 = tk.Label(frm, text='并设置用户的激活时间。', font=mid_font)
    label3.place(x=10, y=10 + interval * 2, anchor='nw')
    label4 = tk.Label(frm, text='注意，用于激活的私钥，', font=mid_font)
    label4.place(x=10, y=10 + interval * 4, anchor='nw')
    label5 = tk.Label(frm, text='必须和打包时用的公钥配对，', font=mid_font)
    label5.place(x=10, y=10 + interval * 5, anchor='nw')
    label6 = tk.Label(frm, text='否则无法激活。', font=mid_font)
    label6.place(x=10, y=10 + interval * 6, anchor='nw')
    label7 = tk.Label(frm, text='你可以在“创建RSA密钥”处创建RSA密钥对。', font=mid_font)
    label7.place(x=10, y=10 + interval * 8, anchor='nw')
    label8 = tk.Label(frm, text='(end)', font=mid_font)
    label8.place(x=10, y=10 + interval * 9, anchor='nw')


menubar = tk.Menu(activate_window)

'''RSA部分'''
rsa_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='创建RSA密钥', menu=rsa_menu)
rsa_menu.add_command(label='随机生成1024位', command=create_rsa_key_1024, font=font)
rsa_menu.add_command(label='随机生成2048位', command=create_rsa_key_2048, font=font)
rsa_menu.add_command(label='随机生成3072位', command=create_rsa_key_3072, font=font)
rsa_menu.add_command(label='随机生成4096位', command=create_rsa_key_4096, font=font)

'''打包源码部分'''
menubar.add_command(label='源码加壳', command=pack_main)

'''激活软件部分'''
menubar.add_command(label='激活软件', command=activation)

'''帮助部分'''
intro_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='帮助', menu=intro_menu)
intro_menu.add_command(label='源码加壳介绍', command=intro_pack_main, font=font)
intro_menu.add_command(label='激活软件介绍', command=intro_activation, font=font)

activate_window.config(menu=menubar)
activation()

activate_window.mainloop()
