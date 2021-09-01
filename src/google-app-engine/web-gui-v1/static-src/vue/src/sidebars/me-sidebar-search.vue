<!-- Vue component for the login-form -->
<template>
    <div id='me-sidebar-search'>
        <h1>Search preferences</h1>
        <div class='ui fluid selection dropdown'>
            <input name='profile' type='hidden' />
            <i class='dropdown icon'></i>
            <div class='default text'>Default profile</div>
            <div class='menu'>
                <div class='item' v-bind:data-value='profile.name' v-bind:key='profile.name' v-for='profile in search_profiles'>{{ profile.name }}</div>
            </div>
        </div>
        <div class='checkboxes'>
            <div class='all'>
                <div class='ui slider checkbox'>
                    <input name='search_in_all' type='checkbox' v-model='active_options.search_in_all' />
                    <label>Search all</label>
                </div>
            </div>
            <div class='options' v-if='!active_options.search_in_all'>
                <div class='ui slider checkbox'>
                    <input name='search_in_all' type='checkbox' v-model='active_options.search_in_user_tokens' />
                    <label>Search user tokens</label>
                </div>
                <div class='ui slider checkbox'>
                    <input name='search_in_all' type='checkbox' v-model='active_options.search_in_client_tokens' />
                    <label>Search client tokens</label>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'me-sidebar-search',
    mounted: function() {
        // Local this
        let vue_this = this;

        // Create the dropdown
        $('.ui.dropdown').dropdown({
            clearable: true,
            onChange: function(value) {
                vue_this.change_profile(value);
            }
        });
    },
    data: function() {
        return {
            active_options: null,
            changed: false
        };
    },
    computed: {
        default_profile: function() {
            // Returns the default search profile
            return this.$store.state.app.user_config.config.search_profiles.filter(
                function(item) {
                    return item.name == null;
                }
            );
        },
        search_profiles: function() {
            // Returns the search profiles sorted and without the 'null' element. The 'null' element
            // will be used as the default search profile
            return this.$store.state.app.user_config.config.search_profiles
                .sort(function(a, b) {
                    // If the name is 'null', we have the default one
                    if (a.name == null || b.name == null) {
                        return 1;
                    }

                    // Compare the names
                    if (a.name.toUpperCase() > b.name.toUpperCase()) {
                        return 1;
                    } else if (a.name.toUpperCase() < b.name.toUpperCase()) {
                        return -1;
                    }

                    // If they are the same
                    return 0;
                })
                .filter(function(item) {
                    return item.name != null;
                });
        }
    },
    created: function() {
        // Local this
        let vue_this = this;

        // Get the user settings
        this.$store.commit('update_user_settings', {
            success: function(data) {
                // Set the current search profile to default
                vue_this.change_profile(null);
            },
            failed: function() {
                $('body').toast({
                    position: 'bottom center',
                    message: "Couldn't retrieve your search profiles",
                    closeIcon: true,
                    displayTime: 'auto',
                    showIcon: 'user',
                    class: 'error'
                });
            }
        });
    },
    methods: {
        change_profile: function(profile) {
            // Find the profile
            let new_profile = new Array();
            if (profile) {
                new_profile = this.$store.state.app.user_config.config.search_profiles.filter(
                    function(element) {
                        return element.name == profile;
                    }
                );
            } else {
                new_profile = this.default_profile;
            }

            if (new_profile.length == 1) {
                this.active_options = new_profile[0];
            }
        }
    }
};
</script>