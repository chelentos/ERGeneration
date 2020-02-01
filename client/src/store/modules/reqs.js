/* eslint-disable no-param-reassign */
import { MUTATION_TYPE, ACTION_TYPE, GETTER_TYPE } from '../../types'

import reqsAPI from '../../api/reqs'

export default {
  state: {
    reqs: null,
  },

  mutations: {
    [MUTATION_TYPE.setReqs]: (state, reqs) => {
      state.reqs = reqs
    },
  },

  actions: {
    [ACTION_TYPE.sendReqs]: async ({ commit }, reqs) => {
      const creqs = await reqsAPI.classify(reqs)
      commit(MUTATION_TYPE.setReqs, creqs.data)
    },
  },

  getters: {
    [GETTER_TYPE.getReqs]: (state) => state.reqs,
  },
}
