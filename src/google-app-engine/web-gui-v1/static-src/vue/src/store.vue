/* A global store for Vue. Will be used to store state information about the application */

<script>
import Vue from 'vue';
import Vuex from 'vuex';

// Make sure Vue knows to use Vuex
Vue.use(Vuex);

// Export the store
export default new Vuex.Store({
    state: {
        ui: {
            media_type: null,
            search_active: false,
            menu_open: true,
            sidebar_available: true,
            sidebar_open: true
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
        },
        set_sidebar_state: function(state, new_state) {
            // Method to set the state of the sidebar; open or closed. When the 'new_state' is set
            // to true, the sidebar should be open. Whe the 'new_state' is set to false, the menu
            // should be closed
            state.ui.sidebar_open = new_state;
        }
    }
});
</script>