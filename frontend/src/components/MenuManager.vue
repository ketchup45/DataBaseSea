<template>
    <div>
        <div class="header">
            浮 冰 位 置 记 录 系 统
        </div>
        <div class="body">
            <div class="liner">
                <el-menu default-active="1" class="el-menu-vertical-demo" background-color="#6a8cae" text-color="#fff"
                    active-text-color="#ffd04b" @select="handleselect">

                    <el-menu-item index="1">
                        <i class="el-icon-location"></i>
                        <span slot="title">浮冰管理</span>
                    </el-menu-item>

                    <el-menu-item index="2">
                        <i class="el-icon-s-custom"></i>
                        <span slot="title">用户管理</span>
                    </el-menu-item>
                </el-menu>
            </div>
            <div class="main">
                <div id="icemanager" v-show="active == 1">
                    <icemanager></icemanager>
                </div>
                <div id="usermanager" v-show="active == 2">
                    <usermanager></usermanager>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import icemanager from '@/components/manager/IceMgr.vue'
import usermanager from '@/components/manager/UserMgr.vue'
export default {
    components: {
        icemanager: icemanager,
        usermanager: usermanager,
    },
    data() {
        return {
            active: 1,
        }
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
    text-align: center;
    line-height: 10vh;
    font-size: 25px;
    font-weight: 800;
    background-color: #c1dde1;
    /* padding-left: 100px; */
}

.body {
    width: 100%;
    height: 648px;
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