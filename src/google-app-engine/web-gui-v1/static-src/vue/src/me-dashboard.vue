<!-- Vue component for the login-form -->
<template>
  <div id='me-dashboard'>
    <!-- Component -->
    <div id='me-dashboard-header'>
      <me-dashboard-button-menu></me-dashboard-button-menu>
      <!-- Component -->
      <div id='me-dashboard-search'>
        <i class='search icon'></i>
      </div>
      <!-- /Component -->
      <!-- Component -->
      <div id='me-dashboard-button-user'>
        <i class='user icon'></i>
      </div>
      <!-- /Component -->
      <!-- Component -->
      <div id='me-dashboard-button-sidebar'>
        <i class='filter icon'></i>
      </div>
      <!-- /Component -->
    </div>
    <!-- /Component -->
    <p>{{ $store.state.ui.menu_open }}</p>
    <p>{{ $store.state.ui.media_type }}</p>
  </div>
</template>

<script>
// Import the needed components
import jquery from 'jquery';
import me_dashboard_button_menu from './components/me-dashboard-button-menu'
import store from './store'

// Export the dashboard
export default {
  name: 'me-dashboard',
  store,                  // Makes sure the store is usable in components
  components: {
    'me-dashboard-button-menu': me_dashboard_button_menu
  },
  data: function() {
    return {}
  },
  methods: {
    set_media_type: function() {
      // TODO: Maybe move this to the store? Discussable...

      // Function to set the window size in the Vue-object and the 'device-type'. The 'device-type' can
      // be either 'desktop', 'table' or 'phone'.
      var media_type = null;

      // Search for the correct media-type
      if (window.matchMedia('only screen and (max-width: 700px)').matches) { media_type = 'phone'; }
      if (window.matchMedia('only screen and (min-width: 701px)').matches) { media_type = 'tablet'; }
      if (window.matchMedia('only screen and (min-width: 1000px)').matches) { media_type = 'desktop'; }

      // Set the media type in the store
      store.commit('set_media_type', media_type);
    }
  },
  created: function() {
    // When creating this object, we can set the correct values for the page

    // Set the media-type
    this.set_media_type();

    // Create a variable that can be used as 'this' in the callbacks that change the context of the
    // 'this' element
    var vue_this = this;

    // Add a handler to the resize-event of the 'window' object so we can see when the user resized
    // the window
    jquery(window).resize(function() {
      // Set the device type again
      vue_this.set_media_type();
    });
  }
}
</script>