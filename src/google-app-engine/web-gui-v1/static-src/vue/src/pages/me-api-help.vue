<template>
    <div id='me-content-api-help'>
        <me-page-title icon='question circle outline'>API help</me-page-title>
        <me-grid>
            <me-cell padding v-bind:span='12'>
                <me-card padding raised wide>
                    <p>
                        The REST API for the Me system uses API groups. Each group contains one or
                        more endpoints that can be used to create, retrieve, update or delete
                        resources in the system. Each endpoint uses permissions for specific HTTP
                        methods to determine what a user or client can or can't do. This page
                        describes the API groups and endpoint that exists and what permissions the
                        user or client needs to be able to use them.
                    </p>
                    <p>The REST API URL is as follows:</p>
                    <code>https://me.dstark.nl/api/v1/&lt;group&gt;/&lt;endpoint&gt;</code>
                    <p>
                        To authenticate, you can specify a Client Token for API endpoints that
                        require a client token, or a User Token for API endpoints that require a
                        user token. To specify a token, you need to set one of the following HTTP
                        headers:
                    </p>
                    <ul>
                        <li>X-Me-Auth-User; to specify a User Token</li>
                        <li>X-Me-Auth-Client; to specify a Client Token</li>
                    </ul>
                </me-card>
            </me-cell>
        </me-grid>
        <me-page-title icon='question circle outline'>Groups and endpoints</me-page-title>

        <me-grid>
            <me-cell padding v-bind:span='12'>
                <me-card id='groups' raised wide>
                    <div class='loading_text' v-if='loading'>
                        <div class='ui active inline loader'></div>Loading the API endpoints
                    </div>
                    <div v-if='!loading'>
                        <me-api-help-group v-bind:group='group' v-bind:key='group.name' v-for='group in endpoints'></me-api-help-group>
                    </div>
                </me-card>
            </me-cell>
        </me-grid>
    </div>
</template>

<script>
import me_page_title from '../components/me-page-title';
import me_card from '../components/me-card';
import me_grid from '../components/me-grid';
import me_cell from '../components/me-cell';
import me_api_call from '../me/api_call';
import me_flexline from '../components/me-flexline';
import me_api_help_group from '../components/me-api-help-group';

export default {
    name: 'me-content-api-help',
    components: {
        'me-page-title': me_page_title,
        'me-card': me_card,
        'me-grid': me_grid,
        'me-cell': me_cell,
        'me-flexline': me_flexline,
        'me-api-help-group': me_api_help_group
    },
    data: function() {
        return {
            loading: true,
            endpoints: null
        };
    },
    created: function() {
        // We don't need a sidebar on this page. Disable it.
        this.$store.commit('set_sidebar_availability', false);

        // Local this
        let vue_this = this;

        // Retrieve the API groups from the API
        me_api_call({
            group: 'help',
            endpoint: 'endpoints',
            method: 'GET'
        })
            .then(function(data) {
                // We have the data
                let endpoints = data.data.dataset.data;

                // Sort the groups
                endpoints.sort((a, b) => {
                    if (a.name > b.name) {
                        return 1;
                    }
                    return -1;
                });

                // Sort the endpoints in the groups
                endpoints.forEach(function(group) {
                    group.endpoints.sort((a, b) => {
                        if (a.name > b.name) {
                            return 1;
                        }
                        return -1;
                    });
                });

                // Set the data
                vue_this.endpoints = endpoints;
                vue_this.loading = false;
            })
            .catch(function(data) {
                vue_this.loading = false;
                $('body').toast({
                    position: 'bottom center',
                    message: "Couldn't retrieve endpoints",
                    closeIcon: true,
                    displayTime: 'auto',
                    showIcon: 'user',
                    class: 'error'
                });
            });
    }
};
</script>
