// Imports
import Vue from 'vue'
import store from './store'
import router from './router'
import me_dashboard from './me-dashboard.vue'

// TODO: Remove this before deploying to production
Vue.config.devtools = true;

// Create the Vue object for the 'me-dashboard'
var vue_dashboard = new Vue({
  el: 'div#app-dashboard',
  router,
  store,
  render: function render(h) {
    return h(me_dashboard);
  }
});
