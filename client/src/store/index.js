import Vue from 'vue'
import Vuex from 'vuex'
import Reqs from './modules/reqs'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    reqs: {
      namespaced: true,
      ...Reqs,
    },
  },
})
