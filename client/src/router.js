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
        {
          path: 'projects/:projectId',
          name: 'project',
          meta: { label: '' },
          component: () => import('./components/Projects/VProject.vue'),
        },
        {
          path: 'projects/:projectId/input',
          name: 'reqsInput',
          meta: { label: '' },
          component: () => import('./components/Requirements/VReqsInput.vue'),
        },
        {
          path: 'projects/:projectId/er_generation',
          name: 'er_generation',
          meta: { label: '' },
          component: () => import('./components/ER/VERGeneration.vue'),
        },
        {
          path: 'projects/:projectId/er',
          name: 'er_generation',
          meta: { label: '' },
          component: () => import('./components/ER/VShowER.vue'),
        },
      ],
    },
  ],
})
