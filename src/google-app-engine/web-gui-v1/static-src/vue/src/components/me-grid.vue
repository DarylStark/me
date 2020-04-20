<!-- Vue component for the a grid -->
<template>
  <div v-bind:class='[ "ui", { "middle aligned": vcenter, "center aligned": hcenter }, "grid" ]'>
    <slot></slot>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-grid',
  props: {
    vcenter: { type: Boolean, default: false },
    hcenter: { type: Boolean, default: false }
  }
}
</script>