<template>
    <div class="container">
        <div class="login_box" v-show="target == 1">
            <div class="head" style="color: #000080">
                浮冰位置记录系统
            </div>
            <!-- 登录 -->
            <div>
                <el-form label-width="0" class="login_form" :model="login_form" :rules="login_rules" ref="login_form">
                    <!-- 用户名 -->
                    <el-form-item prop="username">
                        <el-input v-model="login_form.username" spellcheck="false" placeholder="用户名">
                        </el-input>
                    </el-form-item>
                    <!-- 密码 -->
                    <el-form-item prop="password">
                        <el-input v-model="login_form.password" show-password spellcheck="false" placeholder="密码">
                        </el-input>
                    </el-form-item>


                    <!-- 按钮 -->
                    <el-form-item class="btns">
                        <el-button type="primary" @click="mylogin()">登录</el-button>
                    </el-form-item>

                </el-form>
                <div>
                    <div class="operate">
                        <span id="op1" @click="change(2)">注册</span>
                        <!-- <span id="op2" @click="change(3)">忘记密码</span> -->
                    </div>
                </div>
            </div>
        </div>   

        <!-- 注册表单 -->
        <div class="reg_box" v-show="target == 2">
            <div class="head" style="color: #000080">
                浮冰位置记录系统
            </div>
            <div>
                <el-form class="reg_form" :model="reg_form" :rules="reg_rules" ref="reg_form">
                    <!-- 用户名 -->
                    <el-form-item prop="username">
                        <el-input prefix-icon="iconfont icon-user" v-model="reg_form.username" spellcheck="false"
                            placeholder="用户名">
                        </el-input>
                    </el-form-item>
                    <!-- 密码 -->
                    <el-form-item prop="password">
                        <el-input prefix-icon="iconfont icon-password" v-model="reg_form.password" show-password
                            spellcheck="false" placeholder="密码"></el-input>
                    </el-form-item>

                    <!-- 按钮 -->
                    <el-form-item class="btns">
                        <el-button type="primary" @click="myregister()">注册</el-button>
                    </el-form-item>

                </el-form>
                <div>
                    <div>
                        <span @click="change(1)"
                            style="margin-left:210px;color: #000;opacity: .5;font-weight: 400;font-size: 16px;cursor:pointer;">登录</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MyLogin',
    data() {
        return {
            target: 1,
            //登录
            login_form: {
                username: '',
                password: ''
            },
            login_rules: {
                username: [ { required: true, message: '请输入用户名', trigger: 'blur' }],
                password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
            }, 
            //注册
            reg_form: {
                username: '',
                password: ''
            },
            reg_rules: {
                username: [{ required: true, message: '请设置用户名', trigger: 'blur' }],
                password: [{ required: true, message: '请设置密码', trigger: 'blur' }]
            }, 
        }
    },
    methods: {
        change(id) {
            this.target = id;
        },
        mylogin() {
            this.$refs.login_form.validate(valid => {
                if (!valid)
                    return;
                else //验证通过再发送请求
                    this.login();
            })
        },
        async login() {

            this.$axios.post("/api/user/login", this.login_form).then((res) => {
                console.log(res.status);
                //200登录成功
                if (res.data.code != 200) {
                    return this.$message({
                        message: res.data.msg,
                        type: 'error '
                    })
                } else {
                    this.$message({
                        message: '登录成功',
                        type: 'success'
                    })

                    //储存token
                    window.localStorage.setItem("token", res.data.token);
                    
                    //转到路由定义的其他网页
                    if (res.data.role == 2)
                        this.$router.push('/manager')
                    else
                        this.$router.push('/user')
                }
            }).catch(() => {
                // console.log(res.response.data);
                this.$message({
                    message: "网络故障",
                    type: 'error'
                })
            })

        },
        //注册
        myregister(){
            this.$refs.reg_form.validate(valid => {
                if (!valid)
                    return;
                else{
                    this.$axios.request({
                            method:'POST',
                            url:'/api/user/register',
                            data:{
                                username:this.reg_form.username,
                                password:this.reg_form.password,
                            }
                    }).then((res)=>{
                            // console.log(res.status);
                            if(res.data.status==200)
                            {
                                this.$message({
                                message: '注册成功',
                                type: 'success'
                                })
                                this.target = 1;
                                // 页面变为登录页面
                            }
                            else{
                                this.$message({
                                message: res.data.msg,
                                type: 'error'
                                }) 
                            }         
                    })
                }
            })
        },
    }
}
</script>

<style lang="less" scoped>
.container {
    background-color: #8ba9c7;
    height: 100%;
    width: 100%;
}

.head {
    text-align: center;
    height: 80px;
    line-height: 50px;
    font-size: larger;
}

.login_box {
    height: 350px;
    width: 450px;
    background-color: white;
    border-radius: 3px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.reg_box {
    height: 350px;
    width: 450px;
    background-color: white;
    border-radius: 3px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.input {
    width: 350px;
    height: 50px;
    margin-left: 50px;
}

.el-form-item {
    width: 350px;
    margin-left: 50px;
}

.btns {
    text-align: center;
}

.operate {
    text-align: center;
    color: #000;
    opacity: .5;
    font-weight: 400;
    font-size: 16px;
    //margin-left: 28px;
}

#op1 {
    padding-left: 15px;
    padding-right: 15px;
    text-align: center;
    //border-right: 1px solid #bdb9b9;
    cursor: pointer;
}

#op2 {
    padding-left: 30px;
    padding-right: 15px;
    //border-right: 1px solid #bdb9b9;
    cursor: pointer;
}
</style>