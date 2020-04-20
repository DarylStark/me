<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
  <div id='me-dashboard-button-user'>

    <div class="ui pointing dropdown top right" ref='dropdown'>
      <i class='user icon'></i>
      <!-- TODO: Display the name of the user instead of a static name -->
      <span v-if='$store.state.ui.media_type != "phone"'>Daryl Stark</span>
      <div class="menu">
        <div class="header" v-if='$store.state.ui.media_type == "phone"'>
          <i class="user icon"></i>
          Daryl Stark
        </div>
        <div class="item">
          <router-link to='/userprofile'>
            <i class="user circle icon"></i>
            Profile
          </router-link>
        </div>
        <div class="item">
          <i class="pen icon"></i>
          Rename session
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
import me_api_call from '../me/api_call'

export default {
  name: 'me-dashboard-button-user',
  mounted: function() {
    // Add the 'dropdown' functionality of Semantic UI to the dropdown
    $(this.$refs.dropdown).dropdown({ action: 'hide' });
  },
  methods: {
    logout: function() {
      me_api_call({
        group: 'aaa',
        endpoint: 'remove_user_token',
        method: 'DELETE'
      }).then(function(data) {
        // Logged out! Remove the cookie
        $cookies.remove('user_token');

        // Redirect the user to the loginpage
        location.href = '/ui/login';
      }).catch(function(data) {
        // Something went wrong
        console.log(data);

        // TODO: Error message
      });
    }
  }
}
</script>
