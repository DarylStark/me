<!-- Vue component for the login-form -->
<template>
  <div id='me-dashboard'>
    <!-- Component -->
    <me-dashboard-header></me-dashboard-header>
    <!-- /Component -->
    <p>{{ $store.state.ui.menu_open }}</p>
    <p>{{ $store.state.ui.media_type }}</p>
  </div>
</template>

<script>
// Import the needed components
import jquery from 'jquery'
import store from './store'
import me_dashboard_header from './components/me-dashboard-header'

// Export the dashboard
export default {
  name: 'me-dashboard',
  store,                  // Makes sure the store is usable in components
  components: {
    'me-dashboard-header': me_dashboard_header
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