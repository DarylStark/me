// Imports
import Vue from 'vue'
import me_dashboard from './me-dashboard.vue'

// Create the Vue object for the 'me-dashboard'
var vue_dashboard = new Vue({
  el: 'div#app-dashboard',
  render: function render(h) {
    return h(me_dashboard);
  }
});