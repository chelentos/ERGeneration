import http from './http'

export default {
  getProjects() {
    return http.get('/api/projects')
  },

  newProject(name) {
    return http.post('/api/projects', { name })
  },

  deleteProject(id) {
    return http.delete(`/api/projects/${id}`)
  }
}
