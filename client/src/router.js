import Vue from 'vue'
import Router from 'vue-router'
import ReqsInput from '@/components/ReqsInput.vue'
import ClassifiedReqs from '@/components/ClassifiedReqs.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: ReqsInput,
    },
    {
      path: '/reqs',
      name: 'reqs',
      component: ClassifiedReqs,
      meta: { label: '' },
    },
  ],
})
