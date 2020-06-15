<template>
    <b-card v-if="req" no-body class="mb-1">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <div @click="showAcc()" class="reqList__item-header">
          <b-row v-if="!isERGeneration && !isTTGeneration">
            <b-col lg="8">
              <p>
                {{ req.text }}
              </p>
            </b-col>
            <b-col lg="4">
              Тип: {{ translateReqType(req.type) }}
            </b-col>
          </b-row>
          <b-row v-else>
            <b-col lg="1">
              <b-form-checkbox
                :id="`check-${req.id}`"
                v-model="status"
              >
              </b-form-checkbox>
            </b-col>
            <b-col lg="7">
              <p>
                {{ req.text }}
              </p>
            </b-col>
            <b-col lg="4">
              Тип: {{ translateReqType(req.type) }}
            </b-col>
          </b-row>
        </div>
      </b-card-header>
      <b-collapse :id="`acc-${req.id}`" role="tabpanel"
        @hidden="onCollapseClose()"
      >
        <b-card-body>
          <div>
            <b-row>
              <b-col lg="8">
                <p style="font-weight: 600;">
                  Дата добавления: {{ createdAt }}
                </p>
              </b-col>
              <b-col style="display: flex; justify-content: flex-end;" lg="4">
                <span style="color: #d94343;">
                  <i
                    @click="showDeleteModal()"
                    class="fas fa-trash-alt deleteReqIcon"
                  ></i>
                </span>
              </b-col>
            </b-row>
            <b-row>
              <b-col lg="8">
                <b-form-textarea
                  v-model="newReqText"
                  placeholder="Введите требования"
                  rows="2"
                  max-rows="4"
                  class="reqsInput__area"
                ></b-form-textarea>
              </b-col>
              <b-col lg="4">
                <b-form-group>
                  <b-row>
                    <b-col sm="3">
                      <p class="mt-1">
                        Тип:
                      </p>
                    </b-col>
                    <b-col sm="9">
                      <b-form-select v-model="reqType" :options="options">
                      </b-form-select>
                    </b-col>
                  </b-row>
                </b-form-group>
              </b-col>
            </b-row>
          </div>
          <div style="display: flex; justify-content: flex-end;">
            <div class="mt-2">
              <b-button @click="saveChanges()" variant="primary" class="mr-4">Сохранить</b-button>
              <b-button @click="declineChange()" variant="dark">Отмена</b-button>
            </div>
          </div>
        </b-card-body>
        <b-modal
          :id="`deleteReqsModal-${req.id}`"
          title="Удаление требования"
          :ok-title="'Ок'"
          :cancel-title="'Отмена'"
          @ok="deleteReq()"
          @hide="newProjectTitle = ''"
        >
          <p>Вы действительно хотите удалить данное требование?</p>
        </b-modal>
      </b-collapse>
    </b-card>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

import moment from 'moment'
import reqsMixin from '../../mixins/reqsMixin'

import projectsAPI from '../../api/projects'


export default {
  name: 'VReqsListItem',
  data() {
    return {
      status: false,
      reqType: '',
      newReqText: '',
      options: [
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
          text: 'Поддерж.',
        },
        {
          value: 'L',
          text: 'Закон.',
        },
      ],
    }
  },
  props: {
    req: {
      type: Object,
      default() {
        return {}
      },
    },
  },
  mixins: [reqsMixin],
  mounted() {
    this.restoreDefault()
  },
  computed: {
    ...mapGetters({
      isERGeneration: 'ergeneration/isERGeneration',
      isTTGeneration: 'ergeneration/isTTGeneration',
    }),
    createdAt() {
      return moment(this.req.createdAt).format('DD, MMMM YYYY, HH:mm')
    },
  },
  watch: {
    status() {
      this.$emit('checked', {
        selected: this.status,
        req: this.req,
      })
    },
    isTTGeneration() {
      if (this.isTTGeneration) {
        this.status = true
      } else {
        this.status = false
      }
    },
    isERGeneration() {
      if (this.isERGeneration) {
        if (this.req.type === 'F') {
          this.status = true
        }
      } else {
        this.status = false
      }
    },
  },
  methods: {
    ...mapActions({
      fetchProject: 'projects/fetchProject',
    }),

    showAcc() {
      if (!this.isERGeneration && !this.isTTGeneration) {
        this.$root.$emit('bv::toggle::collapse', `acc-${this.req.id}`)
      }
    },

    restoreDefault() {
      this.reqType = this.req.type
      this.newReqText = this.req.text
    },

    onCollapseClose() {
      this.restoreDefault()
    },

    declineChange() {
      this.restoreDefault()
      this.$root.$emit('bv::toggle::collapse', `acc-${this.req.id}`)
    },

    saveChanges() {
      this.$root.$emit('bv::toggle::collapse', `acc-${this.req.id}`)
      projectsAPI.updateReq(this.$route.params.projectId, {
        id: this.req.id,
        text: this.newReqText,
        type: this.reqType,
      }).then(() => {
        this.fetchProject(this.$route.params.projectId)
      })
    },

    showDeleteModal() {
      this.$bvModal.show(`deleteReqsModal-${this.req.id}`)
    },

    deleteReq() {
      this.$root.$emit('bv::toggle::collapse', `acc-${this.req.id}`)
      projectsAPI.deleteRequirement(
        this.$route.params.projectId,
        this.req.id,
      ).then(() => {
        this.fetchProject(this.$route.params.projectId)
      })
    },
  },
}
</script>

<style lang="scss" scoped>
.reqList__item-header {
  padding: 15px;

  p {
    margin-bottom: 0;
  }
}

.deleteReqIcon {
  cursor: pointer;
}
</style>
