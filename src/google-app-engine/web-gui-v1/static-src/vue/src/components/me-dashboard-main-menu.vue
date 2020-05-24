<!-- Vue component for the login-form -->
<template>
    <div id='me-dashboard-main-menu' v-bind:class='{ floating: $store.state.ui.media_type != "desktop", hidden: !$store.state.ui.menu_open }'>
        <me-dashboard-main-menu-main></me-dashboard-main-menu-main>
        <me-dashboard-main-menu-notes></me-dashboard-main-menu-notes>
    </div>
</template>

<script>
import me_dashboard_main_menu_main from './me-dashboard-main-menu-main';
import me_dashboard_main_menu_notes from './me-dashboard-main-menu-notes';

// Export the main menu
export default {
    name: 'me-dashboard-main-menu',
    components: {
        'me-dashboard-main-menu-main': me_dashboard_main_menu_main,
        'me-dashboard-main-menu-notes': me_dashboard_main_menu_notes
    }
};
</script>