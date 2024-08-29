<template>
    <div>
        <div class="header">
            浮 冰 位 置 记 录 系 统
        </div>
        <div class="body">
            <!-- 左侧导航栏 -->
            <div class="liner">
                <el-menu default-active="1" class="el-menu-vertical-demo" background-color="#6a8cae" text-color="#fff"
                    active-text-color="#ffd04b" @select="handleselect">
                    <el-menu-item index="1">
                        <i class="el-icon-search"></i>
                        <span slot="title">搜索浮冰</span>
                    </el-menu-item>

                    <el-submenu index="2">
                        <template slot="title">
                            <i class="el-icon-files"></i>
                            <span>数据管理</span>
                        </template>
                        <el-menu-item-group>
                            <el-menu-item index="3">检测器</el-menu-item>
                            <el-menu-item index="4">浮冰记录</el-menu-item>
                        </el-menu-item-group>

                    </el-submenu>

                    <el-menu-item index="5">
                        <i class="el-icon-s-home"></i>
                        <span slot="title">个人中心</span>
                    </el-menu-item>

                </el-menu>
            </div>
            <div class="main">
                <div id="usershop" v-show="active == 1">
                    <searchice></searchice>
                </div>

                <div id="detectormanage" v-show="active == 3">
                    <detectormanage></detectormanage>
                </div>

                <div id="recordmanage" v-show="active == 4">
                    <recordmanage></recordmanage>
                </div>

                <div id="userinformation" v-show="active == 5">
                    <userinformation></userinformation>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import searchice from '@/components/user/SearchIce.vue'
import detectormanage from '@/components/user/DetrMgr.vue'
import recordmanage from '@/components/user/RecdMgr.vue'
import userinformation from '@/components/user/UserInfo.vue'
export default {
    components: {
        searchice: searchice,
        detectormanage: detectormanage,
        recordmanage: recordmanage,
        userinformation: userinformation,
    },
    data() {
        return {
            active: 1,
        };
    },
    methods: {
        handleselect(index) {
            this.active = index;
        }
    },
}  
</script>

<style scoped>
.header {
    width: 100%;
    height: 10vh;
    text-align: center;/* 水平居中 */
    line-height: 10vh;
    font-size: 25px;
    font-weight: 800;
    background-color: #207f786f;
    /* padding-left: 100px; */
}

.body {
    width: 100%;
    height: 650px;
    display: flex;
    justify-content: space-around;
}

.liner {
    width: 15%;
    height: 100%;
    background-color: #6a8cae;
}

.main {
    width: 85%;
}
</style>