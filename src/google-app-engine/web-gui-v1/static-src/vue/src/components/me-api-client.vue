<template>
    <div class='client'>
        <me-flexline class='client_title'>
            <div>
                <p class='title'>
                    {{ client.app_name }}
                    <span class='publisher'>({{ client.app_publisher }})</span>
                </p>
                <p class='version'>Version: {{ client.app_version }}</p>
                <p v-if='client.expiration'>
                    Will expire on: {{ expire }}
                    <span class='expired' v-if='expired'>(expired)</span>
                </p>
                <p v-if='!client.expiration'>This token will not expire</p>
            </div>
            <div class='spacer'></div>
            <div class='actions' v-show='!permissions_available'>
                <span data-position='top right' data-tooltip='Disable user token' v-if='client.enabled'>
                    <me-button class='red' icon='power off' v-bind:disabled='loading_disable' v-bind:loading='loading_disable' v-on:click='disable_token'></me-button>
                </span>
                <span data-position='top right' data-tooltip='Enable user token' v-if='!client.enabled'>
                    <me-button class='green' icon='play' v-bind:disabled='loading_disable' v-bind:loading='loading_disable' v-on:click='enable_token'></me-button>
                </span>
                <span data-position='top right' data-tooltip='Token permissions'>
                    <me-button icon='list' v-on:click='show_permissions'></me-button>
                </span>
                <span data-position='top right' data-tooltip='Reveal token'>
                    <me-button icon='key' v-bind:class='{ "green": show_token }' v-on:click='show_token = !show_token'></me-button>
                </span>
                <span data-position='top center' data-tooltip='Edit token'>
                    <me-button icon='edit' v-on:click='edit_token'></me-button>
                </span>
                <span data-position='top right' data-tooltip='Set to not expire'>
                    <me-button icon='infinity' v-bind:disabled='loading_infinity || !client.expiration' v-bind:loading='loading_infinity' v-on:click='set_token_infinite'></me-button>
                </span>
                <span data-position='top right' data-tooltip='Remove token'>
                    <me-button class='red' icon='trash' v-bind:disabled='loading_delete' v-bind:loading='loading_delete' v-on:click='delete_token'></me-button>
                </span>
            </div>
            <div class='actions' v-show='permissions_available'>
                <span data-position='top right' data-tooltip='Close permission view'>
                    <me-button icon='close' v-on:click='hide_permissions'></me-button>
                </span>
            </div>
        </me-flexline>
        <me-flexline class='token_line' v-if='show_token'>
            <div class='grower' ref='token'>{{ client.token }}</div>
            <div class='ui icon button' data-position='top right' data-tooltip='Copy token' v-if='!copied' v-on:click='copy_token'>
                <i class='copy icon'></i>
            </div>
            <div class='ui button' data-position='top right' data-tooltip='Copy token' v-if='copied' v-on:click='copy_token'>Copied to clipboard!</div>
        </me-flexline>
        <me-token-permissions type='client' v-bind:token='client.token' v-if='permissions_available'></me-token-permissions>
    </div>
</template>

<script>
import me_flexline from './me-flexline';
import me_button from './me-button';
import me_token_permissions from './me-token-permissions';
import eventbus from '../eventbus';
import strftime from 'strftime';

export default {
    name: 'me-api-client',
    components: {
        'me-flexline': me_flexline,
        'me-button': me_button,
        'me-token-permissions': me_token_permissions
    },
    computed: {
        expire: function() {
            console.log(this.client);
            let format = this.$store.state.app.user_config.config
                .datetime_formats.datetime_format;
            if (format) {
                return strftime(format, this.client.expiration);
            }
            return undefined;
        },
        expired: function() {
            let today = new Date();
            return this.client.expiration < today;
        }
    },
    data: function() {
        return {
            loading: false,
            loading_disable: false,
            loading_delete: false,
            loading_infinity: false,
            show_token: false,
            copied: false,
            permissions_available: false
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
        },
        copy_token: function() {
            // Copy the token code to the clipboard

            // Local this
            let vue_this = this;

            // Copy the token the the clipboard
            navigator.clipboard.writeText(this.client.token).then(function() {
                vue_this.copied = true;

                setTimeout(function() {
                    vue_this.copied = false;
                }, 2000);
            });
        },
        show_permissions: function() {
            this.permissions_available = true;
            this.show_token = false;
        },
        hide_permissions: function() {
            this.permissions_available = false;
        },
        delete_token: function() {
            // Local this
            let vue_this = this;

            this.loading_delete = true;

            // Ask the user if he is sure to remove this token
            $('body').toast({
                message: 'Do you really want to remove this client?',
                displayTime: 0,
                class: 'white',
                position: 'top center',
                actions: [
                    {
                        text: 'Yes',
                        icon: 'check',
                        class: 'green',
                        click: function() {
                            vue_this.$store.commit(
                                'api_update_api_delete_client_token',
                                {
                                    success: function() {
                                        vue_this.loading_delete = false;
                                        $('body').toast({
                                            position: 'bottom center',
                                            message: 'Deleted token',
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
                                                'Something went wrong while deleting the token',
                                            closeIcon: true,
                                            displayTime: 'auto',
                                            showIcon: 'user',
                                            class: 'error'
                                        });
                                    },
                                    fields: {
                                        id: vue_this.client.id
                                    }
                                }
                            );
                        }
                    },
                    {
                        icon: 'ban',
                        text: 'No',
                        class: 'red',
                        click: function() {
                            vue_this.loading_delete = false;
                        }
                    }
                ]
            });
        },
        edit_token: function() {
            // Show the 'new API client' modal. We use a object as identifier so the modal knows it
            // has to go to 'edit' mode
            eventbus.$emit('show_modal', {
                id: 'modal_new_api_client',
                client: this.client
            });
        },
        set_token_infinite: function() {
            // Method that sets the token to infinite
            this.loading_infinity = true;

            // Local this
            let vue_this = this;

            // We have the time, let's update the user token
            this.$store.commit('api_update_api_client_token', {
                success: function() {
                    vue_this.loading_infinity = false;
                    vue_this.renaming = false;
                    $('body').toast({
                        position: 'bottom center',
                        message: 'Set token to not expire',
                        closeIcon: true,
                        displayTime: 'auto',
                        showIcon: 'user',
                        class: 'success'
                    });
                },
                failed: function() {
                    vue_this.loading_infinity = false;
                    $('body').toast({
                        position: 'bottom center',
                        message:
                            'Something went wrong while setting the token to not expire',
                        closeIcon: true,
                        displayTime: 'auto',
                        showIcon: 'user',
                        class: 'error'
                    });
                },
                fields: {
                    expire: null,
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
