const MUTATION_TYPE = {
  setReqs: 'setReqs',
  setCurrentUser: 'setCurrentUser',
  setProjects: 'setProjects',
  setProject: 'setProject',
  setProjectReqs: 'setProjectReqs',
  setERGeneration: 'setERGeneration',
  setTTGeneration: 'setTTGeneration',
  setERSents: 'setERSents',
}

const ACTION_TYPE = {
  sendReqs: 'sendReqs',
  fetchCurrentUser: 'fetchCurrentUser',
  login: 'login',
  register: 'register',
  logout: 'logout',
  fetchProjects: 'fetchProjects',
  fetchProject: 'fetchProject',
  loadReqs: 'loadReqs',
  genERSents: 'genERSents',
}

const GETTER_TYPE = {
  getReqs: 'getReqs',
  getCurrentUser: 'getCurrentUser',
  getProjects: 'getProjects',
  getProject: 'getProject',
  isERGeneration: 'isERGeneration',
  isTTGeneration: 'isTTGeneration',
  getERSents: 'getERSents',
}

export {
  MUTATION_TYPE,
  ACTION_TYPE,
  GETTER_TYPE,
}
