import Vue from 'vue'
import { BootstrapVue } from 'bootstrap-vue'
import VueCookies from 'vue-cookies'
import App from '@/App.vue'


import store from '@/store'
import router from '@/router'

import './sass/sass.scss'

Vue.use(BootstrapVue)
Vue.use(VueCookies)

Vue.config.productionTip = false

// Vue.use(VueRouter)

store.dispatch('currentUser/fetchCurrentUser').then(() => {
  new Vue({
    router,
    store,
    render: (h) => h(App),
  }).$mount('#app')
})
