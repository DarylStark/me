<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
    <div id='me-dashboard-search' v-bind:class='{ active: this.$store.state.ui.search_active }'>
        <me-input icon='search' icon_position='right' id='search' placeholder='Search ...' ref='search' transparent='true' v-on:enter='start_search' v-on:escape='toggle_search' v-show='this.$store.state.ui.search_active'></me-input>
        <i class='search icon' v-if='!this.$store.state.ui.search_active' v-on:click='toggle_search'></i>
    </div>
</template>

<!-- The script that gets exported from the file -->
<script>
import me_input from './me-input';

export default {
    name: 'me-dashboard-search',
    components: {
        'me-input': me_input
    },
    data: function() {
        return {
            search_active: false
        };
    },
    methods: {
        toggle_search: function() {
            // Method to activate or deactive the search bar
            this.$store.commit('set_search_state', 'toggle');

            // Set focus to the search-input. Because Vue doesn't update the DOM immidiatly, we have to
            // wait for it to do so with the 'nextTick' method.
            this.$nextTick(function() {
                this.$refs.search.focus();
            });
        },
        start_search: function() {
            // Method to start the search
            // TODO: Implement
            console.log('Searching for "' + this.$refs.search.value + '"');
        }
    }
};
</script>