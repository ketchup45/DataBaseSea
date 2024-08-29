<template>
    <div>
        <div class="header">
            检 测 器 管 理
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table">
                <el-table-column prop="detector_id" label="探测器编号" width="200" align="center">
                </el-table-column>
                <el-table-column prop="detector_name" label="探测器名称" width="200" align="center">
                </el-table-column>
                <el-table-column prop="detector_model" label="探测器型号" width="200" align="center">
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
                        <el-button icon="el-icon-plus" size="small" type="success" @click="dialist_add()">添加探测器
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-dialog title="添加探测器" :visible.sync="dia_add" width="30%">
                <el-form ref="add_form" :model="add_form" label-width="150px" :rules="add_form_rules">
                    <el-form-item label="探测器名称：" prop="detector_name">
                        <el-input v-model="add_form.detector_name"></el-input>
                    </el-form-item>
                    <el-form-item label="探测器型号：" prop="detector_model">
                        <el-input v-model="add_form.detector_model"></el-input>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="adddetector()">
                        添加
                    </el-button>
                </div>
            </el-dialog>

            <el-dialog title="修改探测器" :visible.sync="dia_chg" width="30%">
                <el-form ref="form" :model="chg_form" label-width="100px">
                    <el-form-item label="探测器名称：">
                        <span>{{ chg_form.detector_name }}</span>
                    </el-form-item>
                    <el-form-item label="探测器型号：">
                        <el-input v-model="chg_form.detector_model"></el-input>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="changedetector()">
                        修改
                    </el-button>
                </div>
            </el-dialog>
            <el-dialog title="删除探测器" :visible.sync="dia_dlt" width="30%">
                <div>
                    确定删除此探测器吗？
                </div>
                <div style="text-align: center;">
                    <el-button type="primary" @click="deletedetector()">
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
        return {
            tableData: [],
            dia_add: false,
            dia_chg: false,
            dia_dlt: false,
            add_form: {
                detector_name: '',
                detector_model: '',
                action: "add",
            },
            chg_form: {
                detector_name: '',
                detector_model: '',
                action: "change",
            },
            want_delete: '',
            add_form_rules: {
                detector_name:  [{ required: true, message: '必填项', trigger: 'blur' }],
                detector_model: [{ required: true, message: '必填项', trigger: 'blur' }],
            },
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/user/detector").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = res.data.tabledata;
                }
            })
        },
        dialist_add() {
            this.dia_add = true;
        },
        adddetector() {
            this.$refs.add_form.validate(valid => {
                if (!valid)
                    return;
                else //验证通过再发送请求
                    this.$axios.post("/api/user/detector", this.add_form).then((res) => {
                        console.log(res.data);
                        if (res.data.status == 200) {
                            this.$message({
                                message: "添加成功",
                                type: "success"
                            })
                            this.dia_add = false;
                            this.getdata();
                        } 
                        else if (res.data.status == 403) { //Forbidden
                            this.$message({
                                message: res.data.msg,
                                type: "error"
                            })
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
        dialist_chg(row) {
            this.chg_form.detector_name = row.detector_name;
            this.chg_form.detector_model = row.detector_model;
            this.dia_chg = true;
        },
        changedetector() {
            this.$axios.post("/api/user/detector", this.chg_form).then((res) => {
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
        },
        dialist_dlt(row) {
            this.want_delete = row.detector_name;
            this.dia_dlt = true;
        },
        deletedetector() {
            this.$axios.delete("/api/user/detector", { data: { want_delete: this.want_delete } }).then((res) => {
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