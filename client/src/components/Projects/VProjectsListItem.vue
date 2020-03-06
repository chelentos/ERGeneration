<template>
    <b-card :title="project.name" :sub-title="`Количество требований: ${project.reqsNum}`">
      <span class="projectsList__item__deleteIcon-color">
        <i
          @click="showDeleteModal()"
          class="fas fa-trash-alt projectsList__item__deleteIcon"
        ></i>
      </span>
      <a :href="`/#/projects/${project.id}`" class="card-link">Открыть</a>
      <b-modal 
        :id="`deleteProjectModal-${project.id}`"
        title="Удаление проекта"
        :ok-title="'Ок'"
        :cancel-title="'Отмена'"
        @ok="deleteProject()"
        @hide="newProjectTitle = ''"
      >
        <p>Вы действительно хотите удалить данный проект?</p>
      </b-modal>
    </b-card>
</template>

<script>
import { mapActions } from 'vuex'

import projectsAPI from '../../api/projects'

export default {
  name: 'VProjectsListItem',
  props: {
    project: {
      type: Object,
      default() {
        return {}
      },
    },
  },
  methods: {
    ...mapActions({
      fetchProjects: 'projects/fetchProjects',
    }),
    deleteProject() {
      projectsAPI.deleteProject(this.project.id).then(() => {
        this.fetchProjects()
      })
    },
    showDeleteModal() {
      this.$bvModal.show(`deleteProjectModal-${this.project.id}`)
    },
  },
}
</script>

<style lang="scss" scoped>
.projectsList__item__deleteIcon {
  position: absolute;
  right: 20px;
  top: 24px;
  cursor: pointer;

  &-color {
    color: #d94343;
  }
}
</style>
