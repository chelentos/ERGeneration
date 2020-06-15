<template>
    <b-container v-if="sent" class="ERGenContainer mb-3">
      <b-row class="justify-content-md-center">
        <b-col col lg="12">
          <div class="buttonsBlock">
            <b-button 
              @click="generateER"
              variant="primary"
              class="mr-2"
            >Генерация</b-button>
            <b-button 
              @click="deleteSentenceModal"
              variant="danger"
              class="mr-2"
            >Убрать предложение</b-button>
            <b-button
              @click="goBack"
              variant="dark"
            >Отмена</b-button>
          </div>
          <div class="sentenceText mt-3">
            <p>
              <span class="text-primary" style="font-weight: 700;">Предложение: </span>
              {{ sent.sentence_text }}
            </p>
          </div>
          <v-diagram class="mt-4" :sent="sent" />
          <b-modal
            :id="`deleteSentenceModal-${idx}`"
            title="Удаление предложения"
            :ok-title="'Ок'"
            :cancel-title="'Отмена'"
            @ok="deleteSentence"
          >
            <p>Вы действительно хотите убрать данное предложение?</p>
          </b-modal>
        </b-col>
      </b-row>
      <b-row class="justify-content-md-center mt-2">
        <b-col col lg="4">
          <b-table
            :items="sent.subjs.subjects"
            :fields="fields"
            responsive="sm"
          >
            <template v-slot:head(text)="data">
              <span class="text-primary">Субъект</span>
            </template>
            <template v-slot:head(num)="data">
              <span class="text-primary">Число</span>
            </template>
            <template v-slot:head(action)="data">
              <span></span>
            </template>
            <template v-slot:cell(text)="data">
              <b-input @input="subjectTextChanged(data, $event)" :value="data.item.text" />
            </template>
            <template v-slot:cell(num)="data">
              <b-form-select @input="subjectNumChanged(data, $event)" :value="data.item.num" :options="numOptions" />
            </template>
            <template v-slot:cell(action)="data">
              <div class="actionsCell">
                <span
                  style="color: #d94343; cursor: pointer;"
                  @click="deleteWordModal(data, 'subj')"
                >
                  <i class="fas fa-times"></i>
                </span>
                <span
                  v-if="sent.subjs.type === 'atr'"
                  style="cursor: pointer;"
                  :style="data.item.isKey ? 'color: #194480;' : 'color: #2d7ef7;'"
                  @click="changeIsKey(data, 'subj')"
                >
                  <i class="fas fa-key"></i>
                </span>
              </div>
            </template>
          </b-table>
          <div class="addWordDiv">
            <b-button class="addWordDiv__button" variant="primary"
              @click="addWordModal('subj')"
            >
              Добавить
            </b-button>
          </div>
        </b-col>
        <b-col col lg="1" class="typeCol">
          <div class="justify-content-md-center mt-3">
            <p class="text-primary text-center" style="font-weight: 700;">
              Тип
            </p>
            <b-form-select
              @input="subjectTypeChanged"
              :value="sent.subjs.type"
              :options="typeOptions"
            />
          </div>
        </b-col>
        <b-col col lg="2" class="relCol">
          <div class="justify-content-md-center mt-3">
            <p class="text-primary text-center" style="font-weight: 700;">
              Связь
            </p>
            <b-input @input="depChanged($event)" class="mt-3 mb-2" :value="sent.dep.text"></b-input>
            <b-form-select @input="depMandatoryChanged" :options="depOptions" :value="sent.dep.mandatory" />
          </div>
        </b-col>
        <b-col col lg="1" class="typeCol typeCol-right">
          <div class="justify-content-md-center mt-3">
            <p class="text-primary text-center" style="font-weight: 700;">
              Тип
            </p>
            <b-form-select 
              @change="objectTypeChanged"
              :value="sent.objs.type"
              :options="typeOptions" 
            />
          </div>
        </b-col>
        <b-col col lg="4">
          <b-table
            :items="sent.objs.objects"
            :fields="fields"
            responsive="sm"
          >
            <template v-slot:head(text)="data">
              <span class="text-primary">Объект</span>
            </template>
            <template v-slot:head(num)="data">
              <span class="text-primary">Число</span>
            </template>
            <template v-slot:head(action)="data">
              <span></span>
            </template>
            <template v-slot:cell(text)="data">
              <b-input @input="objectTextChanged(data, $event)" :value="data.item.text" />
            </template>
            <template v-slot:cell(num)="data">
              <b-form-select @input="objectNumChanged(data, $event)" :value="data.item.num" :options="numOptions" />
            </template>
            <template v-slot:cell(action)="data">
              <div class="actionsCell">
                <span
                  style="color: #d94343; cursor: pointer;"
                  @click="deleteWordModal(data, 'obj')"
                >
                  <i class="fas fa-times"></i>
                </span>
                <span
                  v-if="sent.objs.type === 'atr'"
                  style="cursor: pointer;"
                  :style="data.item.isKey ? 'color: #194480;' : 'color: #2d7ef7;'"
                  @click="changeIsKey(data, 'obj')"
                >
                  <i class="fas fa-key"></i>
                </span>
              </div>
            </template>
          </b-table>
          <div class="addWordDiv">
            <b-button class="addWordDiv__button" variant="primary"
              @click="addWordModal('obj')"
            >
              Добавить
            </b-button>
          </div>
        </b-col>
        <b-modal
            :id="`deleteWordModal`"
            title="Удаление слова"
            :ok-title="'Ок'"
            :cancel-title="'Отмена'"
            @ok="deleteWord"
          >
            <p>Вы действительно хотите убрать данное слово?</p>
          </b-modal>
          <b-modal
            :id="`addWordModal`"
            title="Добавление слова"
            :ok-title="'Добавить'"
            :cancel-title="'Отмена'"
            @ok="addWord"
          >
            <b-row>
              <b-col sm="3">
                <label :for="`wordText`">Слово:</label>
              </b-col>
              <b-col sm="9">
                <b-input v-model="wordForAdd" id="wordText" placeholder="Введите слово"/>
              </b-col>
            </b-row>
            <b-row class="mt-2">
              <b-col sm="3">
                <label :for="`wordNum`">Число:</label>
              </b-col>
              <b-col sm="9">
                <b-form-select v-model="addWordNum" :options="numOptions" id="wordNum" />
              </b-col>
            </b-row>
          </b-modal>
      </b-row>
    </b-container>
</template>

<script>

import _ from 'lodash'

import { mapMutations, mapActions, mapGetters } from 'vuex'

import VDiagram from '../Graph/VDiagram.vue'

export default {
  name: 'VERGeneration',
  components: {
    VDiagram,
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
    }
  },
  computed: {
    ...mapGetters({
      sents: 'ergeneration/getERSents',
      idx: 'ergeneration/getCurrentSent',
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
      setIdx: 'ergeneration/setCurrentSent',
      updateElement: 'ergeneration/updateElement',
      updateElementsType: 'ergeneration/updateElementsType',
      updateDep: 'ergeneration/updateDep',
      deleteERSent: 'ergeneration/deleteERSent',
      deleteERSentWord: 'ergeneration/deleteERSentWord',
      addERSentWord: 'ergeneration/addERSentWord',
      setIsNewER: 'ergeneration/setIsNewER',
    }),
    ...mapActions({
      sendERSents: 'ergeneration/sendERSents',
    }),
    goBack() {
      this.$router.push('./')
    },
    subjectTypeChanged(val) {
      this.updateElementsType({
        type: 'subj',
        elType: val,
      })
    },
    objectTypeChanged(val) {
      this.updateElementsType({
        type: 'obj',
        elType: val,
      })
    },
    subjectNumChanged(data, val) {
      const newEl = { ...data.item, num: val}
      this.updateElement({
        type: 'subj',
        oldEl: data.item,
        newEl,
      })
    },
    objectNumChanged(data, val) {
      const newEl = { ...data.item, num: val}
      this.updateElement({
        type: 'obj',
        oldEl: data.item,
        newEl,
      })
    },
    changeIsKey(data, type) {
      const newEl = { ...data.item, isKey: !data.item.isKey }
      this.updateElement({
        type,
        oldEl: data.item,
        newEl,
      })
    },
    deleteSentenceModal() {
      this.$bvModal.show(`deleteSentenceModal-${this.idx}`)
    },
    deleteSentence() {
      this.deleteERSent()
      if (this.sents.length === 1) {
        this.$router.push('./')
      }
    },
    depMandatoryChanged(val) {
      this.updateDep({
        ...this.sents[this.idx].dep,
        mandatory: val,
      })
    },
    deleteWordModal(data, type) {
      this.wordForDelete = data.item
      this.deleteWordType = type
      this.$bvModal.show(`deleteWordModal`)
    },
    deleteWord() {
      this.deleteERSentWord({
        type: this.deleteWordType,
        word: this.wordForDelete,
      })
      this.wordForDelete = null
      this.deleteWordType = null
    },
    addWordModal(type) {
      this.addWordType = type
      this.$bvModal.show(`addWordModal`)
    },
    addWord() {
      this.addERSentWord({
        type: this.addWordType,
        word: {
          text: this.wordForAdd,
          num: this.addWordNum,
          isKey: false,
        }
      })
      this.addWordType = null
      this.addWordNum = ''
      this.wordForAdd = ''
    },
    async generateER() {
      await this.sendERSents()

      this.setIsNewER(true)
      this.$router.push(`/projects/${this.$route.params.projectId}/er`)
    },
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

.actionsCell {
  display: flex;
  justify-content: center;

  span {
    margin-top: 8px;
  }

  span:nth-child(2n) {
    margin-left: 10px;
  }
}


</style>
