import Vue from 'vue'
import Router from 'vue-router'
import Index from "../components/Index";
import Login from "../components/Login";
import Register from "../components/Register";
import Course from "../components/Course";
import CourseDetail from "../components/CourseDetail";
import Cart from "../components/Cart";
import Order from "../components/Order";
import OrderSuccess from "../components/OrderSuccess";


Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'index',
            component: Index
        },
        {path: '/index', name: 'index', component: Index},
        {
            path: '/login',
            name: 'login',
            component: Login
        },
        {
            path: '/register',
            name: 'register',
            component: Register
        },
        {path: '/course', name: 'course', component: Course},
        {path: '/detail/:id', name: 'CourseDetail', component: CourseDetail},
        {path: "/cart", name: 'cart', component: Cart},
        {path: "/order", name: 'order', component: Order},
        {path: "/payments/result", component: OrderSuccess}
    ]
})
