<script>
/* A global store for Vue. Will be used to store state information about the application */
import Vue from 'vue';
import Vuex from 'vuex';
import me_api_call from './me/api_call';
import me_client_call from './me/client_call';
import eventbus from './eventbus';

// Make sure Vue knows to use Vuex
Vue.use(Vuex);

// Export the store
export default new Vuex.Store({
    state: {
        app: {
            environment: null,
            user_token: null,
            loading_text: 'Loading dashboard',
            user_config: {
                _updated: false,
                config: {}
            }
        },
        ui: {
            media_type: null,
            search_active: false,
            menu_open: true,
            sidebar_available: true,
            sidebar_open: true,
            menus: {
                main: [
                    {
                        group: 'Menu',
                        display_group_title: false,
                        items: [
                            {
                                title: 'Dashboard',
                                icon: 'columns',
                                dst: '/home'
                            },
                            { title: 'Feed', icon: 'list', dst: '/feed' },
                            {
                                title: 'Notes',
                                icon: 'clipboard outline',
                                dst: '/notes'
                            }
                        ]
                    },
                    {
                        group: 'Music',
                        display_group_title: true,
                        items: [
                            { title: 'Events', icon: 'music', dst: '/events' },
                            {
                                title: 'Making music',
                                icon: 'guitar',
                                dst: '/making_music'
                            }
                        ]
                    }
                ],
                user: [
                    {
                        title: 'User profile and settings',
                        icon: 'user circle',
                        dst: '/userprofile',
                        type: 'link'
                    },
                    {
                        title: 'Rename session',
                        icon: 'pen',
                        action: function() {
                            eventbus.$emit(
                                'show_modal',
                                'modal_set_session_title'
                            );
                        },
                        type: 'action'
                    },
                    {
                        title: 'Logout',
                        icon: 'sign out alternate',
                        action: function() {
                            me_api_call({
                                group: 'aaa',
                                endpoint: 'remove_user_token',
                                method: 'DELETE'
                            })
                                .then(function(data) {
                                    // Logged out! Remove the cookie
                                    $cookies.remove('user_token');

                                    // Redirect the user to the loginpage
                                    location.href = '/ui/login';
                                })
                                .catch(function(data) {
                                    $('body').toast({
                                        position: 'bottom center',
                                        message: "Couldn't remove your session",
                                        closeIcon: true,
                                        displayTime: 'auto',
                                        showIcon: 'user',
                                        class: 'error'
                                    });
                                });
                        },
                        type: 'action'
                    }
                ]
            },
            actions: [
                {
                    icon: 'bars',
                    title: 'Toggle menu',
                    type: 'action',
                    action: function(vue_instance) {
                        vue_instance.$store.commit('set_menu_state', 'toggle');
                    },
                    show: true
                },
                {
                    id: 'toggle_sidebar',
                    icon: 'bars',
                    title: 'Toggle sidebar',
                    type: 'action',
                    action: function(vue_instance) {
                        vue_instance.$store.commit(
                            'set_sidebar_state',
                            'toggle'
                        );
                    },
                    show: true
                },
                {
                    icon: 'redo',
                    title: 'Reload page',
                    type: 'action',
                    action: function(vue_instance) {
                        location.reload();
                    },
                    show: true
                },
                {
                    icon: 'desktop',
                    title: 'API clients',
                    type: 'link',
                    dst: '/api_clients',
                    show: true
                },
                {
                    icon: 'key',
                    title: 'Change password',
                    type: 'action',
                    action: function(vue_instance) {
                        eventbus.$emit('show_modal', 'modal_change_password');
                    },
                    show: true
                }
            ],
            local_actions: new Array()
        },
        api_data: {
            user_token_object: {
                expiration: null,
                created: null,
                description: null,
                token: null
            },
            user_object: {
                _updated: false,
                username: null,
                fullname: null,
                email: null,
                password_date: null,
                second_factor_enabled: false
            },
            api_clients: {
                _updated: false,
                _updated_user_tokens: false,
                clients: []
            }
        }
    },
    mutations: {
        set_media_type: function(state, media_type) {
            // Method to set the media type. Can be 'phone', 'table' or 'desktop'. When set to
            // phone or table, we have to hide the menu. When set to desktop, we show the menu.

            // First, set the state
            state.ui.media_type = media_type;

            // Then decide if we should hide or show the menu.
            if (
                state.ui.media_type == 'phone' ||
                state.ui.media_type == 'tablet'
            ) {
                state.ui.menu_open = false;
                state.ui.sidebar_open = false;
            } else {
                state.ui.menu_open = true;
                state.ui.sidebar_open = true;
            }
        },
        set_menu_state: function(state, new_state) {
            // Method to set the state of the menu; open or closed. When the 'new_state' is set to
            // true, the menu should be open. When the 'new_state' is set to false, the menu should
            // be closed. If the state is set to 'toggle', we 'toggle' the menu
            if (new_state == true || new_state == false) {
                state.ui.menu_open = new_state;
            } else if (new_state == 'toggle') {
                state.ui.menu_open = !state.ui.menu_open;
            }

            // When we are on mobile, the state of the menu is set to open AND the sidebar is
            // already open, we have to close the sidebar. Otherwise, they are in eachothers way
            if (
                state.ui.media_type == 'phone' &&
                state.ui.sidebar_open &&
                new_state
            ) {
                state.ui.sidebar_open = false;
            }
        },
        set_sidebar_state: function(state, new_state) {
            // Method to set the state of the sidebar; open or closed. When the 'new_state' is set
            // to true, the sidebar should be open. Whe the 'new_state' is set to false, the menu
            // should be closed. If the state is set to 'toggle', we 'toggle' the menu
            if (new_state == true || new_state == false) {
                state.ui.sidebar_open = new_state;
            } else if (new_state == 'toggle') {
                state.ui.sidebar_open = !state.ui.sidebar_open;
            }

            // When we are on mobile, the state of the sidebar is set to open AND the menu is
            // already open, we have to close the menu. Otherwise, they are in eachothers way
            if (
                state.ui.media_type == 'phone' &&
                state.ui.menu_open &&
                new_state
            ) {
                state.ui.menu_open = false;
            }
        },
        set_sidebar_availability: function(state, new_availability) {
            // Enable or disable the sidebar. For some pages, the sidebar is not needed and has to
            // be disabled to not confuse the user
            state.ui.sidebar_available = new_availability;

            // Hide or show the global action as well
            state.ui.actions.forEach(function(action) {
                if (action.id == 'toggle_sidebar') {
                    action.show = new_availability;
                }
            });
        },
        set_search_state: function(state, new_state) {
            // Method to set the state of the searchbar; open or closed. When the 'new_state' is set
            // to true, the searchbar should be open. Whe the 'new_state' is set to false, the bar
            // should be closed. If the state is set to 'toggle', we 'toggle' the searchbar
            if (new_state == true || new_state == false) {
                state.ui.search_active = new_state;
            } else if (new_state == 'toggle') {
                state.ui.search_active = !state.ui.search_active;
            }
        },
        set_environment: function(state, environment) {
            // Sets the environment for the app. If the environment is empty, we assume production
            state.app.environment = 'production';
            if (environment) {
                state.app.environment = environment;
            }
        },
        set_user_token: function(state, token) {
            // Sets the user token for the app
            state.app.user_token = token.token;

            // Set the fields in the local token object
            for (let key of Object.keys(state.api_data.user_token_object)) {
                if (key in token) {
                    state.api_data.user_token_object[key] = token[key];
                    if (key == 'expiration') {
                        // Prepare the date object so JavaScript knows it is in UTC
                        if (token[key]) {
                            token[key] = token[key].replace(' ', 'T');
                            token[key] = new Date(token[key] + 'Z');
                            state.api_data.user_token_object[key] = token[key];
                            if (state.api_data.api_clients._updated) {
                                let current_token = null;
                                state.api_data.api_clients.clients.forEach(
                                    function(client) {
                                        current_token = client.user_tokens.find(
                                            function(user_token) {
                                                return (
                                                    user_token.token ==
                                                    state.api_data
                                                        .user_token_object.token
                                                );
                                            }
                                        );
                                    }
                                );

                                if (current_token) {
                                    current_token.expiration = token[key];
                                }
                            }
                        }
                    }
                }
            }
        },
        api_update_user_object: function(state, options = null) {
            // Method to update the user object

            // Set the object
            let api_options = {
                success: null,
                failed: null,
                force: false
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Update the object, if needed
            if (api_options.force || !state.api_data.user_object._updated) {
                // Retrieve the user object
                me_api_call({
                    group: 'aaa',
                    endpoint: 'user_object',
                    method: 'GET'
                })
                    .then(function(data) {
                        // Data received
                        state.api_data.user_object._updated = true;
                        state.api_data.user_object.fullname =
                            data.data.object.fullname;
                        state.api_data.user_object.username =
                            data.data.object.username;
                        state.api_data.user_object.email =
                            data.data.object.email;
                        state.api_data.user_object.password_date = new Date(
                            data.data.object.password_date + ' UTC'
                        );
                        state.api_data.user_object.second_factor_enabled =
                            data.data.object.second_factor_enabled;

                        // Run the callback (if there is any)
                        if (api_options.success) {
                            api_options.success(state.api_data.user_object);
                        }
                    })
                    .catch(function(data) {
                        // Run the callback (if there is any)
                        if (api_options.failed) {
                            api_options.failed(data);
                        }
                    });
            } else {
                api_options.success(state.api_data.user_object);
            }
        },
        api_save_user_object: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                user_object: null
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            me_api_call({
                group: 'aaa',
                endpoint: 'user_object',
                method: 'PATCH',
                data: api_options.user_object
            })
                .then(function(data) {
                    if (data.data.success) {
                        // Update the store
                        state.api_data.user_object.fullname =
                            api_options.user_object.fullname;
                        state.api_data.user_object.username =
                            api_options.user_object.username;
                        state.api_data.user_object.email =
                            api_options.user_object.email;

                        // Run the callback (if there is any)
                        if (api_options.success) {
                            api_options.success(state.api_data.user_object);
                        }
                    } else {
                        // API was not a succes
                        return Promise.reject(data.data.data_text);
                    }
                })
                .catch(function(data) {
                    // Something went wrong

                    // Run the callback (if there is any)
                    if (api_options.failed) {
                        api_options.failed(data);
                    }
                });
        },
        api_save_user_object_password_date: function(state) {
            // Sets the password-date for the user object to now
            state.api_data.user_object.password_date = new Date();
        },
        api_set_user_object_2nd_factor: function(state, enabled) {
            // Sets the 'second_factor_enabled' value to true or false so the application knows the
            // state of two-factor authentication
            state.api_data.user_object.second_factor_enabled = enabled == true;
        },
        api_update_api_clients: function(state, options = null) {
            // Method to update the API clients

            // Set the object
            let api_options = {
                success: null,
                failed: null,
                force: false,
                get_user_tokens: true
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Update the object, if needed
            if (
                api_options.force ||
                !state.api_data.api_clients._updated ||
                (!state.api_data.api_clients._updated_user_tokens &&
                    api_options.get_user_tokens)
            ) {
                // Retrieve the user object
                me_api_call({
                    group: 'api_clients',
                    endpoint: 'client',
                    method: 'GET'
                })
                    .then(function(data) {
                        state.api_data.api_clients._updated = true;

                        // Data received. First, we remove all data from the current list
                        state.api_data.api_clients.clients = [];

                        // Add the new data to the current list
                        data.data.dataset.data.forEach(function(element) {
                            if (element.expiration) {
                                element.expiration = new Date(
                                    element.expiration + ' UTC'
                                );
                            }

                            // Add a 'user tokens' property to the element
                            element.user_tokens = [];

                            // Add the element to the list
                            state.api_data.api_clients.clients.push(element);
                        });

                        if (api_options.get_user_tokens) {
                            // Now that we have the clients, we can retrieve the user tokens for this client
                            me_api_call({
                                group: 'aaa',
                                endpoint: 'user_token',
                                method: 'GET'
                            })
                                .then(function(data) {
                                    // Set 'updated' to true so it won't update again if needed
                                    state.api_data.api_clients._updated_user_tokens = true;

                                    // Add the user-tokens to the client-objects
                                    data.data.dataset.data.forEach(function(
                                        element
                                    ) {
                                        // Convert the date-fields to a Date object
                                        element.created = new Date(
                                            element.created + ' UTC'
                                        );
                                        if (element.expiration) {
                                            element.expiration = new Date(
                                                element.expiration + ' UTC'
                                            );
                                        }

                                        // Find the client token that belongs to this one
                                        let api_client = state.api_data.api_clients.clients.find(
                                            function(client) {
                                                return (
                                                    client.id ==
                                                    element.client_token
                                                );
                                            }
                                        );

                                        if (api_client) {
                                            // Add the user token to the client-object
                                            api_client.user_tokens.push(
                                                element
                                            );
                                        }
                                    });

                                    // Run the callback (if there is any)
                                    if (api_options.success) {
                                        api_options.success(
                                            state.api_data.api_clients.clients
                                        );
                                    }
                                })
                                .catch(function(data) {
                                    // Run the callback (if there is any)
                                    if (api_options.failed) {
                                        api_options.failed(data);
                                    }
                                });
                        } else {
                            // Run the callback (if there is any)
                            if (api_options.success) {
                                api_options.success(
                                    state.api_data.api_clients.clients
                                );
                            }
                        }
                    })
                    .catch(function(data) {
                        // Run the callback (if there is any)
                        if (api_options.failed) {
                            api_options.failed(data);
                        }
                    });
            } else {
                api_options.success(state.api_data.api_clients.clients);
            }
        },
        api_update_api_user_token: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                fields: {
                    id: null,
                    expire: null,
                    description: null,
                    enabled: null
                }
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Check if a 'id' is given
            if (api_options.fields.id == null) {
                if (api_options.failed) {
                    api_options.failed('No id given');
                }
                return;
            }

            // Find the local object
            var user_token = null;
            state.api_data.api_clients.clients.forEach(function(client) {
                if (user_token == null) {
                    user_token = client.user_tokens.find(function(user) {
                        return user.id == api_options.fields.id;
                    });
                }
            });

            // Make sure the 'expire' date is a dateformat that the API understands
            if ('expire' in api_options.fields) {
                // Save the old expire date-object to a temporary variable
                var old_expire = api_options.fields.expire;

                if (api_options.fields.expire != null) {
                    // Convert to UTC and replace the characters we don't need
                    api_options.fields.expire = api_options.fields.expire.toISOString();
                    api_options.fields.expire = api_options.fields.expire.replace(
                        'T',
                        ' '
                    );
                    api_options.fields.expire = api_options.fields.expire.replace(
                        'Z',
                        ''
                    );
                    api_options.fields.expire = api_options.fields.expire.replace(
                        '.000',
                        ''
                    );
                }
            }

            // Send the request
            me_api_call({
                group: 'aaa',
                endpoint: 'user_token',
                method: 'PATCH',
                data: api_options.fields
            })
                .then(function(data) {
                    // Update the local fields

                    // Update the expiration date
                    if ('expire' in api_options.fields) {
                        user_token.expiration = old_expire;

                        // Check if this is the local token
                        if (
                            user_token.token ==
                            state.api_data.user_token_object.token
                        ) {
                            state.api_data.user_token_object.expiration = old_expire;
                        }
                    }

                    // Update the description
                    if (api_options.fields.description != null) {
                        user_token.description = api_options.fields.description;

                        // Check if this is the local token
                        if (
                            user_token.token ==
                            state.api_data.user_token_object.token
                        ) {
                            state.api_data.user_token_object.description =
                                api_options.fields.description;
                        }
                    }

                    // Update the disabled state
                    if (api_options.fields.enabled != null) {
                        user_token.enabled = api_options.fields.enabled;
                    }

                    // Execute the callback
                    if (api_options.success) {
                        api_options.success(data);
                    }
                })
                .catch(function(error) {
                    if (api_options.failed) {
                        api_options.failed(error);
                    }
                });
        },
        api_update_api_add_user_token: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                fields: {
                    client_id: null
                }
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Check if a 'id' is given
            if (api_options.fields.client_id == null) {
                if (api_options.failed) {
                    api_options.failed('No ID given');
                }
                return;
            }

            // Find the client in the local cache
            let client = state.api_data.api_clients.clients.find(function(
                client
            ) {
                return client.id == api_options.fields.client_id;
            });
            if (client == undefined) {
                if (api_options.failed) {
                    api_options.failed('No client found');
                }
                return;
            }

            // Send the request
            me_api_call({
                group: 'aaa',
                endpoint: 'user_token',
                method: 'POST',
                data: api_options.fields
            })
                .then(function(data) {
                    // Add the new object to the local cache
                    let new_object = data.data.object;
                    client.user_tokens.push(new_object);

                    // Execute the callback
                    if (api_options.success) {
                        api_options.success(data);
                    }
                })
                .catch(function(error) {
                    if (api_options.failed) {
                        api_options.failed(error);
                    }
                });
        },
        api_update_api_delete_user_token: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                fields: {
                    id: null
                }
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Check if a 'id' is given
            if (api_options.fields.id == null) {
                if (api_options.failed) {
                    api_options.failed('No ID given');
                }
                return;
            }

            // Find the token in the local cache
            let user_token = null;
            let client_index = null;
            let user_index = null;
            state.api_data.api_clients.clients.forEach(function(
                client,
                index_client
            ) {
                if (user_token == null) {
                    user_token = client.user_tokens.find(function(
                        user,
                        index_user
                    ) {
                        client_index = index_client;
                        user_index = index_user;
                        return user.id == api_options.fields.id;
                    });
                }
            });
            if (user_token == null) {
                if (api_options.failed) {
                    api_options.failed('No user token given');
                }
                return;
            }

            // Local this
            let vue_this = this;

            // Send the request
            me_api_call({
                group: 'aaa',
                endpoint: 'user_token',
                method: 'DELETE',
                data: api_options.fields
            })
                .then(function(data) {
                    // Remove the element from the state
                    Vue.delete(
                        state.api_data.api_clients.clients[client_index]
                            .user_tokens,
                        user_index
                    );

                    // Execute the callback
                    if (api_options.success) {
                        api_options.success(data);
                    }
                })
                .catch(function(error) {
                    if (api_options.failed) {
                        api_options.failed(error);
                    }
                });
        },
        api_update_api_user_token_title: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                description: null
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Execute the API
            // Local this
            let vue_this = this;

            // Send the request
            me_api_call({
                group: 'aaa',
                endpoint: 'set_token_description',
                method: 'PATCH',
                data: { description: api_options.description }
            })
                .then(function(data) {
                    // Update the local state
                    state.api_data.user_token_object.description =
                        api_options.description;

                    // Search if there is a token in the cache that needs to be updated
                    if (state.api_data.api_clients._updated) {
                        let current_token = null;
                        state.api_data.api_clients.clients.forEach(function(
                            client
                        ) {
                            current_token = client.user_tokens.find(function(
                                user_token
                            ) {
                                return (
                                    user_token.token ==
                                    state.api_data.user_token_object.token
                                );
                            });
                        });

                        if (current_token) {
                            current_token.description = api_options.description;
                        }
                    }

                    // Execute the callback
                    if (api_options.success) {
                        api_options.success(data);
                    }
                })
                .catch(function(error) {
                    if (api_options.failed) {
                        api_options.failed(error);
                    }
                });
        },
        update_user_settings: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                force: false
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            if (api_options.force || !state.app.user_config._updated) {
                // Do the call
                me_client_call({
                    endpoint: 'user_settings'
                })
                    .then(function(data) {
                        state.app.user_config.config = data.data;
                        state.app.user_config._updated = true;
                        if (api_options.success) {
                            api_options.success(data.data);
                        }
                    })
                    .catch(function(error) {
                        if (api_options.failed) {
                            api_options.failed();
                        }
                    });
            } else {
                if (api_options.success) {
                    api_options.success(state.app.user_config.config);
                }
            }
        },
        save_user_settings: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                config: state.app.user_config.config
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Do the call
            me_client_call({
                endpoint: 'user_settings',
                method: 'POST',
                data: api_options.config
            })
                .then(function(data) {
                    state.app.user_config.config = JSON.parse(
                        JSON.stringify(api_options.config)
                    );
                    state.app.user_config._updated = true;
                    if (api_options.success) {
                        api_options.success();
                    }
                })
                .catch(function(error) {
                    if (api_options.failed) {
                        api_options.failed();
                    }
                });
        },
        add_local_actions: function(state, actions) {
            // Method to add local actions
            if (Array.isArray(actions)) {
                actions.forEach(function(action) {
                    Vue.set(
                        state.ui.local_actions,
                        state.ui.local_actions.length,
                        action
                    );
                });
            }
        },
        local_actions_set_show: function(state, options) {
            // Set the 'show' state for a specific local action. The options object should contain
            // at least the following attributes:
            // - id: the id of the local option to set
            // - show: eiter true, false or 'toggle' to determine the new state of the option
            state.ui.local_actions.forEach(function(action) {
                if (action.id == options.id) {
                    action.show = options.show;
                }
            });
        },
        global_actions_set_show: function(state, options) {
            // Set the 'show' state for a specific local action. The options object should contain
            // at least the following attributes:
            // - id: the id of the local option to set
            // - show: eiter true, false or 'toggle' to determine the new state of the option
            state.ui.actions.forEach(function(action) {
                if (action.id == options.id) {
                    action.show = options.show;
                }
            });
        },
        remove_local_actions: function(state) {
            // Method to remove all local actions
            state.ui.local_actions = new Array();
        },
        api_update_api_client_token: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                fields: {
                    id: null,
                    name: null,
                    version: null,
                    publisher: null,
                    enabled: null
                }
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Check if a 'id' is given
            if (api_options.fields.id == null) {
                if (api_options.failed) {
                    api_options.failed('No id given');
                }
                return;
            }

            // Find the local object
            var client_token = null;
            client_token = state.api_data.api_clients.clients.find(function(
                client
            ) {
                return client.id == api_options.fields.id;
            });

            // Send the request
            me_api_call({
                group: 'api_clients',
                endpoint: 'client',
                method: 'PATCH',
                data: api_options.fields
            })
                .then(function(data) {
                    // Update the local fields

                    // Update the disabled state
                    if (api_options.fields.enabled != null) {
                        client_token.enabled = api_options.fields.enabled;
                    }

                    // Update the name
                    if (api_options.fields.name != null) {
                        client_token.app_name = api_options.fields.name;
                    }

                    // Update the version
                    if (api_options.fields.version != null) {
                        client_token.app_version = api_options.fields.version;
                    }

                    // Update the publisher
                    if (api_options.fields.publisher != null) {
                        client_token.app_publisher =
                            api_options.fields.publisher;
                    }

                    // Update the expiration
                    if ('expire' in api_options.fields) {
                        client_token.expiration = api_options.fields.expire;
                    }

                    // Execute the callback
                    if (api_options.success) {
                        api_options.success(data);
                    }
                })
                .catch(function(error) {
                    if (api_options.failed) {
                        api_options.failed(error);
                    }
                });
        },
        add_api_client: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                fields: {
                    name: null,
                    version: null,
                    publisher: null
                }
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Send the API call to add the client
            // Send the request
            me_api_call({
                group: 'api_clients',
                endpoint: 'client',
                method: 'POST',
                data: api_options.fields
            })
                .then(function(data) {
                    // Add to local clients
                    let client_object = data.data.object;
                    client_object.user_tokens = new Array();
                    Vue.set(
                        state.api_data.api_clients.clients,
                        state.api_data.api_clients.clients.length,
                        client_object
                    );

                    // Execute the callback
                    if (api_options.success) {
                        api_options.success(data);
                    }
                })
                .catch(function(error) {
                    if (api_options.failed) {
                        api_options.failed(error);
                    }
                });
        },
        api_update_api_delete_client_token: function(state, options) {
            // Set the object
            let api_options = {
                success: null,
                failed: null,
                fields: {
                    id: null
                }
            };

            // Loop through the given object and set the values to the local object
            if (options) {
                for (let key of Object.keys(options)) {
                    api_options[key] = options[key];
                }
            }

            // Check if a 'id' is given
            if (api_options.fields.id == null) {
                if (api_options.failed) {
                    api_options.failed('No ID given');
                }
                return;
            }

            // Find the token in the local cache
            let client_token = null;
            let client_index = null;
            client_token = state.api_data.api_clients.clients.find(function(
                client,
                index
            ) {
                client_index = index;
                return client.id == api_options.fields.id;
            });
            if (client_token == null) {
                if (api_options.failed) {
                    api_options.failed('No valid client token given');
                }
                return;
            }

            // Local this
            let vue_this = this;

            // Send the request
            me_api_call({
                group: 'api_clients',
                endpoint: 'client',
                method: 'DELETE',
                data: api_options.fields
            })
                .then(function(data) {
                    // Remove the element from the state
                    Vue.delete(
                        state.api_data.api_clients.clients,
                        client_index
                    );

                    // Execute the callback
                    if (api_options.success) {
                        api_options.success(data);
                    }
                })
                .catch(function(error) {
                    if (api_options.failed) {
                        api_options.failed(error);
                    }
                });
        }
    }
});
</script>
