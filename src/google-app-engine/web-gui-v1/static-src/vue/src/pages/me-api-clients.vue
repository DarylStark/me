<template>
    <div id='me-content-api-clients'>
        <me-modal-new-api-client></me-modal-new-api-client>
        <me-page-title icon='desktop'>
            API clients
            <template v-slot:actions>
                <me-button v-bind:disabled='loading' v-on:click='reload'>Reload</me-button>
                <me-button primary v-bind:disabled='loading' v-on:click='show_add_client'>Add client</me-button>
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
import me_modal_new_api_client from '../modals/me-modal-new-api-client';
import eventbus from '../eventbus';

export default {
    name: 'me-content-api-clients',
    components: {
        'me-page-title': me_page_title,
        'me-button': me_button,
        'me-grid': me_grid,
        'me-cell': me_cell,
        'me-h1': me_h1,
        'me-card': me_card,
        'me-api-client': me_api_client,
        'me-modal-new-api-client': me_modal_new_api_client
    },
    created: function() {
        // Local this
        var vue_this = this;

        // Add the local actions for this page. These actions will be visible in the command palette
        this.$store.commit('add_local_actions', [
            {
                id: 'reload-client-tokens',
                icon: 'redo',
                title: 'Reload client tokens',
                type: 'action',
                action: function(vue_instance) {
                    vue_this.set_clients_forced();
                },
                show: true
            },
            {
                id: 'add-client-token',
                icon: 'redo',
                title: 'Add client token',
                type: 'action',
                action: function(vue_instance) {
                    vue_this.show_add_client();
                },
                show: true
            }
        ]);

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
        },
        show_add_client: function() {
            // Show the 'new API client' modal
            eventbus.$emit('show_modal', 'modal_new_api_client');
        },
        set_clients_forced: function() {
            this.loading = true;
            this.set_clients(true);
        },
        reload: function() {
            this.set_clients_forced();
        }
    },
    beforeRouteLeave: function(to, from, next) {
        this.$store.commit('remove_local_actions');
        next(true);
    }
};
</script>
