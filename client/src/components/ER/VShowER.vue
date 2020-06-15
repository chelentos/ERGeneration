<template>
    <b-container v-if="sent || !isNewEr" class="ERGenContainer mb-3">
        <v-e-r class="mt-4" />
        <div class="buttonsBlock mt-3">
          <b-button v-if="isNewEr" @click="openSaveModal" variant="primary" class="mr-2">
            Сохранить
          </b-button>
          <b-button @click="exportXML" variant="primary" class="mr-2">
            Экспорт в XML
          </b-button>
          <b-button class="mr-2" @click="goBack">
            Назад
          </b-button>
          <b-button v-if="isNewEr" variant="dark" @click="goToProject">
            Отмена
          </b-button>
        </div>
        <b-modal id="saveErModal" title="Сохранение ER-диаграммы" hide-footer>
          <div class="saveModal">
            <div class="saveModal__item">
              <b-input type="text" placeholder="Название" v-model="name"></b-input>
            </div>
            <div>
              <b-button @click="saveEr" variant="primary">
                Сохранить
              </b-button>
            </div>
          </div>
        </b-modal>
    </b-container>
</template>

<script>

import _ from 'lodash'

import { mapMutations, mapActions, mapGetters } from 'vuex'

import projectsAPI from '../../api/projects'

import VER from '../Graph/VER.vue'

export default {
  name: 'VShowER',
  components: {
    VER,
  },
  data() {
    return {
      fields: ['text', 'num', 'action'],
      typeOptions: [
        {
          value: 'ent',
          text: 'сущ.',
        },
        {
          value: 'atr',
          text: 'атр.',
        },
      ],
      numOptions: [
        {
          value: 'Sing',
          text: 'ед.',
        },
        {
          value: 'Plur',
          text: 'мн.',
        },
      ],
      depOptions: [
        {
          value: true,
          text: 'обяз.',
        },
        {
          value: false,
          text: 'необяз.',
        },
      ],
      wordForDelete: null,
      deleteWordType: null,
      wordForAdd: '',
      addWordType: null,
      addWordNum: '',
      name: '',
    }
  },
  computed: {
    ...mapGetters({
      sents: 'ergeneration/getERSents',
      idx: 'ergeneration/getCurrentSent',
      er: 'ergeneration/getER',
      isNewEr: 'ergeneration/isNewEr',
    }),
    sent() {
      return this.sents.length > 0 ? this.sents[this.idx] : null
    },
  },
  mounted() {
    this.subjectTextChanged = _.debounce((data, val) => {
      const newEl = { ...data.item, text: val}
      this.updateElement({
        type: 'subj',
        oldEl: data.item,
        newEl,
      })
    }, 500)

    this.objectTextChanged = _.debounce((data, val) => {
      const newEl = { ...data.item, text: val}
      this.updateElement({
        type: 'obj',
        oldEl: data.item,
        newEl,
      })
    }, 500)

    this.depChanged = _.debounce((val) => {
      this.updateDep({
        ...this.sents[this.idx].dep,
        text: val,
      })
    }, 500)
  },
  methods: {
    ...mapMutations({
      setIsNewER: 'ergeneration/setIsNewER',
    }),
    goToProject() {
      this.setIsNewER(false)
      this.$router.push('./')
    },
    goBack() {
      if (this.isNewEr) {
        this.$router.push(`/projects/${this.$route.params.projectId}/er_generation`)
      } else {
        this.setIsNewER(false)
        this.$router.push('./')
      }
    },
    openSaveModal() {
      this.$bvModal.show('saveErModal')
    },
    saveEr() {
      projectsAPI.saveER(this.$route.params.projectId, {
        erd: this.er,
        name: this.name
      }).then(() => {
        this.setIsNewER(false)
        this.$router.push('./')
      })
    },
    exportXML() {
      projectsAPI.exportXML(this.er)
        .then((response) => {
          window.open(`http://127.0.0.1:5000/${response.data.xmlLink}`, '_blank')
        })
    }
  },
}
</script>

<style lang="scss" scoped>

.chevronWrapper {
  position:absolute; height:100%; width:100%;
  display: table;

  span {
    display: table-cell;
    vertical-align: middle;
    text-align:center;
    
    i {
      cursor: pointer;
    }
  }
}

.sentenceText {
  width: 100%;
  margin-bottom: 0;
}

.buttonsBlock {
  display: flex;
  justify-content: flex-end;
}

.ERGenContainer {
  padding: 0;
}

.typeCol {
  padding: 0 2px 0 2px;
}

.addWordDiv {
  display: flex;
  justify-content: center;

  &__button {
    width: 150px;
  }
}

.buttonsBlock {
  display: flex;
  justify-content: center;
}

.saveModal {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  &__item {
    width: 80%;
    min-width: 320px;
    margin-bottom: 15px;
  }
}

</style>
