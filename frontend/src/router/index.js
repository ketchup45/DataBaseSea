import Vue from 'vue'
import VueRouter from 'vue-router'
import LogRes from '@/components/MenuLogReg.vue'
import User from '@/components/MenuUser.vue'
import Manager from '@/components/MenuManager.vue'

Vue.use(VueRouter)
export default new VueRouter({
    mode:'history',
    routes: [
        {
            path:'/',
            redirect:'/login'
        },
        {
            path: '/login',
            component: LogRes,
            meta: {
                title: "登录"
            },
        },
        {
            path: '/user',
            component: User,
            meta: {
                title: "用户界面"
            }
        },
        {
            path: '/manager',
            component: Manager,
            meta: {
                title: "管理员界面"
            }
        },
    ]
})