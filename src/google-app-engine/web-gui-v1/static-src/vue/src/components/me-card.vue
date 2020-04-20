<!-- Vue component for the a card -->
<template>
  <div class='ui' v-bind:class='[ { raised: raised }, "card" ]' v-bind:id='id'>
    <div v-bind:class='{ padding: padding }'>
      <slot></slot>
    </div>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-card',
  props: {
    id: null,
    raised: { type: Boolean, default: false },
    padding: { type: Boolean, default: false }
  }
}
</script>