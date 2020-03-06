<template>
    <b-navbar :type="type"
              :variant="variant"
              :toggle-breakpoint="toggleBreakpoint"
              :fixed="fixed"
              :sticky="sticky"
              class="app-header"
    >
      <slot></slot>
    </b-navbar>
</template>

<script>
export default {
  name: 'VNavbar',
  props: {
    toggleable: {
      type: String,
      default: 'md',
    },
    type: {
      type: String,
      default: 'dark',
    },
    variant: {
      type: String,
      default: 'primary',
    },
    toggleBreakpoint: {
      type: String,
      default: 'light',
    },
    fixed: {
      type: String,
      default: null,
    },
    sticky: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style scoped>
</style>
