// Imports
import Vue from 'vue'
import me_loginform from './me-loginform.vue'

// Create the Vue object for the 'me-loginform'
new Vue({
  el: 'div#app-login',
  render: function render(h) {
    return h(me_loginform);
  }
});