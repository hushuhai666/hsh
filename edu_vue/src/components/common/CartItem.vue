<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_img" alt="">
            <span><router-link to="/course/detail/1">{{course.name}}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option :label="item.expire_text" :value="item.id" :key="item.id"
                           v-for="item in course.expire_list"></el-option>
<!--                <el-option label="2个月有效" value="60" key="60"></el-option>-->
<!--                <el-option label="3个月有效" value="90" key="90"></el-option>-->
<!--                <el-option label="永久有效" value="10000" key="10000"></el-option>-->
            </el-select>
        </div>
        <div class="cart_column column_4">¥{{course.real_price}}</div>
        <div class="cart_column column_4" @click="del">删除</div>
    </div>
</template>

<script>
    export default {
        name: "Cartltem",
        props: ['course'],
        data(){
            return{
                expire:0,
                checked:'',
            }
        },
        watch: {
            // 通过监测课程id来切换有效期
            'course.expire_id': function () {
                // 后台发送请求切换状态
                this.change_expire();
            },
            // 通过监测select的变化来改变当前的选中状态
            'course.selected': function () {
                // 后台发送请求切换状态
                this.change_select()
            },
        },
        methods:{

            change_expire() {
                // let token = sessionStorage.token || localStorage.token;
                let token = localStorage.token || sessionStorage.token;
                // console.log(token)
                this.$axios.put("http://127.0.0.1:9000/cart/option/", {
                    course_id: this.course.id,
                    expire_id: this.course.expire_id,
                }, {
                    headers: {
                        // 提交购物车时必须携带token  jwt 后必须跟空格
                        "Authorization": "jwt " + token,
                    }
                }).then(response=>{
                    console.log(response.data);
                    this.course.real_price = response.data.price;

                    // 改变价格
                }).catch(error=>{
                    console.log(error);
                })
            },

            // 状态切换
            change_select() {
                let token = localStorage.token || sessionStorage.token;
                this.$axios.patch("http://127.0.0.1:9000/cart/option/", {
                    selected: this.course.selected,
                    course_id: this.course.id,
                }, {
                    headers: {
                        // 提交token必须在请求头声明token  jwt必须有空格
                        "Authorization": "jwt " + token,
                    }
                }).then(response => {
                    this.$message.success(response.data.message);

                    // 向父组件提交事件 来修改购物车已勾选的课程的总价
                    this.$emit("change_select");

                }).catch(error => {
                    this.$message.error(error.response)
                })
            },



            del() {
                let token = localStorage.token || sessionStorage.token;
                this.$axios.delete("http://127.0.0.1:9000/cart/option/", {
                    params: {
                        "course_id": this.course.id,
                    },
                    headers: {
                        "Authorization": "jwt " + token,
                    }
                }).then(response => {
                    this.$message.success(response.data.message)

                    // 当自组价删除商品时需要通知父组件来执行对应的方法  可以向父组件提交事件
                    this.$emit("del_course");

                }).catch(error => {
                    console.log(error);
                    this.$message.success(error.data.message)
                })

            },
        },
    }
</script>

<style scoped>
    .cart_item::after {
        content: "";
        display: block;
        clear: both;
    }

    .cart_column {
        float: left;
        height: 250px;
    }

    .cart_item .column_1 {
        width: 88px;
        position: relative;
    }

    .my_el_checkbox {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        top: 0;
        margin: auto;
        width: 16px;
        height: 16px;
    }

    .cart_item .column_2 {
        padding: 67px 10px;
        width: 520px;
        height: 116px;
    }

    .cart_item .column_2 img {
        width: 175px;
        height: 115px;
        margin-right: 35px;
        vertical-align: middle;
    }

    .cart_item .column_3 {
        width: 197px;
        position: relative;
        padding-left: 10px;
    }

    .my_el_select {
        width: 117px;
        height: 28px;
        position: absolute;
        top: 0;
        bottom: 0;
        margin: auto;
    }

    .cart_item .column_4 {
        padding: 67px 10px;
        height: 116px;
        width: 142px;
        line-height: 116px;
    }

</style>
