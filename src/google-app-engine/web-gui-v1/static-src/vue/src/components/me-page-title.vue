<template>
  <div class='me-page-title'>
    <div class='title'>
      <i v-bind:class='[ { icon: icon }, icon ]' v-if='icon'></i>
      <slot></slot>
    </div>
    <div class='actions'>
      <slot name='actions'></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'me-page-title',
  props: {
      icon: { type: String, default: false }
  }
}
</script>
