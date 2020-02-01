<template>
  <div v-if="reqs !== null" class="reqsList">
    <b-list-group>
      <b-list-group-item  v-for="(req, index) in Object.entries(reqs)" :key=index>
        <span class="reqList__item-text">
          {{ req[0] }}
        </span>
        <span>
          {{ req[1] }}
        </span>
      </b-list-group-item >
    </b-list-group>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'

export default {
  name: 'ClassifiedReqs',
  computed: {
    ...mapGetters({
      reqs: 'reqs/getReqs',
    }),
  },
  methods: {
  },
}
</script>

<style lang="scss" scoped>

.reqsList {
  height: 80vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

</style>
