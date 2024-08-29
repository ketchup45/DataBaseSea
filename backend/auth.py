import jwt
import datetime

# 全局密钥
secret = 'seaicetest'  #自定义密钥

# 生成token
def encode_func(user):
    # user = {'user_id': data[0], 'username': data[1], 'password': data[2], "role": data[3]}
    dic = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
        'iat': datetime.datetime.now() - datetime.timedelta(days=1),  # 开始时间
        'iss': 'sishengyu',  # 签发者
        'data': user
    }
    encoded = jwt.encode(dic, secret, algorithm='HS256')
    return encoded


# 解析token
def decode_func(token):
    decode = jwt.decode(token, secret, issuer='sishengyu', algorithms=['HS256'])
    # 返回解码出来的data
    return decode['data']

def get_token_userid(token):
    data = decode_func(token)
    userid = data['user_id']
    return (userid)

def get_token_userrole(token):
    data = decode_func(token)
    userrole = data['role']
    return (userrole)