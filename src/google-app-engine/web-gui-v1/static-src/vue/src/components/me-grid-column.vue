<!-- Vue component for the a column in a grid -->
<template>
  <div class='column'>
    <slot></slot>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-grid-column'
}
</script>