<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
  <div id='me-dashboard-button-menu' v-on:click='toggle_menu' v-bind:class="{ hide_menu: !$store.state.ui.menu_open }">
      <i class='bars icon'></i>
      <span v-if='$store.state.ui.menu_open'>Me</span>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-dashboard-button-menu',
  methods: {
      toggle_menu: function() {
          // Toggle the menu
          this.$store.commit('set_menu_state', !this.$store.state.ui.menu_open);
      }
  }
}
</script>