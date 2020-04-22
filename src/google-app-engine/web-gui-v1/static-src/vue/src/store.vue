<script>
/* A global store for Vue. Will be used to store state information about the application */
import Vue from 'vue';
import Vuex from 'vuex';
import me_api_call from './me/api_call'

// Make sure Vue knows to use Vuex
Vue.use(Vuex);

// Export the store
export default new Vuex.Store({
    state: {
        app: {
            environment: null,
            user_token: null
        },
        ui: {
            media_type: null,
            search_active: false,
            menu_open: true,
            sidebar_available: true,
            sidebar_open: true
        },
        api_data: {
            user_object: {
                _updated: false,
                username: null,
                fullname: null,
                email: null,
                password_date: null,
                second_factor_enabled: false
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
            if (state.ui.media_type == 'phone' || state.ui.media_type == 'tablet') {
                state.ui.menu_open = false;
                state.ui.sidebar_open = false;
            } else {
                state.ui.menu_open = true;
                state.ui.sidebar_open = true;
            }
        },
        set_menu_state: function(state, new_state) {
            // Method to set the state of the menu; open or closed. When the 'new_state' is set to
            // true, the menu should be open. Whe the 'new_state' is set to false, the menu should
            // be closed
            state.ui.menu_open = new_state;

            // When we are on mobile, the state of the menu is set to open AND the sidebar is
            // already open, we have to close the sidebar. Otherwise, they are in eachothers way
            if (state.ui.media_type == 'phone' && state.ui.sidebar_open && new_state) {
                state.ui.sidebar_open = false;
            }
        },
        set_sidebar_state: function(state, new_state) {
            // Method to set the state of the sidebar; open or closed. When the 'new_state' is set
            // to true, the sidebar should be open. Whe the 'new_state' is set to false, the menu
            // should be closed
            state.ui.sidebar_open = new_state;

            // When we are on mobile, the state of the sidebar is set to open AND the menu is
            // already open, we have to close the menu. Otherwise, they are in eachothers way
            if (state.ui.media_type == 'phone' && state.ui.menu_open && new_state) {
                state.ui.menu_open = false;
            }
        },
        set_sidebar_availability: function(state, new_availability) {
            // Enable or disable the sidebar. For some pages, the sidebar is not needed and has to
            // be disabled to not confuse the user
            state.ui.sidebar_available = new_availability;
        },
        set_environment: function(state, environment) {
            // Sets the environment for the app. If the environment is empty, we assume production
            state.app.environment = 'production';
            if (environment) {
                state.app.environment = environment;
            }
        },
        set_user_token: function(state, user_token) {
            // Sets the user token for the app
            state.app.user_token = user_token;
        },
        api_update_user_object: function(state, options = null) {
            // Method to update the user object

            // Set the object
            let api_options = {
                success: null,
                failed: null,
                force: false
            }

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
                  group: 'aaa', endpoint: 'user_object',
                  method: 'GET'
                }).then(function(data) {
                  // Data received
                  state.api_data.user_object._updated = true;
                  state.api_data.user_object.fullname = data.data.object.fullname;
                  state.api_data.user_object.username = data.data.object.username;
                  state.api_data.user_object.email = data.data.object.email;
                  state.api_data.user_object.password_date = new Date(data.data.object.password_date + ' UTC');
                  state.api_data.user_object.second_factor_enabled = data.data.object.second_factor_enabled;

                  // Run the callback (if there is any)
                  if (api_options.success) { api_options.success(state.api_data.user_object); }
                }).catch(function(data) {
                  // Something went wrong
                  console.log(data);

                  // TODO: Error message

                  // Run the callback (if there is any)
                  if (api_options.failed) { api_options.failed(data); }
                });
            } else {
                api_options.success(state.api_data.user_object);
            }
        }
    }
});
</script>
