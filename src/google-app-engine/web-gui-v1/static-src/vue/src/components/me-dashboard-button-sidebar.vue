<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
  <div id='me-dashboard-button-sidebar' v-if='$store.state.ui.sidebar_available'>
      <i class="ellipsis vertical icon"></i>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-dashboard-button-sidebar'
}
</script>