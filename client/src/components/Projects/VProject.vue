<template>
    <b-container class="mt-5">
      <b-row class="justify-content-md-center">
        <b-col v-if="project" col lg="10">
          <div>
            <div style="display: flex; justify-content: flex-start; float: left;">
              <h3 style="justify-content: flex-end;">
                {{ project.name }}
              </h3>
            </div>
            <div style="display: flex; justify-content: flex-end;">
              <b-button @click="TTGenClicked()" class="mr-2 genButton"
                :disabled="isERGeneration"
              >
                {{ !isTTGeneration ? 'Создать ТЗ' : 'Отмена' }}
              </b-button>
              <b-button @click="ERGenClicked()" class="genButton"
                :disabled="isTTGeneration"
              >
                {{ !isERGeneration ? 'Сгенерировать ER' : 'Отмена' }}
              </b-button>
            </div>
          </div>
          <b-button
            v-b-modal.newProjectModal
            block variant="primary"
            @click="addReqs"
          >
            Добавить требования
          </b-button>
          <div v-if="project.reqs.length > 0" class="mt-3">
            <p v-for="(req, index) in project.reqs" :key="index">
              <v-reqs-list-item @checked="reqSelectionChanged" :req="req" ></v-reqs-list-item>
            </p>
          </div>
          <div v-show="isERGeneration || isTTGeneration" class="genApproveButtons mb-5">
            <b-button variant="primary" class="mr-2"
              :disabled="selectedReqs.length === 0"
              @click="generate()"
            >
              Продолжить
            </b-button>
            <b-button variant="dark">
              Отмена
            </b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
</template>

<script>
import { mapMutations, mapActions, mapGetters } from 'vuex'

import VReqsListItem from '../Requirements/VReqsListItem.vue'

import projectsAPI from '../../api/projects'

export default {
  name: 'VProject',
  components: {
    VReqsListItem,
  },
  data() {
    return {
      selectedReqs: [],
    }
  },
  computed: {
    ...mapGetters({
      project: 'projects/getProject',
      isERGeneration: 'projects/isERGeneration',
      isTTGeneration: 'projects/isTTGeneration',
    }),
  },
  mounted() {
    this.fetchProject(this.$route.params.projectId)
  },
  methods: {
    ...mapMutations({
      setERGeneration: 'projects/setERGeneration',
      setTTGeneration: 'projects/setTTGeneration',
    }),
    ...mapActions({
      fetchProject: 'projects/fetchProject',
      genERSents: 'projects/genERSents',
    }),
    addReqs() {
      this.$router.push(`/projects/${this.$route.params.projectId}/input`)
    },
    ERGenClicked() {
      this.setERGeneration(!this.isERGeneration)
    },
    TTGenClicked() {
      this.setTTGeneration(!this.isTTGeneration)
    },
    reqSelectionChanged(val) {
      if (val.selected) {
        if (!this.selectedReqs.find((el) => el.id === val.req.id)) {
          this.selectedReqs.push(val.req)
        }
      } else if (this.selectedReqs.find((el) => el.id === val.req.id)) {
        this.selectedReqs = this.selectedReqs.filter((r) => r.id !== val.req.id)
      }
    },

    generate() {
      if (this.isTTGeneration) {
        projectsAPI.generateTT(this.$route.params.projectId, this.selectedReqs)
          .then((response) => {
            window.open(`http://127.0.0.1:5000/${response.data.ttLink}`, '_blank')
            this.setTTGeneration(false)
            this.selectedReqs = []
          })
      } else if (this.isERGeneration) {
        this.genERSents({
          projectId: this.$route.params.projectId,
          text: this.selectedReqs.map((r) => r.text).join(' '),
        })
          .then(() => {
            this.$router.push('./')
          })
      }
    },
  },
}
</script>

<style scoped>
.genButton {
  width: 180px !important;
}

.genApproveButtons {
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>
