<template>
    <b-container>
      <b-row class="justify-content-md-center">
        <b-col col lg="10">
          <b-button
            v-b-modal.newProjectModal
            block variant="primary"
          >
            Создать новый проект
          </b-button>
          <div v-if="projects.length > 0" class="mt-3">
            <p v-for="project in projects" :key="project.id">
              <v-projects-list-item :project="project" class="mb-2"></v-projects-list-item>
            </p>
          </div>
        </b-col>
      </b-row>
      <b-modal 
        id="newProjectModal"
        title="Новый проект"
        :ok-title="'Создать'"
        :cancel-title="'Отмена'"
        @ok="newProject()"
        @hide="newProjectTitle = ''"
      >
        <b-input autofocus v-model="newProjectTitle" placeholder="Введите название"></b-input>
      </b-modal>
    </b-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

import projectsAPI from '../../api/projects'

import VProjectsListItem from './VProjectsListItem.vue'

export default {
  name: 'VProjectsList',
  components: {
    VProjectsListItem,
  },
  data() {
    return {
      newProjectTitle: '',
    }
  },
  computed: {
    ...mapGetters({
      currentUser: 'currentUser/getCurrentUser',
      projects: 'projects/getProjects',
    }),
  },
  mounted() {
    this.fetchProjects()
  },
  methods: {
    ...mapActions({
      fetchProjects: 'projects/fetchProjects',
    }),
    newProject() {
      projectsAPI.newProject(this.newProjectTitle).then(() => {
        this.fetchProjects()
      })
    }
  },
}
</script>

<style scoped>
</style>
