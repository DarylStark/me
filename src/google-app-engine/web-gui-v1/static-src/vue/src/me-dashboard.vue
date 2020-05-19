<!-- Vue component for the login-form -->
<template>
  <div id='me-dashboard'>
    <!-- Splashscreen -->
    <transition name='slide-fade'>
      <me-splashscreen v-if='!done_loading'></me-splashscreen>
    </transition>
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
    <me-modal-set-session-title></me-modal-set-session-title>
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
import me_modal_set_session_title from './modals/me-modal-set-session-title'
import me_splashscreen from './components/me-splashscreen'
import vue_cookies from 'vue-cookies'
import me_api_call from './me/api_call'
import eventbus from './eventbus'

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
    'me-modal-command-palette': me_modal_command_palette,
    'me-modal-set-session-title': me_modal_set_session_title,
    'me-splashscreen': me_splashscreen
  },
  data: function() {
    return {
      'done_loading': false,
      'loading_watcher': 0,
      'loading_state': {
        'user_profile': false,
        'user_settings': false,
        'other': false
      }
    }
  },
  watch: {
    loading_watcher: function() {
      // Set counters to zero
      let done = 0;
      let not_done = 0;

      // Check how far we are
      for (let key in this.loading_state) {
        if (this.loading_state[key] === true) {
          done++;
        } else {
          not_done++;
        }
      }

      // If we are done, set 'done_loading' to true so the splashscreen can go away
      if (not_done == 0) { this.done_loading = true; }
    }
  },
  methods: {
    set_media_type: function() {
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
    this.$store.commit('set_user_token', { 'token': $cookies.get('user_token') });

    // Update the user object in the store. This is used to set the users name on the page
    this.$store.commit('api_update_user_object');

    // Verify the user token. When we do this, we get the User Token object from the API in
    // response.
    this.$store.state.app.loading_text = 'Verifying user token';
    me_api_call({
      group: 'aaa', endpoint: 'verify_user_token',
      method: 'GET'
    }).then(function(data) {
      vue_this.loading_state.user_profile = true;
      vue_this.loading_watcher++;
      
      // Save the data in the store
      vue_this.$store.commit('set_user_token', data['data']['object']);

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

      // The user-token was correct. That means we can now retrieve the user settings from the
      // client API
      vue_this.$store.state.app.loading_text = 'Retrieving user settings';
      vue_this.$store.commit('update_user_settings', {
        success: function() {
          vue_this.loading_state.user_settings = true;
          vue_this.loading_watcher++;
        },
        failed: function() {
          $('body').toast({
            position: 'bottom center',
            message: 'Couldn\'t retrieve your user settings',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        }
      });
    }).catch(function(data) {
      $('body').toast({
        position: 'bottom center',
        message: 'Couldn\'t retrieve your user token',
        closeIcon: true,
        displayTime: 'auto',
        showIcon: 'user',
        class: 'error'
      });
    });

    this.$store.state.app.loading_text = 'Setting handlers';

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
          vue_this.$store.commit('set_search_state', false);
        }
      }
    });

    // Add a handler to 'keyup' events. When the user does a keyup event we can do special actions,
    // like opening the command pallete, hide the menu, hide the sidebar, etc.
    jquery(document).keyup(function(event) {
      // CTRL+SHIFT+Q opens the Command Palette
      if (event.ctrlKey && event.key == 'Q') {
        eventbus.$emit('show_modal', 'modal_command_palette');
      }

      // CTRL+SHIFT+A: Toggle the menu
      if (event.ctrlKey && event.key == 'A') {
        vue_this.$store.commit('set_menu_state', 'toggle');
      }

      // CTRL+SHIFT+A: Toggle the sidebar
      if (event.ctrlKey && event.key == 'S') {
        vue_this.$store.commit('set_sidebar_state', 'toggle');
      }
    });

    vue_this.loading_state.other = true;
    vue_this.loading_watcher++;
  }
}
</script>
