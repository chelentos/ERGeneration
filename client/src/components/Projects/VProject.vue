<template>
    <b-container class="mb-3">
      <b-row class="justify-content-md-center">
        <b-col v-if="project" col lg="10">
          <div style="display: flex; justify-content: space-between;">
            <div style="display: flex; justify-content: flex-start;">
              <b-button
                :disabled="isTTGeneration"
                @click="toProjects"
                variant="outline-primary"
              >
                К проектам
              </b-button>
            </div>
            <div style="display: flex; justify-content: flex-end;">
              <b-button
                v-b-modal.newProjectModal
                @click="addReqs"
                class="mr-2"
                variant="primary"
              >
                Добавить требования
              </b-button>
              <b-button @click="TTGenClicked()" class="mr-2 genButton" variant="dark"
                :disabled="isERGeneration || project.reqs.length === 0"
              >
                {{ !isTTGeneration ? 'Создать ТЗ' : 'Отмена' }}
              </b-button>
              <b-button
                :disabled="isTTGeneration || project.reqs.length === 0"
                @click="erModalClick()"
                class="mr-2 genButton" variant="dark"
              >
                {{ !isERGeneration ? 'ER диаграмма' : 'Отмена' }}
              </b-button>
              <b-modal id="erModal" title="Просмотр ER" hide-footer>
                <div v-if="project.ers.length > 0" class="mt-3">
                  <div v-for="(er, index) in project.ers" :key="index">
                    <div @click="showER(er.erd)" class="erList__item">
                      {{ er.name }}
                      <div class="erList__item__sub">
                        {{ momentDate(er.createdAt) }}
                      </div>
                    </div>
                  </div>
                </div>
                <b-button :disabled="project.reqs.length === 0" @click="ERGenClicked()" variant="primary" class="erList__button">
                  Создать новую
                </b-button>
              </b-modal>
            </div>
          </div>
          <b-row class="ml-2 mt-2 mb-2">
            <h3>
              <span class="text-primary" style="font-weight: 700;">Проект:</span> {{ project.name }}
            </h3>
          </b-row>
          <!--
          <b-row class="justify-content-md-center mt-2 mb-2">
            <b-col col lg="9">
              <b-input placeholder="Поиск" />
            </b-col>
            <b-col col lg="3">
              <b-form-select
                v-model="selectedReqsType"
                :options="filterReqsOption"
              />
            </b-col>
          </b-row>
          -->
          <div v-if="project.reqs.length > 0" class="mt-3">
            <p v-for="(req, index) in project.reqs" :key="index">
              <v-reqs-list-item @checked="reqSelectionChanged" :req="req" ></v-reqs-list-item>
            </p>
          </div>
          <div v-else class="mt-5">
            <b-card class="text-center noReqsCard">
              <div>
                Требования отсутствуют
              </div>
            </b-card>
          </div>
          <div v-show="isERGeneration || isTTGeneration" class="genApproveButtons mb-5">
            <b-button variant="primary" class="mr-2"
              :disabled="selectedReqs.length === 0"
              @click="generate()"
            >
              Продолжить
            </b-button>
            <b-button @click="erModalClick()" variant="dark">
              Отмена
            </b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
</template>

<script>
import moment from 'moment'
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
      selectedReqsType: [],
      filterReqsOption: [
        {
          value: 'all',
          text: 'Все',
        },
        {
          value: 'FT',
          text: 'Отказоуст.',
        },
        {
          value: 'SE',
          text: 'Безопасн.',
        },
        {
          value: 'F',
          text: 'Функц.',
        },
        {
          value: 'LF',
          text: 'UI/UX',
        },
        {
          value: 'PE',
          text: 'Производ.',
        },
        {
          value: 'A',
          text: 'Доступн.',
        },
        {
          value: 'US',
          text: 'Юзабил.',
        },
        {
          value: 'SC',
          text: 'Масштаб.',
        },
        {
          value: 'O',
          text: 'Эксплуатац.',
        },
        {
          value: 'L',
          text: 'Закон.',
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      project: 'projects/getProject',
      isERGeneration: 'ergeneration/isERGeneration',
      isTTGeneration: 'ergeneration/isTTGeneration',
    }),
  },
  mounted() {
    this.setERGeneration(false)
    this.setTTGeneration(false)
    this.fetchProject(this.$route.params.projectId)
    this.selectedReqsType = 'all'
  },
  methods: {
    ...mapMutations({
      setERGeneration: 'ergeneration/setERGeneration',
      setTTGeneration: 'ergeneration/setTTGeneration',
      setIdx: 'ergeneration/setCurrentSent',
      setER: 'ergeneration/setER',
    }),
    ...mapActions({
      fetchProject: 'projects/fetchProject',
      genERSents: 'ergeneration/genERSents',
    }),
    addReqs() {
      this.$router.push(`/projects/${this.$route.params.projectId}/input`)
    },
    ERGenClicked() {
      this.$bvModal.hide('erModal')
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
            this.selectedReqs = []
          })
        this.setTTGeneration(false)  
      } else if (this.isERGeneration) {
        this.genERSents({
          projectId: this.$route.params.projectId,
          text: this.selectedReqs.map((r) => r.text).join(' '),
        })
          .then(() => {
            this.setIdx(0)
            this.$router.push(`/projects/${this.$route.params.projectId}/er_generation`)
          })
      }
    },
    toProjects() {
      this.$router.push('../')
    },
    erModalClick() {
      if (this.isERGeneration) {
        this.setERGeneration(!this.isERGeneration)
      } else {
        this.$bvModal.show('erModal')
      }
      window.scrollTo(0, 0)
    },
    momentDate(date) {
      return moment(date).format('DD.MM.YYYY')
    },
    showER(erd) {
      this.setER(erd)
      this.$router.push(`/projects/${this.$route.params.projectId}/er`)
    }
  },
}
</script>

<style lang="scss" scoped>
.genButton {
  width: 180px !important;
}

.genApproveButtons {
  display: flex;
  justify-content: center;
  width: 100%;
}

.noReqsCard {
  font-size: 1.5em;
  font-weight: 600;
}

.erDropdown {
  margin: 0 !important;
}

.erList {

  &__button {
    margin: 10px 0;
    width: 100%;
  }

  &__item {
    cursor: pointer;
    margin-bottom: 10px;
    &__sub {
      font-size: 0.9em;
      color: grey;
    }
  }

  &__item:hover {
    background: rgb(243, 243, 243);
  }
}
</style>
