<template>
  <button v-bind:class='[ "ui", { primary: primary}, { disabled: disabled }, "button" ]' v-on:click='$emit("click");'>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'me-button',
  props: {
      primary: { type: Boolean, default: false },
      disabled: { type: Boolean, default: false }
  }
}
</script>
