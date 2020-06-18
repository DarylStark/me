<script>
/* A global router for Vue */
import Vue from 'vue';
import VueRouter from 'vue-router';

// Import page
import me_dashboard from './pages/me-dashboard';
import me_feed from './pages/me-feed';
import me_notes from './pages/me-notes';
import me_userprofile from './pages/me-userprofile';
import me_api_clients from './pages/me-api-clients';
import me_api_help from './pages/me-api-help';
import me_search from './pages/me-search';
import me_sidebar_search from './sidebars/me-sidebar-search';

// Make sure Vue knows to use VueRouter
Vue.use(VueRouter);

// Create the Vue-router
export default new VueRouter({
    base: '/ui/',
    mode: 'history',
    linkExactActiveClass: 'active',
    routes: [
        { path: '/home', components: { default: me_dashboard } },
        { path: '/feed', components: { default: me_feed } },
        { path: '/notes', components: { default: me_notes } },
        { path: '/userprofile', components: { default: me_userprofile } },
        { path: '/api_clients', components: { default: me_api_clients } },
        { path: '/api_help', components: { default: me_api_help } },
        {
            path: '/search/:query',
            components: { default: me_search, sidebar: me_sidebar_search }
        }
    ]
});
</script>
