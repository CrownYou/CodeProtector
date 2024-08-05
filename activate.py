# coding: utf-8
# @Author: Crown You
import base64
import os
import sys
from datetime import datetime
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature

r'''此程序专供服务器自动生成激活码使用
调用方式：python activate.py <管理员私钥地址> <用户身份标识符> <期限，整型，单位：天>
如果要设定期限为永久，请将期限设定为0
结果输出在activate.py所在文件夹中的activation_code.txt中
如果生成失败，activation_code.txt的内容将为"0"

在cmd中的使用示例：
python activate.py "D:\MyProjects\3.9Program\CodeProtector\keys\private_key_104.pem" BFEBFBFF000806EC 0'''


def activate(prikey_path, user_id, time_limit):
    outpath = 'activation_code.txt'

    def output_0_to_outpath():
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write('0')
        print('激活码生成失败')

    try:
        time_limit = eval(time_limit)
        assert isinstance(time_limit, int)
    except Exception:
        output_0_to_outpath()
        return 0

    # 先处理用于签名的私钥
    key_path = prikey_path.strip().strip('\"').strip('“').rstrip('”')
    if os.path.exists(key_path) and '.pem' in key_path:
        with open(key_path, 'rb') as keyfile:
            p = keyfile.read()
        try:
            key = RSA.importKey(p)
            if bytes("-----BEGIN RSA PRIVATE KEY-----".encode('utf-8')) in p:
                privkey_signer = PKCS1_signature.new(key)
            else:
                output_0_to_outpath()
                return 0
        except Exception:
            output_0_to_outpath()
            return 0
    else:
        output_0_to_outpath()
        return 0
    # 再将要签名的文字变为哈希，注意这里要签名的内容为 用户身份标识符 + 激活时间 + 有效期
    activation_code = {"激活时间": str(datetime.now()), "有效期限": ..., "数字签名": ...}
    activation_code["有效期限"] = str(time_limit) + '天' if time_limit > 0 else '永久'
    hasher = SHA384.new()
    hasher.update('/'.join([user_id, activation_code["激活时间"], activation_code["有效期限"]]).encode('utf-8'))
    # 最后进行签名
    try:
        signature = base64.b64encode(privkey_signer.sign(hasher))
    except Exception:
        output_0_to_outpath()
        return 0
    activation_code["数字签名"] = str(signature).lstrip("b'").rstrip("'")
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(str(activation_code))
    print('生成成功，激活码在程序所在文件夹中的activation_code.txt里')


activate(sys.argv[1], sys.argv[2], sys.argv[3])
