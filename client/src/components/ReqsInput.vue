<template>
  <div>
    <div class="reqsInput">
      <b-form-textarea
        id="textarea"
        v-model="text"
        placeholder="Введите требования"
        rows="3"
        max-rows="6"
        class="reqsInput__area"
      ></b-form-textarea>
      <b-button class="reqsInput__button" @click="onReqsInputSubmit">
        Отправить
      </b-button>
    </div>
  </div>
</template>

<script>

import { mapActions, mapGetters } from 'vuex'
import '../ASRlibs/annyang'

window.annyang = require('annyang')

export default {
  name: 'ReqsInput',
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
      reqs: 'reqs/getReqs',
    }),
  },
  methods: {
    ...mapActions({
      sendReqs: 'reqs/sendReqs',
    }),
    onReqsInputSubmit() {
      // eslint-disable-next-line no-useless-escape
      this.sendReqs(this.text.match(/[^\.!\?]+[\.!\?]+/g)).then(() => {
        this.$router.push('reqs')
      })
    },
  },
  created() {
    if (window.annyang) {
      const { annyang } = window

      annyang.setLanguage('ru')

      const commands = {
        'привет *rec': (rec) => {
          this.text += this.text.length > 0 ? ` ${rec}.` : `${rec}.`
        },
      };

      // Add our commands to annyang
      annyang.addCommands(commands);

      // Start listening.
      annyang.start();
    }
  },
}
</script>

<style lang="scss" scoped>

.reqsInput {
  height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;

  &__area {
    width: 50%;
  }

  &__button {
    margin-left: 10px;
  }
}

</style>
