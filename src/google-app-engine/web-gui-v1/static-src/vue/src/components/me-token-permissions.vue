<template>
    <div class='me-token-permissions'>
        <me-flexline class='header'>
            <div class='grower'>Permissions</div>
            <div>
                <me-input icon='search' icon_position='right' id='search' placeholder='search' v-model='query'></me-input>
            </div>
        </me-flexline>
        <div class='permissions' v-if='loaded'>
            <me-token-permission v-bind:key='permission.id' v-bind:permission='permission' v-for='permission in selected_permissions'></me-token-permission>
        </div>
        <div class='loading_text' v-if='!loaded'>
            <div class='ui active inline loader'></div>Loading the API clients
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
        token: {
            type: String,
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
            permissions: null,
            loaded: false
        };
    },
    created: function() {
        // Local this
        let vue_this = this;

        // Get the permissions from the API
        me_api_call({
            group: 'aaa',
            endpoint: 'user_permissions',
            method: 'GET',
            data: {
                user_token: this.token
            }
        })
            .then(function(data) {
                console.log(data);
                vue_this.permissions = data.data.dataset.data;
                vue_this.loaded = true;
            })
            .catch(function(error) {
                $('body').toast({
                    position: 'bottom center',
                    message: "Coundn't retrieve token permissions",
                    closeIcon: true,
                    displayTime: 'auto',
                    showIcon: 'user',
                    class: 'error'
                });
            });
    }
};
</script>