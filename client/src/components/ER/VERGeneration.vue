<template>
    <b-container class="mt-5">
      <b-row class="justify-content-md-center">
        <b-col col lg="10">
        </b-col>
      </b-row>
    </b-container>
</template>

<script>

import { mapMutations, mapActions, mapGetters } from 'vuex'

export default {
  name: 'VERGeneration',
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters({
    }),
  },
  mounted() {
    this.fetchProject(this.$route.params.projectId)
  },
  methods: {
    ...mapMutations({
    }),
    ...mapActions({
    }),
  },
}
</script>

<style scoped>

</style>
