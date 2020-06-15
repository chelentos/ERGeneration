import Vue from 'vue'
import Vuex from 'vuex'
import CurrentUser from './modules/currentUser'
import Projects from './modules/projects'
import ERGeneration from './modules/ergeneration'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    currentUser: {
      namespaced: true,
      ...CurrentUser,
    },
    projects: {
      namespaced: true,
      ...Projects,
    },
    ergeneration: {
      namespaced: true,
      ...ERGeneration
    }
  },
})
