<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
  <div id='me-dashboard-button-options'>

    <div class='ui pointing dropdown top right' ref='dropdown'>
      <i class='ellipsis vertical icon'></i>
      <div class='menu'>
        <div class='item' v-if='$store.state.ui.sidebar_available' v-on:click='toggle_sidebar'>
          <i class='bars icon'></i>
            <span v-if='!$store.state.ui.sidebar_open'>Show sidebar</span>
            <span v-if='$store.state.ui.sidebar_open'>Hide sidebar</span>
        </div>
        <div class='divider' v-if='$store.state.ui.sidebar_available'></div>
        <div class='item' v-on:click='command_palette'>
          <i class='terminal icon'></i>
            Command palette
        </div>
        <div class='item' v-on:click='reload_page'>
          <i class='redo icon'></i>
            Reload page
        </div>
      </div>
    </div>

  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
import '../../semantic/dist/semantic'
import '../../semantic/dist/components/dropdown'
import eventbus from '../eventbus'

export default {
  name: 'me-dashboard-button-options',
  mounted: function() {
    // Add the 'dropdown' functionality of Semantic UI to the dropdown
    $(this.$refs.dropdown).dropdown({ action: 'hide' });
  },
  methods: {
    toggle_sidebar: function() {
        // Toggle the side
        this.$store.commit('set_sidebar_state', !this.$store.state.ui.sidebar_open);
    },
    reload_page: function() {
      // Reload the page
      location.reload();
    },
    command_palette: function() {
      // Show the enable 2nd factor dialog
      eventbus.$emit('show_modal', 'modal_command_palette');
    }
  }
}
</script>