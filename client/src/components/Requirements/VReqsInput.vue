<template>
    <b-container class="mt-5">
      <b-row class="justify-content-md-center">
        <b-col col lg="8">
          <div class="reqsInput mt-5">
            <b-form-textarea
              id="textarea"
              v-model="text"
              placeholder="Введите требования"
              rows="8"
              max-rows="10"
              class="reqsInput__area"
            ></b-form-textarea>
            <div class="buttonsBlock mt-2">
              <b-button
                class="reqsInput__button mr-2"
                variant="primary"
                @click="onReqsInputSubmit"
              >
                Отправить
              </b-button>
              <b-button
                class="reqsInput__button"
                variant="dark"
                @click="goBack"
              >
                Отмена
              </b-button>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

import '../../ASRlibs/annyang'

window.annyang = require('annyang')

export default {
  name: 'VReqsInput',
  data() {
    return {
      text: '',
      listening: false,
      debug: true,
      userSaid: '',
      registeredCommands: [],
    }
  },
  computed: {
    ...mapGetters({
      project: 'projects/getProject',
    }),
  },
  created() {
    if (window.annyang) {
      const { annyang } = window

      annyang.setLanguage('ru')

      annyang.addCallback('result', (phrases) => {
        const res = phrases[0]
        this.text += `${res.toUpperCase().charAt(0)}${res.split(' ')[0].slice(1)} ${res.split(' ').slice(1).join(' ')}. `
      });

      // Start listening.
      annyang.start({ autoRestart: true, continuous: false })
    }
  },
  beforeDestroy() {
    const { annyang } = window
    annyang.abort()
  },
  methods: {
    ...mapActions({
      loadReqs: 'projects/loadReqs',
    }),
    onReqsInputSubmit() {
      this.loadReqs({
        projectId: this.$route.params.projectId,
        reqs: this.text.match(/[^.!?]+[.!?]+/g),
      }).then(() => {
        this.$router.push('./')
      })
    },
    goBack() {
      this.$router.push('./')
    }
  },
}
</script>

<style scoped>

.buttonsBlock {
  width: 100%;
  display: flex;
  justify-content: center;
}

</style>
