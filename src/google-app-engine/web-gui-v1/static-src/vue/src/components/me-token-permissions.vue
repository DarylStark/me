<template>
    <div class='me-token-permissions'>
        <me-flexline class='header'>
            <div class='grower'>Permissions</div>
            <div>
                <me-input icon='search' icon_position='right' id='search' placeholder='search' v-model='query'></me-input>
            </div>
        </me-flexline>
        <div class='permissions'>
            <me-token-permission v-bind:key='permission.id' v-bind:permission='permission' v-for='permission in selected_permissions'></me-token-permission>
        </div>
    </div>
</template>

<script>
import me_api_call from '../me/api_call';
import me_token_permission from './me-token-permission';
import me_flexline from './me-flexline';
import me_input from './me-input';

export default {
    name: 'me-token-permissions',
    components: {
        'me-token-permission': me_token_permission,
        'me-flexline': me_flexline,
        'me-input': me_input
    },
    props: {
        type: {
            required: true,
            validator: function(value) {
                return ['client', 'user'].indexOf(value) !== -1;
            }
        },
        token_id: {
            type: Number,
            required: true
        }
    },
    computed: {
        selected_permissions: function() {
            // If the query is empty, we return the list 'as-is'
            if (this.query == null || this.query == '') {
                return this.permissions;
            }

            // Get the query
            let query = this.query.toLowerCase();

            // Return the filtered list
            return this.permissions.filter(function(item) {
                // Get the complete permission name
                let full_permission =
                    item.section.toLowerCase() +
                    '.' +
                    item.subject.toLowerCase();

                // Return if this item should be showed
                return (
                    item.description.toLowerCase().includes(query) ||
                    item.section.toLowerCase().includes(query) ||
                    item.subject.toLowerCase().includes(query) ||
                    full_permission.includes(query)
                );
            });
        }
    },
    data: function() {
        return {
            query: null,
            permissions: [
                {
                    id: 1,
                    section: 'aaa',
                    subject: 'retrieve_user_token_with_credentials',
                    description:
                        'Retrieving a user token using the users credentials',
                    granted: true
                },
                {
                    id: 2,
                    section: 'aaa',
                    subject: 'refresh_user_token',
                    description: 'Refreshing a user token before it expires',
                    granted: true
                },
                {
                    id: 3,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 4,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 5,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 6,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 7,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 8,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 9,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 10,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 11,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 12,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                },
                {
                    id: 13,
                    section: 'api_clients',
                    subject: 'retrieve_clients',
                    description: 'Retrieve API clients',
                    granted: true
                }
            ]
        };
    },
    mounted: function() {
        // Get the permissions from the API
        // TODO: Implement
    }
};
</script>