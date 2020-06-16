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

// Make sure Vue knows to use VueRouter
Vue.use(VueRouter);

// Create the Vue-router
export default new VueRouter({
    base: '/ui/',
    mode: 'history',
    linkExactActiveClass: 'active',
    routes: [
        { path: '/home', component: me_dashboard },
        { path: '/feed', component: me_feed },
        { path: '/notes', component: me_notes },
        { path: '/userprofile', component: me_userprofile },
        { path: '/api_clients', component: me_api_clients },
        { path: '/api_help', component: me_api_help },
        { path: '/search/:query', component: me_search }
    ]
});
</script>
