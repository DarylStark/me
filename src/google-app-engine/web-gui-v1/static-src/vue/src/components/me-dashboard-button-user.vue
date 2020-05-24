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
                <template v-for='item in $store.state.ui.menus.user'>
                    <router-link class='item' tag='div' v-bind:key='item.title' v-bind:to='item.dst' v-if='item.dst'>
                        <i v-bind:class='[ item.icon, "icon" ]'></i>
                        {{ item.title }}
                    </router-link>
                    <div class='item' v-bind:key='item.title' v-if='item.action' v-on:click.prevent='item.action'>
                        <i v-bind:class='[ item.icon, "icon" ]'></i>
                        {{ item.title }}
                    </div>
                </template>
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
    }
};
</script>
