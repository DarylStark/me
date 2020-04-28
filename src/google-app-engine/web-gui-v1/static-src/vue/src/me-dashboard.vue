<!-- Vue component for the login-form -->
<template>
  <div id='me-dashboard'>
    <!-- Header area -->
    <me-dashboard-header></me-dashboard-header>
    <div id='me-dashboard-menu-and-content'>
      <!-- Content area -->
      <me-dashboard-main-menu></me-dashboard-main-menu>
      <me-dashboard-content></me-dashboard-content>
      <me-dashboard-sidebar></me-dashboard-sidebar>
    </div>
    <!-- Dialogs -->
    <me-modal-changepassword></me-modal-changepassword>
    <me-modal-disable-2nd-factor></me-modal-disable-2nd-factor>
    <me-modal-enable-2nd-factor></me-modal-enable-2nd-factor>
    <me-modal-command-palette></me-modal-command-palette>
  </div>
</template>

<script>
// Import the needed components
import Vue from 'vue'
import jquery from 'jquery'
import me_dashboard_header from './components/me-dashboard-header'
import me_dashboard_main_menu from './components/me-dashboard-main-menu'
import me_dashboard_content from './components/me-dashboard-content'
import me_dashboard_sidebar from './components/me-dashboard-sidebar'
import me_modal_changepassword from './modals/me-modal-changepassword'
import me_modal_disable_2nd_factor from './modals/me-modal-disable-2nd-factor'
import me_modal_enable_2nd_factor from './modals/me-modal-enable-2nd-factor'
import me_modal_command_palette from './modals/me-modal-command-palette'
import vue_cookies from 'vue-cookies'
import me_api_call from './me/api_call'

// Enable the use of the Vue Cookies module
Vue.use(vue_cookies);

// Export the dashboard
export default {
  name: 'me-dashboard',
  components: {
    'me-dashboard-header': me_dashboard_header,
    'me-dashboard-main-menu': me_dashboard_main_menu,
    'me-dashboard-content': me_dashboard_content,
    'me-dashboard-sidebar': me_dashboard_sidebar,
    'me-modal-changepassword': me_modal_changepassword,
    'me-modal-disable-2nd-factor': me_modal_disable_2nd_factor,
    'me-modal-enable-2nd-factor': me_modal_enable_2nd_factor,
    'me-modal-command-palette': me_modal_command_palette
  },
  methods: {
    set_media_type: function() {
      // TODO: Maybe move this to the store? Discussable...

      // Function to set the window size in the Vue-object and the 'device-type'. The 'device-type' can
      // be either 'desktop', 'table' or 'phone'.
      let media_type = null;

      // Search for the correct media-type
      if (window.matchMedia('only screen and (max-width: 1024px)').matches) { media_type = 'tablet'; }
      if (window.matchMedia('only screen and (max-width: 799px)').matches) { media_type = 'phone'; }
      if (window.matchMedia('only screen and (min-width: 1024px)').matches) { media_type = 'desktop'; }

      // Set the media type in the store
      this.$store.commit('set_media_type', media_type);
    }
  },
  created: function() {
    // When creating this object, we can set the correct values for the page

    // Set the media-type
    this.set_media_type();

    // Create a variable that can be used as 'this' in the callbacks that change the context of the
    // 'this' element
    let vue_this = this;

    // Set the environment for the application. We retrieve this from a cookie
    this.$store.commit('set_environment', $cookies.get('environment'));

    // Set the user token for the application. We retrieve this from a cookie
    this.$store.commit('set_user_token', $cookies.get('user_token'));

    // Update the user object in the store. This is used to set the users name on the page
    this.$store.commit('api_update_user_object');

    // Verify the user token. When we do this, we get the User Token object from the API in
    // response.
    me_api_call({
      group: 'aaa', endpoint: 'verify_user_token',
      method: 'GET'
    }).then(function(data) {
      // We got the data. Check if the description for the session is filled in
      if (data['data']['object']['description'] == null) {
        $('body').toast({
          position: 'bottom center',
          message: 'This session has no name yet. You can set a name for this session on your user profile.',
          closeIcon: true,
          displayTime: 'auto',
          showIcon: 'user'
        });
      }
    }).catch(function(data) {
      // Something went wrong
      console.log(data);

      // TODO: Error message
    });

    // Add a handler to the resize-event of the 'window' object so we can see when the user resized
    // the window
    jquery(window).resize(function() {
      // Set the device type again
      vue_this.set_media_type();
    });

    // Add a handler to the click-event of the 'window'. This handler will check if the user clicked
    // outside of the menu and hide the menu if this is a mobile phone.
    jquery(window).click(function(event) {
      // Check if the user clicked inside the content
      if(document.getElementById('me-dashboard-main-menu') != null) {
        if (document.getElementById('me-dashboard-content').contains(event.target) && 
            (vue_this.$store.state.ui.media_type == 'phone' || vue_this.$store.state.ui.media_type == 'tablet')) {
          // If the device is phone, close the menu again
          vue_this.$store.commit('set_menu_state', false);
          vue_this.$store.commit('set_sidebar_state', false);
        }
      }
    });
  }
}
</script>
