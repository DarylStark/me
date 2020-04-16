<!-- Vue component for the login-form -->
<template>
  <div id='me-dashboard-sidebar' v-if='$store.state.ui.sidebar_available' v-bind:class='{ floating: $store.state.ui.media_type != "desktop", hidden: !$store.state.ui.sidebar_open }'>
  </div>
</template>

<script>
export default {
  name: 'me-dashboard-sidebar'
}
</script>