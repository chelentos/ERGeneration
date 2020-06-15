<template>
    <div class="app">
        <v-navbar class="navbar-block">
          <b-navbar-nav>
            <b-nav-item v-if="currentUser" class="px-2" href="/#/projects">Мои проекты</b-nav-item>
          </b-navbar-nav>

          <b-navbar-nav class="ml-auto">
            <b-nav-item v-if="currentUser"
              @click="onLogoutClicked" class="mr-2"
            >
              Выход
            </b-nav-item>
            <b-nav-item v-else class="mr-2" href="/#/login">Вход</b-nav-item>
          </b-navbar-nav>
        </v-navbar>
        <div class="app-body">
            <main class="main">
                <div style="display: flex; align-items: stretch;">
                  <div v-show="isErGeneration" class="generationArrowWrapper">
                    <p
                      :class="idx === 0 ? 'generationArrow generationArrow-off' : 'generationArrow'">
                      <span
                        @click="goBack"
                        style="font-size: 30px;"
                      >
                        <i class="fas fa-chevron-left"></i>
                      </span>
                    </p>
                  </div>
                  <div class="container-fluid h-100">
                    <router-view/>
                  </div>
                  <div v-show="isErGeneration" class="generationArrowWrapper">
                    <p 
                      :class="idx === sents.length - 1 ? 'generationArrow generationArrow-off' : 'generationArrow'">
                      <span
                        @click="goForward"
                        style="font-size: 30px;"
                      >
                        <i class="fas fa-chevron-right"></i>
                      </span>
                    </p>
                  </div>
                </div>                
            </main>
        </div>
    </div>
</template>

<script>
import { mapMutations, mapActions, mapGetters } from 'vuex'
import VNavbar from './VNavbar.vue'

export default {
  name: 'AppContainer',
  data() {
    return {
      windowWidth: 0,
    }
  },
  props: {
    navItems: {
      type: Array,
      default() {
        return []
      },
    },
  },
  components: {
    VNavbar,
  },
  computed: {
    ...mapGetters({
      currentUser: 'currentUser/getCurrentUser',
      sents: 'ergeneration/getERSents',
      idx: 'ergeneration/getCurrentSent',
    }),
    isErGeneration() {
      return this.$route.path.includes('er_generation')
    },
  },
  methods: {
    ...mapMutations({
      setCurrentUser: 'currentUser/setCurrentUser',
      setIdx: 'ergeneration/setCurrentSent',
    }),
    ...mapActions({
      logout: 'currentUser/logout',
    }),
    onLogoutClicked() {
      this.logout().then(() => {
        this.setCurrentUser(null)
        this.$router.push('/')
      })
    },
    goForward() {
      if (this.idx < this.sents.length - 1) {
        this.setIdx(this.idx + 1)
      }
    },
    goBack() {
      if (this.idx > 0) {
        this.setIdx(this.idx - 1)
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.app-body {
  margin-top: 20px;
}

.app-header{
  min-width: 320px !important;
}

.generationArrowWrapper {
  height: 600px;
  width: 150px;
  display: flex;
  justify-content: center;

  .generationArrow {
    margin: auto;
    cursor: pointer;

    &-off {
      color: grey;
      cursor: default;
    }
  }
}

@media screen and (max-width: 992px) {
  .navbar-block {
    position: relative !important;
  }

  .app-body {
    margin-top: 0;
  }
}

@media screen and (min-width: 575px) {
  .navbar-block {
    z-index: 200
  }
}
</style>
