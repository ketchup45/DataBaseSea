from flask import Flask, jsonify, request
from sqlalchemy import text

from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig #数据库配置

from datetime import datetime

# 跨域
from flask_cors import cross_origin
from flask_cors import CORS

import auth #token

app = Flask(__name__)

# 添加配置数据库
app.config.from_object(BaseConfig)
# 初始化拓展,app到数据库的ORM映射
db = SQLAlchemy(app)

# 检查数据库连接是否成功
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())



# 用户登录
@app.route("/api/user/login", methods=["POST"])
@cross_origin()
def login():
    print(request.json)
    username = request.json.get("username").strip()
    password = request.json.get("password").strip()
    sql = ('select * '
           + 'from user '
           + 'where user_name = "{0}" and password = "{1}"').format(username, password)
    data = db.session.execute(text(sql)).first()
    if data != None:
        user = {'user_id': data[0], 'username': data[1], 'password': data[2], "role": data[3]}
        # 生成token
        token = auth.encode_func(user)
        return jsonify({"code": 200, "msg": "登录成功", "role": data[3], "token": token})
    else:
        return jsonify({"code": 1000, "msg": "用户名或密码错误"})


#用户注册__检测验证码和手机是否在数据库中
@app.route("/api/user/register", methods=["POST"])
@cross_origin()
def register():
    rq = request.json
    # 获取验证码和手机号
    username = rq.get("username")
    password = rq.get("password")
    #检查是否存在
    data = db.session.execute(text('select * from user where user_name="%s"' % username)).fetchall()
    if not data:
        db.session.execute(text('insert into user(user_name,password,role) value("%s","%s",0)' % (username, password)))
        db.session.commit() #保存更改
        return jsonify({"status": "200", "msg": "注册成功"})
    else:
        return jsonify({"status": "1000", "msg": "该用户已存在"})

# 用户界面搜索浮冰相关信息
@app.route("/api/user/search", methods=["POST", "GET"])
@cross_origin()
def user_search():
    #搜索
    if request.method == 'POST':
        # 根据用户id找到所有的检测器，从而找到所有对应的记录
        rq = request.json  # 接收信息
        ice_id = rq.get('ice_id')
        start_time = rq.get('start_time')
        end_time = rq.get('end_time')
        icedata = db.session.execute(text('select * from ice where ice_id = %s' % ice_id)).fetchall()
        if not icedata:
            return jsonify(status=406, msg="该浮冰不存在")
        else:
            iceData = dict(ice_name=icedata[0][1], ice_type=icedata[0][2], ice_size=icedata[0][3])
        #分别赋值，实现合并不同情况
        if not start_time:
            start_time = "1000-01-01 12:00:00"
        if not end_time:
            end_time = "3000-01-01 12:00:00"
        if datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") >= datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"):
            return jsonify(status=407, msg="起始时间应早于结束时间")
        recdata = db.session.execute(text('select * from record where ice_id = %s\
                                        AND record_time BETWEEN "%s" AND "%s" ORDER BY record_time'
                                        % (ice_id, start_time, end_time))).fetchall()
        if not recdata:
            return jsonify(status=408, msg="该时间段内不存在记录")
        else:
            coordData=[] = []
            for i in range(len(recdata)):
                dic = dict(latitude=recdata[i][3], longtitude=recdata[i][4])
                coordData.append(dic)
            return jsonify(status=200, tabledata=iceData, coorddata=coordData, msg="查询成功")



# 用户界面管理检测器相关信息
@app.route("/api/user/detector", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_detector():
    userid = auth.get_token_userid(request.headers.get('token'))  # 获取用户id
    userrole = auth.get_token_userrole(request.headers.get('token'))  # 获取用户role
    # 获取检测器信息
    if request.method == 'GET':
        data = db.session.execute(text('select * from detector where user_id = %d' % userid)).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(detector_id=data[i][0], detector_name=data[i][1], detector_model=data[i][2])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    #添加
    if request.method == 'POST' and request.json.get('action') == "add":
        if userrole == 0:
            return jsonify(status=403, msg="您的执行权限不足")
        rq = request.json #接收信息
        detector_name = rq.get('detector_name')
        detector_model = rq.get('detector_model')
        exist = db.session.execute(text('select * from detector where detector_name="%s"' % detector_name)).fetchall()
        if not exist: #不存在
            db.session.execute(text('insert detector(detector_name,detector_model,user_id) value("%s","%s",%d)'
                % (detector_name, detector_model,userid)))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该探测器已存在")
    if request.method == 'POST' and request.json.get('action') == "change":
        rq = request.json
        detector_name = rq.get('detector_name')
        detector_model = rq.get('detector_model')
        db.session.execute(text('update detector set detector_model="%s" where detector_name="%s"'
                                % (detector_model, detector_name)))
        db.session.commit()
        return jsonify(status=200, msg="修改成功")
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        db.session.execute(text('delete from detector where detector_name="%s"' % want_delete))
        db.session.commit()
        return jsonify(status=200, msg="删除成功")



# 用户界面管理检测器相关信息
@app.route("/api/user/record", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_record():
    userid = auth.get_token_userid(request.headers.get('token'))  # 获取用户id
    userrole = auth.get_token_userrole(request.headers.get('token'))  # 获取用户role
    # 获取浮冰记录信息
    if request.method == 'GET':
        #根据用户id找到所有的检测器，从而找到所有对应的记录
        textcmd = text("SELECT r.*\
                        FROM record r JOIN detector d ON d.detector_id = r.detector_id\
                        WHERE d.user_id = %d\
                        ORDER BY record_id" % userid)
        data = db.session.execute(textcmd).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(record_id=data[i][0], ice_id=data[i][1], detector_id=data[i][2],
                       latitude=data[i][3], longtitude=data[i][4], record_time=(data[i][5].strftime("%Y-%m-%d %H:%M:%S")))
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    #添加
    if request.method == 'POST' and request.json.get('action') == "add":
        #403权限不足
        if userrole == 0:
            return jsonify(status=403, msg="您的执行权限不足")
        rq = request.json #接收信息
        ice_id= rq.get('ice_id')
        detector_id = rq.get('detector_id')
        latitude = rq.get('latitude')
        longtitude = rq.get('longtitude')
        # 406检测器不存在
        tcmd1 = text(('select * from detector where detector_id=%s' % detector_id))
        res1 = db.session.execute(tcmd1).fetchall()
        if not res1:
            return jsonify(status=406, msg="该检测器不存在")
        # 407该检测器不属于当前用户
        tcmd2 = text(('select * from detector where detector_id=%s and user_id=%d' % (detector_id, userid)))
        res2 = db.session.execute(tcmd2).fetchall()
        if not res2:
            return jsonify(status=407, msg="该检测器不属于您")
        # 408浮冰不存在
        tcmd3 = text(('select * from ice where ice_id=%s' % ice_id))
        res3 = db.session.execute(tcmd3).fetchall()
        if not res3:
            return jsonify(status=408, msg="该浮冰不存在")
        #成功添加
        current_date = datetime.now()
        db.session.execute(text('insert record(ice_id,detector_id,latitude,longtitude,record_time) value(%s,%s,%s,%s,"%s")'
                                % (ice_id,detector_id,latitude,longtitude,current_date.strftime("%Y-%m-%d %H:%M:%S"))))
        db.session.commit()
        #把这个记录的id赋值给浮冰对应的最新id
        tcmd4 = text(('SELECT record_id FROM record\
                       WHERE ice_id = %s AND detector_id = %s\
                       ORDER BY record_time DESC\
                       LIMIT 1' % (ice_id, detector_id)))
        newrecid = db.session.execute(tcmd4).fetchall()
        db.session.execute(text('update ice set record_id=%s where ice_id=%s'
                                % (newrecid[0][0], ice_id)))
        db.session.commit()
        return jsonify(status=200, msg="添加成功")
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        db.session.execute(text('delete from record where record_id=%s' % want_delete))
        db.session.commit()
        return jsonify(status=200, msg="删除成功")


@app.route("/api/user/userinfo", methods=["POST", "GET"])
@cross_origin()
def user_userinfo():
    userid = auth.get_token_userid(request.headers.get('token'))
    if request.method == 'GET':
        data = db.session.execute(text('select * from user where user_id=%s' % userid)).fetchall()
        if data:
            return jsonify(status=200, user_name=data[0][1])
        else:
            return jsonify(status=404, message="User not found")#, 404
    if request.method=='POST':
        print("******************")
        new_pwd=request.json.get('new_pwd')
        old_pwd=request.json.get('old_pwd')
        print("old_pwd")
        data = db.session.execute(text('select * from user where user_id=%s and password="%s"'% (userid,old_pwd))).fetchall()
        if not data:
            return jsonify(status=1000,msg="原始密码错误")
        else:
            db.session.execute(text('update user set password="%s" where user_id=%s'% (new_pwd,userid)))
            db.session.commit()
            return jsonify(status=200,msg="修改成功")


# 管理员进行用户管理
@app.route("/api/manager/usermgr", methods=["POST", "GET"])
@cross_origin()
def manager_usermgr():
    # 获取检测器信息
    if request.method == 'GET':
        #查询所有用户
        data = db.session.execute(text('select * from user where role != 2')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(user_id=data[i][0], user_name=data[i][1], user_role=data[i][3])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    #修改权限
    if request.method == 'POST' and request.json.get('action') == "change":
        rq = request.json
        user_name = rq.get('user_name')
        user_role = rq.get('user_role')
        db.session.execute(text('update user set role=%s where user_name="%s"'
                                % (user_role, user_name)))
        db.session.commit()
        return jsonify(status=200, msg="修改成功")


# 管理员进行浮冰管理
@app.route("/api/manager/icemgr", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_icemgr():
    # 获取浮冰信息
    if request.method == 'GET':
        icedata = db.session.execute(text('select * from ice')).fetchall()
        Data = []
        for i in range(len(icedata)):
            dic = dict(ice_id=icedata[i][0], ice_name=icedata[i][1], ice_type=icedata[i][2], ice_size=icedata[i][3])
            recordid = icedata[i][4]  #获取最近的记录信息
            if recordid: #如果存在的话
                recorddata = db.session.execute(text('select * from record where record_id = %d' % recordid)).fetchall()
                dic.update({"ice_lasttime":recorddata[0][5].strftime("%Y-%m-%d %H:%M:%S")})
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    # 添加
    if request.method == 'POST' and request.json.get('action') == "add":
        rq = request.json  # 接收信息
        ice_name = rq.get('ice_name')
        ice_type = rq.get('ice_type')
        ice_size = rq.get('ice_size')
        exist = db.session.execute(text('select * from ice where ice_name="%s"' % ice_name)).fetchall()
        if not exist:  # 不存在
            db.session.execute(text('insert ice(ice_name,ice_type,ice_size) value("%s","%s",%s)'
                                    % (ice_name, ice_type, ice_size)))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该浮冰已存在")
    if request.method == 'POST' and request.json.get('action') == "change":
        rq = request.json
        ice_name = rq.get('ice_name')
        ice_type = rq.get('ice_type')
        ice_size = rq.get('ice_size')
        db.session.execute(text('update ice set ice_type="%s",ice_size=%s where ice_name="%s"'
                                % (ice_type, ice_size, ice_name)))
        db.session.commit()
        return jsonify(status=200, msg="修改成功")
    if request.method == 'DELETE':
        print("yes")
        want_delete = request.json.get('want_delete')
        db.session.execute(text('delete from ice where ice_name="%s"' % want_delete))
        db.session.commit()
        return jsonify(status=200, msg="删除成功")




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000')
    # 开启了debug模式