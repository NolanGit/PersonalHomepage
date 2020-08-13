import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import './assets/public.css'
import router from './routes'
import VCharts from 'v-charts'
import ElementUI from 'element-ui'
import VueCookies from 'vue-cookies'
import './assets/iconfont/iconfont.css'
import VueClipboard from 'vue-clipboard2'
import 'element-ui/lib/theme-chalk/index.css'
import 'font-awesome/css/font-awesome.min.css'

Vue.use(Vuex)
Vue.use(VCharts)
Vue.use(ElementUI)
Vue.use(VueCookies)
Vue.use(VueClipboard)

new Vue({
    router,
    el: '#app',
    render: h => h(App)
})