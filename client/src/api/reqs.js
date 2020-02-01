import axios from 'axios'

export default {
  classify(reqs) {
    console.log(reqs)
    return axios.post('/api/classify', { reqs })
  },
}
