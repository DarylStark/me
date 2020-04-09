<!-- Vue component for the a grid -->
<template>
  <div class='ui middle aligned center aligned grid'>
    <slot></slot>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-grid'
}
</script>