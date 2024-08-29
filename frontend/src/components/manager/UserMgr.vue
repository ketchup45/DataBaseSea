<template>
    <div>
        <div class="header">
            用 户 管 理
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table">
                <el-table-column prop="user_id" label="用户编号" width="200" align="center">
                </el-table-column>
                <el-table-column prop="user_name" label="用户名称" width="200" align="center">
                </el-table-column>
                <el-table-column prop="user_role" label="权限等级" width="200" align="center">
                </el-table-column>
                <el-table-column prop="operate" label="操作" width="200" align="center">
                    <template slot-scope="scope">
                        <el-button size="small" type="warning" @click="dialist_chg(scope.row)">修改权限
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-dialog title="修改权限" :visible.sync="dia_chg" width="30%">
                <el-form ref="form" :model="chg_form" label-width="100px">
                    <el-form-item label="用户编号：">
                        <span>{{ chg_form.user_id }}</span>
                    </el-form-item>
                    <el-form-item label="用户名称：">
                        <span>{{ chg_form.user_name }}</span>
                    </el-form-item>
                    <el-form-item label="权限等级：">
                        <el-select v-model="chg_form.user_role" placeholder="请选择" @change="$forceUpdate()">
                            <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="changeuserrole()">
                        修改
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
            dia_chg: false,
            chg_form: {
                user_id: '',
                user_name: '',
                user_role: '',
                action: "change",
            },
            options: [{
                value: '0',
                label: '0'
                }, {
                value: '1',
                label: '1'
            }],
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/usermgr").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = res.data.tabledata;
                }
            })
        },
        dialist_chg(row) {
            this.chg_form.user_id = row.user_id;
            this.chg_form.user_name = row.user_name;
            this.chg_form.user_role = row.user_role;
            this.dia_chg = true;
        },
        changeuserrole() {
            this.$axios.post("/api/manager/usermgr", this.chg_form).then((res) => {
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