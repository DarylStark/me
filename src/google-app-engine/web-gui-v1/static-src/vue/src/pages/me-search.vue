<template>
    <div id='me-content-search'>
        <me-page-title icon='search'>Search</me-page-title>
        <div class='loading' v-if='this.loading'>
            <div class='ui active inline loader'></div>
            <p>Loading search results</p>
        </div>
        <me-grid class='results' v-if='!this.loading && this.results'>
            <me-cell class='no_results' v-bind:span='12' v-if='results.length == 0'>
                <i class='times icon'></i>
                No results
            </me-cell>
            <me-cell padding v-bind:span='12'>
                <me-card class='results_api_user_token' raised v-if='results_api_user_token.length > 0' wide>
                    <me-h1 inverted>User tokens</me-h1>
                    <p>
                        Found
                        <b>{{ results_api_user_token.length }}</b>
                        user
                        <template v-if='results_api_user_token.length > 1'>tokens</template>
                        <template v-if='results_api_user_token.length == 1'>token</template>
                    </p>
                    <me-flexline v-bind:key='result.id' v-for='result in results_api_user_token'>
                        <div class='icon'>
                            <i class='key icon'></i>
                        </div>
                        <div class='grower'>{{ result.description }}</div>
                    </me-flexline>
                    <p class='actions'>
                        <me-button v-on:click='go_to_user_profile'>Go to user profile</me-button>
                    </p>
                </me-card>
            </me-cell>
            <me-cell padding v-bind:span='12'>
                <me-card class='results_api_client_token' raised v-if='results_api_client_token.length > 0' wide>
                    <me-h1 inverted>API clients</me-h1>
                    <p>
                        Found
                        <b>{{ results_api_client_token.length }}</b>
                        client
                        <template v-if='results_api_client_token.length > 1'>tokens</template>
                        <template v-if='results_api_client_token.length == 1'>token</template>
                    </p>
                    <me-flexline v-bind:key='result.id' v-for='result in results_api_client_token'>
                        <div class='icon'>
                            <i class='key icon'></i>
                        </div>
                        <div class='grower'>{{ result.app_name }}</div>
                    </me-flexline>
                    <p class='actions'>
                        <me-button v-on:click='go_to_api_clients'>Go to API clients</me-button>
                    </p>
                </me-card>
            </me-cell>
        </me-grid>
    </div>
</template>

<script>
import me_page_title from '../components/me-page-title';
import me_api_call from '../me/api_call';
import me_api_client from '../components/me-api-client';
import me_card from '../components/me-card';
import me_grid from '../components/me-grid';
import me_cell from '../components/me-cell';
import me_h1 from '../components/me-h1';
import me_flexline from '../components/me-flexline';
import me_button from '../components/me-button';

export default {
    name: 'me-content-search',
    components: {
        'me-page-title': me_page_title,
        'me-api-client': me_api_client,
        'me-card': me_card,
        'me-grid': me_grid,
        'me-cell': me_cell,
        'me-h1': me_h1,
        'me-flexline': me_flexline,
        'me-button': me_button
    },
    data: function() {
        return {
            loading: true,
            results: null
        };
    },
    computed: {
        results_api_client_token: function() {
            return this.results.filter(function(element) {
                return element._type == 'api_client_token';
            });
        },
        results_api_user_token: function() {
            return this.results.filter(function(element) {
                return element._type == 'api_user_token';
            });
        }
    },
    created: function() {
        // We do need a sidebar on this page. Enable it.
        this.$store.commit('set_sidebar_availability', true);

        // Get the results
        this.get_results();
    },
    beforeRouteUpdate(to, from, next) {
        next();
        this.get_results();
    },
    methods: {
        get_results: function() {
            let query = this.$route.params.query;

            // Local this
            let vue_this = this;

            // Set loading to true so we get a loading-screen
            this.loading = true;

            // Reset the results
            this.results = null;

            // Do the API request to search
            me_api_call({
                group: 'search',
                endpoint: 'search',
                method: 'GET',
                data: { query: query }
            })
                .then(function(data) {
                    vue_this.results = data.data.dataset.data;
                    vue_this.loading = false;
                })
                .catch(function(data) {
                    vue_this.loading = false;
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
        go_to_api_clients: function() {
            this.$router.push('/api_clients');
        },
        go_to_user_profile: function() {
            this.$router.push('/userprofile');
        }
    }
};
</script>
