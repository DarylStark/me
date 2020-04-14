<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
  <div id='me-dashboard-button-user'>

    <div class="ui pointing dropdown top right" ref='dropdown'>
      <i class='user icon'></i>
      <span v-if='$store.state.ui.media_type != "phone"'>Daryl Stark</span>
      <div class="menu">
        <div class="header" v-if='$store.state.ui.media_type == "phone"'>
          <i class="user icon"></i>
          Daryl Stark
        </div>
        <div class="item">
          <i class="user circle icon"></i>
            Profile
        </div>
        <div class="item" v-on:click.prevent='logout'>
          <i class="sign out alternate icon"></i>
            Logout
        </div>
      </div>
    </div>

  </div>
</template>

<!-- The script that gets exported from the file -->
<script>

import '../../semantic/dist/semantic'
import '../../semantic/dist/components/dropdown'

export default {
  name: 'me-dashboard-button-user',
  mounted: function() {
    // Add the 'dropdown' functionality of Semantic UI to the dropdown
    $(this.$refs.dropdown).dropdown({ action: 'hide' });
  },
  methods: {
    logout: function() { console.log('logging out'); }
  }
}
</script>
