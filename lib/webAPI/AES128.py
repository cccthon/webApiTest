import base64
import time
import re

from Crypto.Cipher import AES

# var m = null;
# if(message.indexOf(':websms:')!==-1){
#     m = message.substring(0, message.indexOf(':websms:'));
# }else{
#     m = message;
# }
# var ug = window.navigator.userAgent;
# ug = ug.replace(/ /ig, '');
# m = m + '::websms::'+ ug;
# var fb = (new _fmfp()).get()+'';
# return {
#     cp: selectCipherStrategy(fb).encrypt(cipher, m, fb+key, cfg).toString(),
#     ts: fb
# };


# str不是16的倍数那就补足为16的倍数
def add_to_32(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


key = '25800920791526289422617'  # 密码
# key = key + str(time.time())

print('key:',key)

mobile = '13794829675'  # 待加密文本

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3287.0 Safari/537.36'

strinfo = re.compile(' ')
a = strinfo.sub('',user_agent)

mobile = '13746534562::websms::Mozilla/5.0(Macintosh;IntelMacOSX10_11_6)AppleWebKit/537.36(KHTML,likeGecko)Chrome/65.0.3287.0Safari/537.36'
print('mobile:', mobile)

cryptor = AES.new(add_to_32(key), AES.MODE_ECB)  # 初始化加密器
cpt = cryptor.encrypt(add_to_32(mobile))
cpt1 = base64.encodebytes(cpt)
cpt2 = str(cpt1)
# ciphertext = str(base64.encodebytes(), encoding='utf-8').replace('\n', '')  # 执行加密并转码返回bytes

print(cpt)
print(cpt1)
print(cpt2)



# from base64 import b64encode
# from Crypto.Cipher import AES
#
#
# def getaespwd(key, value):
#     text = value
#     padding = '\0'
#
#     cryptor = AES.new(key, AES.MODE_CBC, padding * 16)
#     # cryptor = AES.new(key, AES.MODE_CBC, b'0000000000000000')
#     # cryptor = AES.new(key, AES.MODE_CBC, b'0000000000000000')
#     length = 16
#     count = len(text)
#     if count < length:
#         add = (length - count)
#         text += (chr(add) * add)
#
#     ciphertext = cryptor.encrypt(text)
#     return b64encode(ciphertext)
#
#
# key = "15019999"  # 秘钥
# value = "123456"  # 被加密字符
# aes128string = getaespwd(key, value)
