<template>
    <div>
        <div class="header">
            搜 索 浮 冰
        </div>
        <div class="body">
            <el-form :inline="true" :model="search_form" size="small" ref="search_form" class="demo-form-inline" 
                     :rules="search_form_rules" style="width: 1000px; margin-top: -20px;">

                <el-form-item label="浮冰编号" prop="ice_id" style="margin-left:-100px">
                    <el-input v-model="search_form.ice_id" placeholder="浮冰编号"></el-input>
                </el-form-item>

                <el-form-item label="记录时间">
                    <el-form-item prop="start_time">
                        <el-date-picker v-model="search_form.start_time" type="datetime" placeholder="开始时间" 
                            value-format="yyyy-MM-dd HH:mm:ss" default-time="12:00:00">
                        </el-date-picker>
                    </el-form-item>
                    至&nbsp;&nbsp;
                    <el-form-item prop="end_time">
                        <el-date-picker v-model="search_form.end_time" type="datetime" placeholder="结束时间" 
                            value-format="yyyy-MM-dd HH:mm:ss" default-time="12:00:00">
                        </el-date-picker>
                    </el-form-item>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="searchice()">查询</el-button>
                    <el-button @click="resetform()">重置</el-button>
                </el-form-item>
            </el-form>

            <div v-show="suc_srch">
                <el-form :inline="true" style="width: auto; margin-left:-100px" class="table" border>
                    <el-form-item label="浮冰名称：" prop="ice_name">
                        <span style="border:solid;border-radius: 2px;border-color:aqua;">&nbsp;{{ ice_name }}&nbsp;</span>
                    </el-form-item>
                    <el-form-item label="浮冰类型：" prop="ice_type">
                        <span style="border:solid;border-radius: 2px;border-color:aqua;">&nbsp;{{ ice_type }}&nbsp;</span>
                    </el-form-item>
                    <el-form-item label="浮冰面积：" prop="ice_size">
                        <span style="border:solid;border-radius: 2px;border-color:aqua;">&nbsp;{{ ice_size }}&nbsp;</span>
                    </el-form-item>
                </el-form>
            </div>
            
            <!-- 高德地图 -->
            <div id="container"></div>
        </div>
    </div>
</template>
  
<script>
import AMapLoader from "@amap/amap-jsapi-loader"
//import AMap from "Amap"
export default {
    //高德地图
    name: "map-view",
    mounted() {
        this.initAMap();
    },
    unmounted() {
        this.map?.destroy();
    },
    //
    data() {
        var CheckInt = (rule, value, cb) => {           
            const regInt = /^\d+$/;
            if (regInt.test(value)) {
                return cb()
            }
            cb(new Error('请输入一个有效的数字'));  
        };
        return {
            suc_srch: false, //查询成功
            ice_name: '',
            ice_type: '',
            ice_size: '',
            search_form: {
                ice_id: '',
                start_time: '',
                end_time: '',
            },
            search_form_rules: {
                ice_id:  [{ required: true, message: '必填项', trigger: 'blur' }, { validator: CheckInt, trigger: 'blur' }],
            },
            //高德地图
            myAmap: null,
            polyline: null,
            path: [],
            startmarker: null,
            endmarker: null,
            cneter: null,
            circleMarker: null,
        }
    },
    methods: {
        searchice() {
            this.$refs.search_form.validate(valid => {
                if (!valid)
                    return;
                else
                    this.$axios.post("/api/user/search", this.search_form).then((res) => {
                        console.log(res.data);
                        if (res.data.status == 200) {
                            this.$message({
                                message: "查询成功",
                                type: "success"
                            })
                            this.ice_name=res.data.tabledata.ice_name;
                            this.ice_type=res.data.tabledata.ice_type;
                            this.ice_size=res.data.tabledata.ice_size;
                            this.suc_srch = true;
                            //显示路线
                            this.showPath(res);
                        }
                        else {
                            this.$message({
                                message: res.data.msg,
                                type: "error"
                            })
                            this.suc_srch = false;
                        }
                    })
            })
        },
        resetform() {
            if(this.$refs.search_form != undefined){
                this.$refs.search_form.resetFields();
                this.suc_srch = false;
                this.myAmap.clearMap()
            }
        },

        //高德地图api
        initAMap() {
            window._AMapSecurityConfig = {
                securityJsCode: "5558753d6f93318d89ccfeec3d31c873",
            };
            AMapLoader.load({
                key: "ab415f4935843c97d62642865f5102b4", // 申请好的Web端开发者Key，首次调用 load 时必填
                version: "2.0", // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
                plugins: ["AMap.PolylineEditor"], //需要使用的的插件列表，如比例尺'AMap.Scale'，支持添加多个如：['...','...']
            })
            .then((AMap) => {
                this.myAmap = new AMap.Map("container", {
                    // 设置地图容器id
                    viewMode: "3D", // 是否为3D地图模式
                    layers: [new AMap.TileLayer.Satellite()],
                    zoom: 1, // 初始化地图级别
                    center: [116.397428, 39.90923], // 初始化地图中心点位置
                });
            })
            .catch((e) => {
                console.log(e);
            });         
        },
        async showPath(res) {
            // 查询前先清空历史
            this.lineList = []
            this.path = []
            this.myAmap.clearMap()
            //配置折线路径
            let lastone = res.data.coorddata.length - 1
            for (let i = 0; i < lastone; i++) {
                var path = [
                    //两个点
                    new window.AMap.LngLat(parseFloat(res.data.coorddata[i].longtitude), parseFloat(res.data.coorddata[i].latitude)),
                    new window.AMap.LngLat(parseFloat(res.data.coorddata[i+1].longtitude), parseFloat(res.data.coorddata[i+1].latitude))
                ]
                //创建 Polyline 实例
                var polyline = new window.AMap.Polyline({
                    path: path,
                    strokeWeight: 5,
                    strokeColor: 'red',
                    lineJoin: 'round' // 折线拐点连接处样式
                })
                this.myAmap.add(polyline)
            }
            //创建点标记
            var startmarker = new window.AMap.Marker({
                position: new window.AMap.LngLat(res.data.coorddata[0].longtitude, res.data.coorddata[0].latitude), //经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
                title: "起点",
            });
            this.myAmap.add(startmarker);

            var endmarker = new window.AMap.Marker({
                position: new window.AMap.LngLat(res.data.coorddata[lastone].longtitude, res.data.coorddata[lastone].latitude), //经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
                title: "终点",
            });
            this.myAmap.add(endmarker);

            //中间点标记
            for (let i = 1; i < lastone; i++) {
                var center = new window.AMap.LngLat(res.data.coorddata[i].longtitude, res.data.coorddata[i].latitude);
                var circleMarker = new window.AMap.CircleMarker({
                    center: center, //圆心
                    radius: 6, //半径
                    fillColor: "rgba(0,255,255,1)", //多边形填充颜色
                    fillOpacity: 1, //多边形填充透明度
                    zIndex: 10, //多边形覆盖物的叠加顺序
                    cursor: "pointer", //鼠标悬停时的鼠标样式
                });
                this.myAmap.add(circleMarker)
            }
        }
    },
    
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
    width: 62%;
    margin: auto;
    margin-top: 30px;
  }

  .table {
    font-weight: 800;
    margin-top: -30px;
  }

  #container {
  margin-top: -15px;
  width: 100%;
  height: 470px;
  }
</style> 
