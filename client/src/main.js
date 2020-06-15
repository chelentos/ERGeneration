import Vue from 'vue'
import { BootstrapVue } from 'bootstrap-vue'
import VueCookies from 'vue-cookies'
import VueMoment from 'vue-moment'
import App from '@/App.vue'


import store from '@/store'
import router from '@/router'

import '@/sass/sass.scss'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(VueCookies)

Vue.config.productionTip = false

const moment = require('moment')
require('moment/locale/ru')

Vue.use(VueMoment, {
  moment,
})

store.dispatch('currentUser/fetchCurrentUser').then(() => {
  new Vue({
    router,
    store,
    render: (h) => h(App),
  }).$mount('#app')
})
