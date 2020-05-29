<template>
    <div id='me-content-api-clients'>
        <me-page-title icon='desktop'>
            API clients
            <template v-slot:actions>
                <me-button primary v-bind:disabled='loading'>Add client</me-button>
            </template>
        </me-page-title>
        <me-grid>
            <me-cell padding v-bind:span='12'>
                <me-card class='clients' raised wide>
                    <me-h1 inverted>Authorized clients</me-h1>
                    <me-api-client v-bind:client='client' v-bind:key='client.id' v-for='client in $store.state.api_data.api_clients.clients' v-if='!loading'></me-api-client>
                    <div class='loading_text' v-if='loading'>
                        <div class='ui active inline loader'></div>Loading the API clients
                    </div>
                </me-card>
            </me-cell>
        </me-grid>
    </div>
</template>

<script>
import me_page_title from '../components/me-page-title';
import me_button from '../components/me-button';
import me_grid from '../components/me-grid';
import me_cell from '../components/me-cell';
import me_h1 from '../components/me-h1';
import me_card from '../components/me-card';
import me_api_client from '../components/me-api-client';

export default {
    name: 'me-content-api-clients',
    components: {
        'me-page-title': me_page_title,
        'me-button': me_button,
        'me-grid': me_grid,
        'me-cell': me_cell,
        'me-h1': me_h1,
        'me-card': me_card,
        'me-api-client': me_api_client
    },
    created: function() {
        // We don't need a sidebar on this page. Disable it.
        this.$store.commit('set_sidebar_availability', false);

        // Update the client tokens in the store
        this.set_clients();
    },
    data: function() {
        return {
            loading: true
        };
    },
    methods: {
        set_clients: function(force = false) {
            // Method to set the API clients

            // Local this
            var vue_this = this;

            // Set the fields for the profile
            this.$store.commit('api_update_api_clients', {
                get_user_tokens: false,
                success: function(data) {
                    vue_this.loading = false;
                },
                failed: function() {
                    vue_this.loading = false;
                    $('body').toast({
                        position: 'bottom center',
                        message:
                            'Something went wrong while retrieving the API clients',
                        closeIcon: true,
                        displayTime: 'auto',
                        showIcon: 'user',
                        class: 'error'
                    });
                },
                force: force
            });
        }
    }
};
</script>
