<template>
    <div class='client'>
        <me-flexline class='client_title'>
            <div>
                <p class='title'>
                    {{ client.app_name }}
                    <span class='publisher'>({{ client.app_publisher }})</span>
                </p>
                <p class='version'>Version: {{ client.app_version }}</p>
            </div>
            <div class='spacer'></div>
            <div class='actions'>
                <span data-position='top right' data-tooltip='Disable user token' v-if='client.enabled'>
                    <me-button class='red' icon='power off' v-bind:disabled='loading_disable' v-bind:loading='loading_disable' v-on:click='disable_token'></me-button>
                </span>
                <span data-position='top right' data-tooltip='Enable user token' v-if='!client.enabled'>
                    <me-button class='green' icon='play' v-bind:disabled='loading_disable' v-bind:loading='loading_disable' v-on:click='enable_token'></me-button>
                </span>
            </div>
        </me-flexline>
    </div>
</template>

<script>
import me_flexline from './me-flexline';
import me_button from './me-button';

export default {
    name: 'me-api-client',
    components: {
        'me-flexline': me_flexline,
        'me-button': me_button
    },
    data: function() {
        return {
            loading: false,
            loading_disable: false
        };
    },
    methods: {
        enable_token: function() {
            // Method that enables the token
            this.loading_disable = true;

            // Local this
            let vue_this = this;

            // We have the time, let's update the user token
            this.$store.commit('api_update_api_client_token', {
                success: function() {
                    vue_this.loading_disable = false;
                    $('body').toast({
                        position: 'bottom center',
                        message: 'Enabled token',
                        closeIcon: true,
                        displayTime: 'auto',
                        showIcon: 'user',
                        class: 'success'
                    });
                },
                failed: function() {
                    vue_this.loading_disable = false;
                    $('body').toast({
                        position: 'bottom center',
                        message:
                            'Something went wrong while enabeling the token',
                        closeIcon: true,
                        displayTime: 'auto',
                        showIcon: 'user',
                        class: 'error'
                    });
                },
                fields: {
                    enabled: true,
                    id: this.client.id
                }
            });
        },
        disable_token: function() {
            // Method that disables the token
            this.loading_disable = true;

            // Local this
            let vue_this = this;

            // We have the time, let's update the user token
            this.$store.commit('api_update_api_client_token', {
                success: function() {
                    vue_this.loading_disable = false;
                    $('body').toast({
                        position: 'bottom center',
                        message: 'Enabled token',
                        closeIcon: true,
                        displayTime: 'auto',
                        showIcon: 'user',
                        class: 'success'
                    });
                },
                failed: function() {
                    vue_this.loading_disable = false;
                    $('body').toast({
                        position: 'bottom center',
                        message:
                            'Something went wrong while disabling the token',
                        closeIcon: true,
                        displayTime: 'auto',
                        showIcon: 'user',
                        class: 'error'
                    });
                },
                fields: {
                    enabled: false,
                    id: this.client.id
                }
            });
        }
    },
    props: {
        client: { mandatory: true }
    }
};
</script>