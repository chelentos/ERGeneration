import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./components/Container/VContainer.vue'),
      children: [
        {
          path: 'login',
          name: 'login',
          meta: { label: '' },
          component: () => import('./components/Auth/VLoginForm.vue'),
        },
        {
          path: 'register',
          name: 'register',
          meta: { label: '' },
          component: () => import('./components/Auth/VRegisterForm.vue'),
        },
        {
          path: 'projects',
          name: 'projects',
          meta: { label: '' },
          component: () => import('./components/Projects/VProjectsList.vue'),
        },
      ],
    },
  ],
})
