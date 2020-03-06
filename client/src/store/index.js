import Vue from 'vue'
import Vuex from 'vuex'
import Reqs from './modules/reqs'
import CurrentUser from './modules/currentUser'
import Projects from './modules/projects'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    reqs: {
      namespaced: true,
      ...Reqs,
    },
    currentUser: {
      namespaced: true,
      ...CurrentUser,
    },
    projects: {
      namespaced: true,
      ...Projects,
    },
  },
})
