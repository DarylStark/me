<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
    <div id='me-dashboard-button-user'>
        <div class='ui pointing dropdown top right' ref='dropdown'>
            <i class='user icon'></i>
            <span v-if='$store.state.ui.media_type != "phone"'>{{ $store.state.api_data.user_object.fullname }}</span>
            <div class='menu'>
                <div class='header' v-if='$store.state.ui.media_type == "phone"'>
                    <i class='user icon'></i>
                    {{ $store.state.api_data.user_object.fullname }}
                </div>
                <router-link class='item' tag='div' to='/userprofile'>
                    <i class='user circle icon'></i>
                    Profile
                </router-link>
                <div class='item' v-on:click.prevent='rename_session'>
                    <i class='pen icon'></i>
                    Rename session
                </div>
                <div class='item' v-on:click.prevent='logout'>
                    <i class='sign out alternate icon'></i>
                    Logout
                </div>
            </div>
        </div>
    </div>
</template>

<!-- The script that gets exported from the file -->
<script>
import '../../semantic/dist/semantic';
import '../../semantic/dist/components/dropdown';
import eventbus from '../eventbus';
import me_api_call from '../me/api_call';

export default {
    name: 'me-dashboard-button-user',
    mounted: function() {
        // Add the 'dropdown' functionality of Semantic UI to the dropdown
        $(this.$refs.dropdown).dropdown({ action: 'hide' });
    },
    methods: {
        logout: function() {
            me_api_call({
                group: 'aaa',
                endpoint: 'remove_user_token',
                method: 'DELETE'
            })
                .then(function(data) {
                    // Logged out! Remove the cookie
                    $cookies.remove('user_token');

                    // Redirect the user to the loginpage
                    location.href = '/ui/login';
                })
                .catch(function(data) {
                    $('body').toast({
                        position: 'bottom center',
                        message: "Couldn't remove your session",
                        closeIcon: true,
                        displayTime: 'auto',
                        showIcon: 'user',
                        class: 'error'
                    });
                });
        },
        rename_session: function() {
            eventbus.$emit('show_modal', 'modal_set_session_title');
        }
    }
};
</script>
