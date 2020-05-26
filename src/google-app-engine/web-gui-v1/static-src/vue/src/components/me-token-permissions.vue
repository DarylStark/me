<template>
    <div class='me-token-permissions'>
        <me-token-permission v-bind:key='permission.id' v-bind:permission='permission' v-for='permission in permissions'></me-token-permission>
    </div>
</template>

<script>
import me_api_call from '../me/api_call';
import me_token_permission from './me-token-permission';

export default {
    name: 'me-token-permissions',
    components: {
        'me-token-permission': me_token_permission
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
    data: function() {
        return {
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