<template>
    <div class='user_token'>
        <me-flexline class='ui segment'>
            <div class='grower client_title'>
                <p class='title' v-if='user_token.description'>{{ user_token.description }}</p>
                <p class='title' v-if='!user_token.description'>No title given</p>
                <p v-if='user_token.expiration'>
                    Will expire on: {{ expire }}
                    <span class='expired' v-if='expired'>(expired)</span>
                </p>
                <p v-if='!user_token.expiration'>This token will not expire</p>
            </div>
            <div class='actions' v-show='!renaming && !permissions_available'>
                <span data-position='top left' data-tooltip='Disable user token' v-if='user_token.enabled'>
                    <me-button class='red' icon='power off' v-bind:disabled='loading_disable' v-bind:loading='loading_disable' v-on:click='disable_token'></me-button>
                </span>
                <span data-position='top left' data-tooltip='Enable user token' v-if='!user_token.enabled'>
                    <me-button class='green' icon='play' v-bind:disabled='loading_disable' v-bind:loading='loading_disable' v-on:click='enable_token'></me-button>
                </span>
                <span data-position='top left' data-tooltip='Token permissions'>
                    <me-button icon='list' v-on:click='show_permissions'></me-button>
                </span>
                <span data-position='top left' data-tooltip='Reveal token'>
                    <me-button icon='key' v-bind:class='{ "green": show_token }' v-on:click='show_token = !show_token'></me-button>
                </span>
                <span data-position='top center' data-tooltip='Rename token'>
                    <me-button icon='edit' v-on:click='rename_token'></me-button>
                </span>
                <div class='inline'>
                    <div class='ui calendar' ref='expire_date_button'>
                        <span data-position='top right' data-tooltip='Set expire date and time'>
                            <me-button class='calendar' icon='clock outline' v-bind:disabled='loading_date' v-bind:loading='loading_date'></me-button>
                        </span>
                    </div>
                </div>
                <span data-position='top right' data-tooltip='Set to not expire'>
                    <me-button icon='infinity' v-bind:disabled='loading_infinity || !user_token.expiration' v-bind:loading='loading_infinity' v-on:click='set_token_infinite'></me-button>
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
            <div class='grower' ref='token'>{{ user_token.token }}</div>
            <div class='ui icon button' data-position='top right' data-tooltip='Copy token' v-if='!copied' v-on:click='copy_token'>
                <i class='copy icon'></i>
            </div>
            <div class='ui button' data-position='top right' data-tooltip='Copy token' v-if='copied' v-on:click='copy_token'>Copied to clipboard!</div>
        </me-flexline>
        <me-flexline class='rename' v-if='renaming'>
            <div class='grower'>
                <me-input fluid id='new_name' placeholder='Enter a name for this token' ref='new_name' transparent v-bind:disabled='loading' v-model='description' v-on:enter='rename_token_send' v-on:escape='cancel_rename'></me-input>
            </div>
            <div>
                <span data-position='top right' data-tooltip='Save'>
                    <me-button class='red' icon='times' v-bind:disabled='loading' v-on:click='cancel_rename'></me-button>
                    <me-button class='green' icon='check' v-bind:disabled='loading' v-bind:loading='loading' v-on:click='rename_token_send'></me-button>
                </span>
            </div>
        </me-flexline>
        <me-token-permissions type='user' v-bind:token='user_token.token' v-if='permissions_available'></me-token-permissions>
    </div>
</template>

<script>
import me_flexline from './me-flexline';
import me_button from './me-button';
import me_input from './me-input';
import me_token_permissions from './me-token-permissions';
import Vue from 'vue';
import strftime from 'strftime';

export default {
    name: 'me-userprofile-api-user',
    computed: {
        expire: function() {
            let format = this.$store.state.app.user_config.config
                .datetime_formats.datetime_format;
            if (format) {
                return strftime(format, this.user_token.expiration);
            }
            return undefined;
        },
        expired: function() {
            let today = new Date();
            return this.user_token.expiration < today;
        }
    },
    data: function() {
        return {
            show_token: false,
            copied: false,
            loading: false,
            loading_date: false,
            loading_disable: false,
            renaming: false,
            description: null,
            loading_delete: false,
            loading_infinity: false,
            permissions_available: false
        };
    },
    methods: {
        show_permissions: function() {
            this.permissions_available = true;
        },
        hide_permissions: function() {
            this.permissions_available = false;
        },
        copy_token: function() {
            // Copy the token code to the clipboard

            // Local this
            let vue_this = this;

            // Copy the token the the clipboard
            navigator.clipboard
                .writeText(this.user_token.token)
                .then(function() {
                    vue_this.copied = true;

                    setTimeout(function() {
                        vue_this.copied = false;
                    }, 2000);
                });
        },
        rename_token: function() {
            // Start the renaming
            this.renaming = true;
            this.show_token = false;

            // Local this
            let vue_this = this;

            // Focus the rename input
            Vue.nextTick().then(function() {
                vue_this.$refs.new_name.focus();
                vue_this.$refs.new_name.select();
            });
        },
        cancel_rename: function() {
            // Cancel the renaming
            this.renaming = false;
            this.description = this.user_token.description;
        },
        rename_token_send: function() {
            if (!this.loading) {
                // Method that actually updates the tokenname
                this.loading = true;

                // Local this
                let vue_this = this;

                // We have the time, let's update the user token
                this.$store.commit('api_update_api_user_token', {
                    success: function() {
                        vue_this.loading = false;
                        vue_this.renaming = false;
                        $('body').toast({
                            position: 'bottom center',
                            message: 'Updated description',
                            closeIcon: true,
                            displayTime: 'auto',
                            showIcon: 'user',
                            class: 'success'
                        });
                    },
                    failed: function() {
                        vue_this.loading = false;
                        $('body').toast({
                            position: 'bottom center',
                            message:
                                'Something went wrong while updating the description',
                            closeIcon: true,
                            displayTime: 'auto',
                            showIcon: 'user',
                            class: 'error'
                        });
                    },
                    fields: {
                        description: this.description,
                        id: this.user_token.id
                    }
                });
            }
        },
        disable_token: function() {
            // Method that disables the token
            this.loading_disable = true;

            // Local this
            let vue_this = this;

            // We have the time, let's update the user token
            this.$store.commit('api_update_api_user_token', {
                success: function() {
                    vue_this.loading_disable = false;
                    $('body').toast({
                        position: 'bottom center',
                        message: 'Disabled token',
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
                    id: this.user_token.id
                }
            });
        },
        enable_token: function() {
            // Method that enables the token
            this.loading_disable = true;

            // Local this
            let vue_this = this;

            // We have the time, let's update the user token
            this.$store.commit('api_update_api_user_token', {
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
                    id: this.user_token.id
                }
            });
        },
        set_token_infinite: function() {
            // Method that sets the token to infinite
            this.loading_infinity = true;

            // Local this
            let vue_this = this;

            // We have the time, let's update the user token
            this.$store.commit('api_update_api_user_token', {
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
                    id: this.user_token.id
                }
            });
        },
        delete_token: function() {
            // Local this
            let vue_this = this;

            this.loading_delete = true;

            // Ask the user if he is sure to remove this token
            $('body').toast({
                message: 'Do you really want to remove this user token?',
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
                                'api_update_api_delete_user_token',
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
                                        id: vue_this.user_token.id
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
        expire_date_set: function(date, mode) {
            if (mode == 'minute') {
                this.loading_date = true;

                // Local this
                let vue_this = this;

                // We have the time, let's update the user token
                this.$store.commit('api_update_api_user_token', {
                    success: function() {
                        vue_this.loading_date = false;
                        $('body').toast({
                            position: 'bottom center',
                            message: 'Updated expiration date and time',
                            closeIcon: true,
                            displayTime: 'auto',
                            showIcon: 'user',
                            class: 'success'
                        });
                    },
                    failed: function() {
                        vue_this.loading_date = false;
                        $('body').toast({
                            position: 'bottom center',
                            message:
                                'Something went wrong while updating the expiration date and time',
                            closeIcon: true,
                            displayTime: 'auto',
                            showIcon: 'user',
                            class: 'error'
                        });
                    },
                    fields: {
                        expire: date,
                        id: this.user_token.id
                    }
                });
            }
        },
        init_calendar: function() {
            // Create the calendar object
            $(this.$refs.expire_date_button).calendar({
                firstDayOfWeek: 1,
                onSelect: this.expire_date_set,
                selectAdjacentDays: true,
                minTimeGap: 15,
                ampm: !this.$store.state.app.user_config.config.datetime_formats
                    .show_24h,
                initialDate: this.user_token.expiration
            });
        }
    },
    components: {
        'me-flexline': me_flexline,
        'me-button': me_button,
        'me-input': me_input,
        'me-token-permissions': me_token_permissions
    },
    props: {
        user_token: { mandatory: true }
    },
    created: function() {
        this.description = this.user_token.description;
    },
    mounted: function() {
        // Local this
        let vue_this = this;

        // Initiate the calendar
        this.init_calendar();
    }
};
</script>
