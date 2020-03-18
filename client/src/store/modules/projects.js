/* eslint-disable no-param-reassign */
import { MUTATION_TYPE, ACTION_TYPE, GETTER_TYPE } from '../../types'

import projectsAPI from '../../api/projects'

export default {
  state: {
    projects: [],
    project: null,
    isERGeneration: false,
    isTTGeneration: false,
  },

  mutations: {
    [MUTATION_TYPE.setProjects]: (state, projects) => {
      state.projects = projects
    },
    [MUTATION_TYPE.setProject]: (state, project) => {
      state.project = project
    },
    [MUTATION_TYPE.setProjectReqs]: (state, reqs) => {
      state.project.reqs = reqs
    },
    [MUTATION_TYPE.setERGeneration]: (state, ERGeneration) => {
      state.isERGeneration = ERGeneration
    },
    [MUTATION_TYPE.setTTGeneration]: (state, TTGeneration) => {
      state.isTTGeneration = TTGeneration
    },
  },

  actions: {
    [ACTION_TYPE.fetchProjects]: async ({ commit }) => {
      const response = await projectsAPI.getProjects()
      commit(MUTATION_TYPE.setProjects, response.data.projects)
    },

    [ACTION_TYPE.fetchProject]: async ({ commit }, id) => {
      const response = await projectsAPI.getProject(id)
      commit(MUTATION_TYPE.setProject, response.data.project)
    },

    [ACTION_TYPE.loadReqs]: async ({ commit }, { projectId, reqs }) => {
      const response = await projectsAPI.loadReqs(projectId, reqs)
      commit(MUTATION_TYPE.setProjectReqs, response.data.reqs)
    },
  },

  getters: {
    [GETTER_TYPE.getProjects]: (state) => state.projects,
    [GETTER_TYPE.getProject]: (state) => state.project,
    [GETTER_TYPE.isERGeneration]: (state) => state.isERGeneration,
    [GETTER_TYPE.isTTGeneration]: (state) => state.isTTGeneration,
  },
}
