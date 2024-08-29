<template>
    <div>
        <div class="header">
            浮 冰 管 理
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table" border>
                <el-table-column prop="ice_id" label="浮冰编号" width="120" align="center">
                </el-table-column>
                <el-table-column prop="ice_name" label="浮冰名称" width="130" align="center">
                </el-table-column>
                <el-table-column prop="ice_type" label="浮冰类型" width="130" align="center">
                </el-table-column>
                <el-table-column prop="ice_size" label="浮冰面积(m2)" width="130" align="center">
                </el-table-column>
                <el-table-column prop="ice_lasttime" label="最近更新时间" width="170" align="center">
                </el-table-column>
                <el-table-column prop="operate" label="操作" width="200" align="center">
                    <template slot-scope="scope">
                        <el-button size="small" type="warning" @click="dialist_chg(scope.row)">修改
                        </el-button>

                        <el-button size="small" type="danger" @click="dialist_dlt(scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column width="140" align="center">
                    <template slot="header">
                        <el-button icon="el-icon-plus" size="small" type="success" @click="dialist_add()">添加浮冰
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-dialog title="添加浮冰" :visible.sync="dia_add" width="30%">
                <el-form ref="add_form" :model="add_form" label-width="160px" :rules="add_form_rules">
                    <el-form-item label="浮冰名称：" prop="ice_name">
                        <el-input v-model="add_form.ice_name"></el-input>
                    </el-form-item>
                    <el-form-item label="浮冰类型：" prop="ice_type">
                        <el-select v-model="add_form.ice_type" placeholder="请选择" @change="$forceUpdate()">
                            <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="浮冰面积：" prop="ice_size">
                        <el-input v-model="add_form.ice_size"></el-input>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="addice()">
                        添加
                    </el-button>
                </div>
            </el-dialog>

            <el-dialog title="修改浮冰" :visible.sync="dia_chg" width="30%">
                <el-form ref="chg_form" :model="chg_form" label-width="100px" :rules="chg_form_rules">
                    <el-form-item label="浮冰名称：" prop="ice_name">
                        <span>{{ chg_form.ice_name }}</span>
                    </el-form-item>
                    <el-form-item label="浮冰类型：" prop="ice_type">
                        <el-select v-model="chg_form.ice_type" placeholder="请选择">
                            <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="浮冰面积：" prop="ice_size">
                        <el-input v-model="chg_form.ice_size"></el-input>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="changeice()">
                        修改
                    </el-button>
                </div>
            </el-dialog>

            <el-dialog title="删除浮冰" :visible.sync="dia_dlt" width="30%">
                <div>
                    确定删除此浮冰吗？
                </div>
                <div style="text-align: center;">
                    <el-button type="primary" @click="deleteice()">
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
        var checkIcesize = (rule, value, cb) => {           
            const regDouble = /^\d+(\.\d+)?$/;
            if (regDouble.test(value)) {
                // 合法的数字
                return cb()
            }
            cb(new Error('请输入一个有效的面积数字'));  
        };
        return {
            tableData: [],
            dia_add: false,
            dia_chg: false,
            dia_dlt: false,
            add_form: {
                ice_name: '',
                ice_type: '',
                ice_size: '',
                action: "add",
            },
            chg_form: {
                ice_name: '',
                ice_type: '',
                ice_size: '',
                action: "change",
            },
            chg_form_rules: {
                ice_type:  [{ required: true, message: '必填项', trigger: 'blur' }],
                ice_size:  [{ required: true, message: '必填项', trigger: 'blur' }, { validator: checkIcesize, trigger: 'blur' }],
            },
            add_form_rules: {
                ice_name:  [{ required: true, message: '必填项', trigger: 'blur' }],
                ice_type:  [{ required: true, message: '必填项', trigger: 'blur' }],
                ice_size:  [{ required: true, message: '必填项', trigger: 'blur' }, { validator: checkIcesize, trigger: 'blur' }],
            },
            options: [{
                value: '桌状冰山',
                label: '桌状冰山'
                }, {
                value: '尖顶冰山',
                label: '尖顶冰山'
                }, {
                value: '岛状冰山',
                label: '岛状冰山'
            }],
            want_delete: '',
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/icemgr").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = res.data.tabledata;
                }
            })
        },
        dialist_add() {
            this.dia_add = true;
        },
        addice() {
            this.$refs.add_form.validate(valid => {
                if (!valid)
                    return;
                else //验证通过再发送请求
                    this.$axios.post("/api/manager/icemgr", this.add_form).then((res) => {
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
        //更改
        dialist_chg(row) {
            this.chg_form.ice_name = row.ice_name;
            this.chg_form.ice_type = row.ice_type;
            this.chg_form.ice_size = row.ice_size;
            this.dia_chg = true;
        },
        changeice() {
            this.$refs.chg_form.validate(valid => {
                if (!valid)
                    return;
                else //验证通过再发送请求
                    this.$axios.post("/api/manager/icemgr", this.chg_form).then((res) => {
                        console.log(res.data);
                        if (res.data.status == 200) {
                            this.$message({
                            message: "修改成功",
                            type: "success"
                            })
                        this.dia_chg = false;
                        this.getdata();
                        }
                    })
            })
            
        },
        //删除
        dialist_dlt(row) {
            this.want_delete = row.ice_name;
            this.dia_dlt = true;
        },
        deleteice() {
            this.$axios.delete("/api/manager/icemgr", { data: { want_delete: this.want_delete } }).then((res) => {
                console.log(res.data);
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