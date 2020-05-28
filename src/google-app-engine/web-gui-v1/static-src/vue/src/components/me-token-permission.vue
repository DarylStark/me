<template>
    <me-flexline class='permission'>
        <div class='grower description'>
            {{ permission.description }}
            <p>{{ permission.section }}.{{ permission.subject }}</p>
        </div>
        <div>
            <div class='ui active inline loader' v-if='loading'></div>
            <!-- TOOD: Create a seperate component for this and use it in the userprofile as well! -->
            <div class='ui slider checkbox' v-if='!loading'>
                <input type='checkbox' v-model='value' v-on:change='change' />
                <label></label>
            </div>
            <!-- /TODO -->
        </div>
    </me-flexline>
</template>

<script>
import me_flexline from './me-flexline';
import me_api_call from '../me/api_call';

export default {
    name: 'me-token-permission',
    components: {
        'me-flexline': me_flexline
    },
    data: function() {
        return {
            value: null,
            loading: false
        };
    },
    props: {
        permission: {
            required: true
        },
        type: {
            required: true,
            validator: function(value) {
                return ['client', 'user'].indexOf(value) !== -1;
            }
        },
        token: {
            required: true,
            type: String
        }
    },
    created: function() {
        this.value = this.permission.granted;
    },
    methods: {
        change: function() {
            // Local this
            let vue_this = this;

            this.loading = true;

            // Get the correct endpoint
            let group = null;
            let endpoint = null;
            let data = null;

            if (this.type == 'user') {
                group = 'aaa';
                endpoint = 'user_permissions';
                data = {
                    user_token: this.token,
                    permission:
                        this.permission.section + '.' + this.permission.subject,
                    granted: this.value
                };
            }

            // Send the API to update the permission
            me_api_call({
                group: group,
                endpoint: endpoint,
                method: 'PATCH',
                data: data
            })
                .then(function(data) {
                    vue_this.permission.granted = vue_this.value;
                    vue_this.loading = false;
                })
                .catch(function(error) {
                    vue_this.loading = false;
                    vue_this.value = !vue_this.value;
                    $('body').toast({
                        position: 'bottom center',
                        message: "Coundn't update permission",
                        closeIcon: true,
                        displayTime: 'auto',
                        showIcon: 'user',
                        class: 'error'
                    });
                });
        }
    }
};
</script>