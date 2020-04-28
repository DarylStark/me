<!-- Vue component for the login-form -->
<template>
  <div v-bind:class='[ "me-flexline", extra_class ]'>
      <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'me-flexline',
  props: {
    extra_class: { type: String }
  }
}
</script>