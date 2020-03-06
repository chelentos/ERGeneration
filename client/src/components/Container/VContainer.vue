<template>
    <div class="app">
        <v-navbar class="navbar-block">
          <b-navbar-nav v-if="$router.app._route.fullPath === '/'">
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
                <div class="container-fluid h-100">
                  <router-view/>
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
    }),
  },
  methods: {
    ...mapMutations({
      setCurrentUser: 'currentUser/setCurrentUser',
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
  },
}
</script>

<style scoped>
.app-body {
  margin-top: 80px;
}

.app-header{
  min-width: 320px !important;
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
