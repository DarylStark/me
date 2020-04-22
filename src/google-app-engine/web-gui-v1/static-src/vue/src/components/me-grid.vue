<!-- Vue component for the a grid -->
<template>
  <div v-bind:class='[ "me-grid", { "vcenter": vcenter, "hcenter": hcenter, "pageheight": pageheight } ]'>
    <slot></slot>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-grid',
  props: {
    vcenter: { type: Boolean, default: false },
    hcenter: { type: Boolean, default: false },
    pageheight: { type: Boolean, default: false }
  }
}
</script>