<template>
    <div>
        <div class="header">
            浮 冰 位 置 记 录 管 理
        </div>
        <div class="body">
            <el-table :data="tableData" class="table" border>
                <el-table-column prop="record_id" label="记录编号" width="92" align="center">
                </el-table-column>
                <el-table-column prop="ice_id" label="浮冰编号" width="92" align="center">
                </el-table-column>
                <el-table-column prop="detector_id" label="检测器编号" width="103" align="center">
                </el-table-column>
                <el-table-column prop="latitude" label="纬度" width="125" align="center">
                </el-table-column>
                <el-table-column prop="longtitude" label="经度" width="125" align="center">
                </el-table-column>
                <el-table-column prop="record_time" label="上传时间" width="200" align="center">
                </el-table-column>
                <el-table-column prop="operate" label="操作" width="150" align="center">
                    <template slot-scope="scope">
                        <el-button size="small" type="danger" @click="dialist_dlt(scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column width="140" align="center">
                    <template slot="header">
                        <el-button icon="el-icon-plus" size="small" type="success" @click="dialist_add()">添加记录
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-dialog title="添加位置记录" :visible.sync="dia_add" width="30%">
                <el-form ref="add_form" :model="add_form" label-width="150px" :rules="add_form_rules">
                    <el-form-item label="浮冰编号：" prop="ice_id">
                        <el-input v-model="add_form.ice_id"></el-input>
                    </el-form-item>
                    <el-form-item label="检测器编号：" prop="detector_id">
                        <el-input v-model="add_form.detector_id"></el-input>
                    </el-form-item>
                    <el-form-item label="纬度：" prop="latitude">
                        <el-input v-model="add_form.latitude"></el-input>
                    </el-form-item>
                    <el-form-item label="经度：" prop="longtitude">
                        <el-input v-model="add_form.longtitude"></el-input>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="addrecord()">
                        添加
                    </el-button>
                </div>
            </el-dialog>

            <el-dialog title="删除记录" :visible.sync="dia_dlt" width="30%">
                <div>
                    确定删除此记录吗？
                </div>
                <div style="text-align: center;">
                    <el-button type="primary" @click="deleterecord()">
                        确定
                    </el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
export default {
    created() {
        this.getdata()
    },
    data() {
        var CheckLati = (rule, value, cb) => {           
            const regDouble = /^(-?\d+(\.\d{1,6})?)$/; // 假设小数点后最多6位数字  
            // 检查值是否匹配正则表达式  
            if (!regDouble.test(value)) {  
                return cb(new Error('请输入一个有效的数字'));  
            } 
            // 尝试将值转换为浮点数
            const floatValue = parseFloat(value);  
            // 检查是否成功转换为浮点数并且是否在指定范围内  
            if (isNaN(floatValue) || floatValue < -90 || floatValue > 90) {  
                return cb(new Error('请输入一个 -90 至 90 之间的浮点数'));
            }  
            else
                return cb();
        };
        var CheckLong = (rule, value, cb) => {           
            const regDouble = /^(-?\d+(\.\d{1,6})?)$/; // 假设小数点后最多6位数字  
            // 检查值是否匹配正则表达式  
            if (!regDouble.test(value)) {  
                return cb(new Error('请输入一个有效的数字'));  
            } 
            // 尝试将值转换为浮点数
            const floatValue = parseFloat(value);  
            // 检查是否成功转换为浮点数并且是否在指定范围内  
            if (isNaN(floatValue) || floatValue < -180 || floatValue > 180) {   
                return cb(new Error('请输入一个 -180 至 180 之间的浮点数'));  
            }  
            else
                return cb();
        };
        var CheckInt = (rule, value, cb) => {           
            const regInt = /^\d+$/;
            if (regInt.test(value)) {
                return cb()
            }
            cb(new Error('请输入一个有效的数字'));  
        };
        return {
            tableData: [],
            dia_add: false,
            dia_dlt: false,
            add_form: {
                ice_id: '',
                detector_id: '',
                latitude: '',
                longtitude: '',
                action: "add",
            },
            add_form_rules: {
                ice_id:  [{ required: true, message: '必填项', trigger: 'blur' }, { validator: CheckInt, trigger: 'blur' }],
                detector_id: [{ required: true, message: '必填项', trigger: 'blur' }, { validator: CheckInt, trigger: 'blur' }],
                latitude: [{ required: true, message: '必填项', trigger: 'blur' }, { validator: CheckLati, trigger: 'blur' }],
                longtitude: [{ required: true, message: '必填项', trigger: 'blur' }, { validator: CheckLong, trigger: 'blur' }],
            },
            want_delete: '',
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/user/record").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = res.data.tabledata;
                }
            })
        },
        dialist_add() {
            this.dia_add = true;
        },
        addrecord() {
            this.$refs.add_form.validate(valid => {
                if (!valid)
                    return;
                else //验证通过再发送请求
                    this.$axios.post("/api/user/record", this.add_form).then((res) => {
                        console.log(res.data);
                        if (res.data.status == 200) {
                            this.$message({
                                message: "添加成功",
                                type: "success"
                            })
                            this.dia_add = false;
                            this.getdata();
                        } 
                        else {
                            this.$message({
                                message: res.data.msg,
                                type: "error"
                            })
                        }
                    })
            })
        },
        dialist_dlt(row) {
            this.want_delete = row.record_id;
            this.dia_dlt = true;
        },
        deleterecord() {
            this.$axios.delete("/api/user/record", { data: { want_delete: this.want_delete } }).then((res) => {
                if (res.data.status == 200) {
                    this.$message({
                        message: res.data.msg,
                        type: "success"
                    })
                    this.getdata()
                    this.dia_dlt = false;
                }
            })
        }
    }
}
</script>

<style scoped>
.header {
    width: 100%;
    height: 10%;
    text-align: center;
    line-height: 64px;
    font-size: 20px;
    font-weight: 800;
    border-bottom: 1px solid #e3e3e3;
}

.body {
    width: 80%;
    margin: auto;
    margin-top: 30px;
}
</style>