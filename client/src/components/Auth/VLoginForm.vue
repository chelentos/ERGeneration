<template>
  <div>
    <b-card class="mt-3 mx-auto loginFormCard" header-tag="header">
      <h5 slot="header" class="mb-0" align="center">Вход</h5>
      <b-form
        @submit.prevent="onSubmit"
      >
        <b-form-group
          label="Почта"
          label-for="emailInput"
        >
          <b-form-input
            id="emailInput"
            v-model="form.email"
            type="email"
            required
            placeholder="Введите почту"
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Пароль" label-for="passwordInput">
          <b-form-input
            v-model="form.password"
            type="password"
            required
            placeholder="Введите пароль"
          ></b-form-input>
        </b-form-group>
        <div>
          <p>
            Еще не зарегестрированы?
            <a href="/#/register">Пройти регистрацию</a>
          </p>
          <div align="right">
            <b-button
              type="submit"
              variant="outline-primary"
              align="center"
              class="loginFormCard__loginButton"
            >
              <i class="fas fa-sign-in" aria-hidden="true"></i> Войти
            </b-button>
          </div>
        </div>
      </b-form>
    </b-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'VLoginForm',
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
    }
  },
  mounted() {
  },
  methods: {
    ...mapActions({
      login: 'currentUser/login',
    }),
    onSubmit() {
      this.login(this.form).then(() => {
        this.$router.push('/')
      })
    },
  },
  computed: {
  },
}
</script>

<style scoped>
  .card-header{
    background-color: #2d7ef7;
    color: white;
  }

  .card{
    width: 60vw;
    max-width: 900px;
  }

  .loginFormCard__loginButton {
    float: right;
  }

  @media only screen and (max-width: 768px) {
    .card{
      width: 90vw;
    }
  }

  @media only screen and (max-width: 480px) {
    .loginFormCard__loginButton {
      width: 100%;
      margin-top: 10px;
    }
  }
</style>
