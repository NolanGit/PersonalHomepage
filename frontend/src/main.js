import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import router from './routes'
import Vuex from 'vuex'
import './assets/iconfont/iconfont.css'
import 'font-awesome/css/font-awesome.min.css'
import VueCookies from 'vue-cookies'

Vue.use(VueCookies)
Vue.use(ElementUI)
Vue.use(Vuex)

new Vue({
    router,
    el: '#app',
    render: h => h(App)
})