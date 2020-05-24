<!-- Vue component for the login-form -->
<template>
    <div id='me-dashboard-header'>
        <me-dashboard-button-menu v-show='!this.$store.state.ui.search_active'></me-dashboard-button-menu>
        <me-dashboard-search></me-dashboard-search>
        <me-dashboard-button-user v-show='!this.$store.state.ui.search_active'></me-dashboard-button-user>
        <me-dashboard-button-options v-show='!this.$store.state.ui.search_active'></me-dashboard-button-options>
    </div>
</template>

<script>
import me_dashboard_button_menu from './me-dashboard-button-menu';
import me_dashboard_search from './me-dashboard-search';
import me_dashboard_button_user from './me-dashboard-button-user';
import me_dashboard_button_options from './me-dashboard-button-options';

export default {
    name: 'me-dashboard-header',
    components: {
        'me-dashboard-button-menu': me_dashboard_button_menu,
        'me-dashboard-search': me_dashboard_search,
        'me-dashboard-button-user': me_dashboard_button_user,
        'me-dashboard-button-options': me_dashboard_button_options
    }
};
</script>