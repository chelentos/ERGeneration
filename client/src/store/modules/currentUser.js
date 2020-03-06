/* eslint-disable no-param-reassign */
import { MUTATION_TYPE, ACTION_TYPE, GETTER_TYPE } from '../../types'

import userAPI from '../../api/user'

export default {
  state: {
    user: null,
  },

  mutations: {
    [MUTATION_TYPE.setCurrentUser]: (state, user) => {
      state.user = user
    },
  },

  actions: {
    [ACTION_TYPE.fetchCurrentUser]: async ({ commit }) => {
      const response = await userAPI.current()
      commit('setCurrentUser', response.data.user)
    },
    [ACTION_TYPE.login]: async ({ commit }, form) => {
      const response = await userAPI.login(form)
      commit('setCurrentUser', response.data.user)
    },
    [ACTION_TYPE.register]: async ({ commit }, form) => {
      const response = await userAPI.register(form)
      commit('setCurrentUser', response.data.user)
    },
    [ACTION_TYPE.logout]: async ({ commit }) => {
      userAPI.logout().then((response) => {
        commit('setCurrentUser', null)
      })
    },
  },

  getters: {
    [GETTER_TYPE.getCurrentUser]: (state) => state.user,
  },
}
