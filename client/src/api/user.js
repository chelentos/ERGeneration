import http from './http'

export default {
  login(form) {
    return http.post('/api/users/login', form)
  },

  current() {
    return http.get('/api/users/current')
  },

  register(form) {
    return http.post('/api/users/register', form)
  },

  logout() {
    return http.get('/api/users/logout')
  },
}
