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
            <div class="mx-auto mt-2" style="width: 100px;">
              <b-button class="reqsInput__button" @click="onReqsInputSubmit">
                Отправить
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

      // Add our commands to annyang
      // annyang.addCommands(commands);

      annyang.addCallback('result', (phrases) => {
        console.log(phrases)
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
  },
}
</script>

<style scoped>
</style>
