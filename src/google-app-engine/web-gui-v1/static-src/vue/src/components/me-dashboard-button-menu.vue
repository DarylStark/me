<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
  <div id='me-dashboard-button-menu' v-on:click='toggle_menu' v-bind:class="{ hide_menu: !$store.state.ui.menu_open }">
      <i class='bars icon'></i>
      <span v-if='$store.state.ui.menu_open'>{{ title }}</span>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-dashboard-button-menu',
  computed: {
    title: function() {
      if (this.$store.state.app.environment != 'production') {
        return 'Me (' + this.$store.state.app.environment + ')';
      }
      return 'Me'
    }
  },
  methods: {
      toggle_menu: function() {
          // Toggle the menu
          this.$store.commit('set_menu_state', 'toggle');
      }
  }
}
</script>