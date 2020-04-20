<template>
  <button v-bind:class='[ "ui", { primary: primary}, "button" ]'>
      <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'me-button',
  props: {
      primary: { type: Boolean, default: false }
  }
}
</script>