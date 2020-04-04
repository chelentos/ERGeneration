import http from './http'

export default {
  getProjects() {
    return http.get('/api/projects')
  },

  newProject(name) {
    return http.post('/api/projects', { name })
  },

  getProject(id) {
    return http.get(`/api/projects/${id}`)
  },

  deleteProject(id) {
    return http.delete(`/api/projects/${id}`)
  },

  loadReqs(projectId, reqs) {
    return http.post(`/api/projects/${projectId}/reqs`, { reqs })
  },

  updateReq(projectId, req) {
    return http.put(`/api/projects/${projectId}/reqs`, { req })
  },

  deleteRequirement(projectId, reqId) {
    return http.delete(`/api/projects/${projectId}/reqs/${reqId}`)
  },

  generateTT(projectId, reqs) {
    return http.post(`/api/projects/${projectId}/generate-tt`, { reqs })
  },

  generateER(projectId, text) {
    return http.post(`/api/projects/${projectId}/generate-er`, { text })
  },
}
