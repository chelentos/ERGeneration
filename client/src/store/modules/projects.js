/* eslint-disable no-param-reassign */
import { MUTATION_TYPE, ACTION_TYPE, GETTER_TYPE } from '../../types'

import projectsAPI from '../../api/projects'

export default {
  state: {
    projects: [],
  },

  mutations: {
    [MUTATION_TYPE.setProjects]: (state, projects) => {
      state.projects = projects
    },
  },

  actions: {
    [ACTION_TYPE.fetchProjects]: async ({ commit }) => {
      const response = await projectsAPI.getProjects()
      commit(MUTATION_TYPE.setProjects, response.data.projects)
    },
  },

  getters: {
    [GETTER_TYPE.getProjects]: (state) => state.projects,
  },
}
