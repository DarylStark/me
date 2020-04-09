<!-- Vue component for the a grid -->
<template>
  <h1 class='ui header' v-bind:class="{ inverted: inverted }">
    <slot></slot>
  </h1>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-h1',
  props: {
    inverted: {
      type: Boolean
    }
  }
}
</script>