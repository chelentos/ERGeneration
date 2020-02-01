module.exports = {
  root: true,
  parserOptions: {
    parser: 'babel-eslint',
  },
  env: {
    browser: true,
  },
  plugins: [
    'vue'
  ],
  extends: [
    'eslint:recommended',
    'plugin:vue/essential',
    '@vue/standard',
    'airbnb-base'
  ],
  rules: {
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    'import/no-unresolved': ['off', 'always', {
      js: 'never',
      vue: 'never'
    }],
    'semi': ["off", "always"],
    'linebreak-style': ["off", "unix"],
  },
  settings: {
    'import/resolver': {
      node: {
        extensions: ['.js','.jsx','.vue']
      }
    },
  }
}