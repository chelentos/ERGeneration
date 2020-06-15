/* eslint-disable no-param-reassign */
import { MUTATION_TYPE, ACTION_TYPE, GETTER_TYPE } from '../../types'

import projectsAPI from '../../api/projects'

export default {
  state: {
    isERGeneration: false,
    isTTGeneration: false,
    ERSents: [],
    currentSent: 0,
    ER: null,
    isNewER: false,
  },

  mutations: {
    [MUTATION_TYPE.setERGeneration]: (state, ERGeneration) => {
      state.isERGeneration = ERGeneration
    },
    [MUTATION_TYPE.setTTGeneration]: (state, TTGeneration) => {
      state.isTTGeneration = TTGeneration
    },
    [MUTATION_TYPE.setERSents]: (state, sents) => {
      state.ERSents = sents
    },
    [MUTATION_TYPE.setCurrentSent]: (state, idx) => {
      state.currentSent = idx
    },
    [MUTATION_TYPE.updateElement]: (state, { type, oldEl, newEl }) => {
      switch (type) {
        case 'subj':
          if (state.ERSents[state.currentSent].subjs.subjects.length > 0) {
            state.ERSents[state.currentSent].subjs.subjects 
              = state.ERSents[state.currentSent].subjs.subjects.map((s) => {
                return s === oldEl ? newEl : s
              })
          }
          break
        case 'obj':
          if (state.ERSents[state.currentSent].objs.objects.length > 0) {
            state.ERSents[state.currentSent].objs.objects
              = state.ERSents[state.currentSent].objs.objects.map((o) => {
                return o === oldEl ? newEl : o
              })
          }
          break
        default:
          break
      }
    },
    [MUTATION_TYPE.updateElementsType]: (state, { type, elType }) => {
      switch (type) {
        case 'subj':
          if (state.ERSents[state.currentSent].subjs) {
            state.ERSents[state.currentSent].subjs.type = elType
          }
          break
        case 'obj':
          if (state.ERSents[state.currentSent].objs) {
            state.ERSents[state.currentSent].objs.type = elType
          }
          break
        default:
          break
      }
    },
    [MUTATION_TYPE.updateDep]: (state, newDep) => {
      state.ERSents[state.currentSent].dep = newDep
    },
    [MUTATION_TYPE.deleteERSent]: (state) => {
      state.ERSents.splice(state.currentSent, 1)
      if (state.currentSent >= state.ERSents.length - 1) {
        state.currentSent -=1
      }
    },
    [MUTATION_TYPE.deleteERSentWord]: (state, { type, word }) => {
      if (type === 'subj') {
        state.ERSents[state.currentSent].subjs.subjects 
        = state.ERSents[state.currentSent].subjs.subjects.filter((w) => w !== word)
      } else if (type === 'obj') {
        state.ERSents[state.currentSent].objs.objects
        = state.ERSents[state.currentSent].objs.objects.filter((w) => w !== word)
      }
    },
    [MUTATION_TYPE.addERSentWord]: (state, { type, word }) => {
      if (type === 'subj') {
        state.ERSents[state.currentSent].subjs.subjects.push(word)
      } else if (type === 'obj') {
        state.ERSents[state.currentSent].objs.objects.push(word)
      }
    },
    [MUTATION_TYPE.setER]: (state, er) => {
      state.ER = er
    },
    [MUTATION_TYPE.setIsNewER]: (state, isNewER) => {
      state.isNewER = isNewER
    }
  },

  actions: {
    [ACTION_TYPE.genERSents]: async ({ commit }, { projectId, text }) => {
      const response = await projectsAPI.generateER(projectId, text)
      commit(MUTATION_TYPE.setERSents, response.data.er)
    },
    [ACTION_TYPE.sendERSents]: async ({ state, commit }) => {
      const response = await projectsAPI.sendERSents(state.ERSents)
      commit(MUTATION_TYPE.setER, response.data.er)
    },
  },

  getters: {
    [GETTER_TYPE.isERGeneration]: (state) => state.isERGeneration,
    [GETTER_TYPE.isTTGeneration]: (state) => state.isTTGeneration,
    [GETTER_TYPE.getERSents]: (state) => state.ERSents,
    [GETTER_TYPE.getCurrentSent]: (state) => state.currentSent,
    [GETTER_TYPE.getER]: (state) => state.ER,
    [GETTER_TYPE.isNewEr]: (state) => state.isNewER,
  },
}
