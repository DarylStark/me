<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
    <div id='me-dashboard-search' v-bind:class='{ active: this.$store.state.ui.search_active }'>
        <me-input icon='search' icon_position='right' id='search' placeholder='Search ...' ref='search' transparent='true' v-model='query' v-on:enter='start_search' v-on:escape='toggle_search' v-show='this.$store.state.ui.search_active' value='test'></me-input>
        <i class='search icon' v-on:click='toggle_search' v-show='!this.$store.state.ui.search_active'></i>
    </div>
</template>

<script>
import me_input from './me-input';

export default {
    name: 'me-dashboard-search',
    components: {
        'me-input': me_input
    },
    data: function() {
        return {
            search_active: false,
            query: null
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

            // Get the query
            let q = null;
            if (this.query != null) {
                q = this.query.trim();
            }

            // Check if the query is valid
            if (q != null && q != '') {
                // Navigate to the page
                this.$router.push('/search/' + q);
            }
        }
    }
};
</script>