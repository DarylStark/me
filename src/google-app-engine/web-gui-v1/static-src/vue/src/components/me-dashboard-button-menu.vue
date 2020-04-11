<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
  <div id='me-dashboard-button-menu' v-on:click='toggle_menu' v-bind:class="{ hide_menu: !show_menu }">
      <i class='bars icon'></i>
      <span v-if='show_menu'>Me</span>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-dashboard-button-menu',
  data: function() {
    return {
        show_menu: true
    };
  },
  props: {
  },
  methods: {
      toggle_menu: function() {
          // Toggle the menu
          this.show_menu = !this.show_menu;
      }
  }
}
</script>