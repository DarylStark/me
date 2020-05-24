<template>
  <div id='me-content-userprofile'>
    <me-page-title icon='user circle'>
      User profile
      <template v-slot:actions>
        <me-button primary :disabled='!changed' :loading='saving' v-on:click='save_profile'>Save</me-button>
        <me-button :disabled='!changed' v-on:click='set_field_values'>Cancel</me-button>
      </template>
    </me-page-title>
    <me-grid>
      <me-cell padding v-bind:span='4' class='tablet-span-8'>
        <me-card raised wide>
          <me-h1 inverted>User profile</me-h1>
          <form class='ui form'>
            <me-input v-on:enter='save_profile' label='Username' :disabled='saving' id='username' placeholder='Username' icon='user' v-model='user_object.username' v-on:input='changed = true' :error='fields.username_error'></me-input>
            <me-input v-on:enter='save_profile' label='Full name' :disabled='saving' id='fullname' placeholder='Full name' icon='user circle' v-model='user_object.fullname' v-on:input='changed = true' :error='fields.fullname_error'></me-input>
            <me-input v-on:enter='save_profile' label='E-mail address' :disabled='saving' id='email' placeholder='E-mail address' icon='user' v-model='user_object.email' v-on:input='changed = true' :error='fields.email_error'></me-input>
          </form>
        </me-card>
      </me-cell>
      <me-cell padding v-bind:span='4'>
        <me-card raised wide>
          <me-h1 inverted>Authentication options</me-h1>
          <div class='action_button'>
            <div v-if='password_age == 1'>Your password is <b>{{ password_age }} day</b> old.</div>
            <div v-if='password_age > 1'>Your password is <b>{{ password_age }} days</b> old.</div>
            <div v-if='password_age == 0'>You changed your password today</div>
            <div>
              <me-button v-on:click='show_change_password_dialog'>Change password</me-button>
            </div>
          </div>
          <div class='action_button' v-if='$store.state.api_data.user_object.second_factor_enabled'>
            <div>Two-factor authentication is <b>enabled</b></div>
            <div>
              <me-button v-on:click='show_disable_2nd_factor_dialog'>Disable</me-button>
            </div>
          </div>
          <div class='action_button' v-if='!$store.state.api_data.user_object.second_factor_enabled'>
            <div>Two-factor authentication is <b>disabled</b></div>
            <div>
              <me-button v-on:click='show_enable_2nd_factor_dialog'>Enable</me-button>
            </div>
          </div>
        </me-card>
      </me-cell>
      <me-cell padding v-bind:span='4'>
        <me-card raised wide>
          <me-h1 inverted>Session options</me-h1>
          <div class='action_button'>
            <div v-if='$store.state.api_data.user_token_object.description'>Your session is named <b>{{ $store.state.api_data.user_token_object.description }}</b></div>
            <div v-if='!$store.state.api_data.user_token_object.description'>This session has <b>no name</b></div>
            <div><me-button v-on:click='rename_session'>Rename session</me-button></div>
          </div>
          <div class='action_button'>
            <div v-if='$store.state.api_data.user_token_object.expiration'>Your session will expire in <b>{{ user_session_expire_period }}</b></div>
            <div v-if='!$store.state.api_data.user_token_object.expiration'>This session will not expire</div>
            <div><me-button v-bind:disabled='!user_session_refreshable' v-on:click='refresh_token' v-bind:loading='loading_refresh'>Refresh session</me-button></div>
          </div>
        </me-card>
      </me-cell>
    </me-grid>
    <me-page-title icon='user circle'>
      GUI settings
      <template v-slot:actions>
        <me-button primary :disabled='!user_settings_changed' :loading='saving_user_settings' v-on:click='save_user_settings'>Save</me-button>
        <me-button :disabled='!user_settings_changed' v-on:click='set_user_settings_field_values'>Cancel</me-button>
      </template>
    </me-page-title>
    <me-grid>
      <me-cell padding v-bind:span='4' class='tablet-span-8'>
        <me-card raised wide class='date_formats'>
          <me-h1 inverted>Date and time formats</me-h1>
          <form class='ui form'>
            <div class='setting_field'>
              <me-input :disabled='saving_user_settings' v-on:input='user_settings_changed = true' label='Datetime format' id='datetime_format' placeholder='Datetime format' icon='clock outline' v-model='user_settings.datetime_formats.datetime_format'></me-input>
              <p class='example_title'>Example</p>
              <div class='dateformat_example'>{{ example_datetime_format }}</div>
            </div>
            <div class='setting_field'>
              <div class='ui slider checkbox'>
                <input :disabled='saving_user_settings' type='checkbox' name='24h'  v-on:input='user_settings_changed = true' v-model='user_settings.datetime_formats.show_24h'>
                <label>Use 24h notation in timepickers</label>
              </div>
            </div>
          </form>
        </me-card>
      </me-cell>
    </me-grid>
    <me-page-title icon='key'>
      User tokens
      <template v-slot:actions>
        <me-button primary v-on:click='set_clients_forced' v-bind:disabled='!loaded_clients'>Reload</me-button>
      </template>
    </me-page-title>
    <me-grid>
      <me-cell padding v-bind:span='12'>
        <me-card raised wide class='clients'>
          <me-h1 inverted>Authorized clients</me-h1>
          <me-userprofile-api-client v-if='loaded_clients' v-for='client in $store.state.api_data.api_clients.clients' v-bind:key='client.id' v-bind:client='client'></me-userprofile-api-client>
          <div class='loading_text' v-if='!loaded_clients'>
            <div class='ui active inline loader'></div>
            Loading the API clients
          </div>
        </me-card>
      </me-cell>
    </me-grid>
  </div>
</template>

<script>
import me_page_title from '../components/me-page-title'
import me_grid from '../components/me-grid'
import me_cell from '../components/me-cell'
import me_card from '../components/me-card'
import me_input from '../components/me-input'
import me_h1 from '../components/me-h1'
import me_button from '../components/me-button'
import me_api_call from '../me/api_call'
import eventbus from '../eventbus'
import me_userprofile_api_client from '../components/me-userprofile-api-client'
import strftime from 'strftime'
import { refresh_user_token } from '../me/global_actions'

export default {
  name: 'me-content-userprofile',
  components: {
    'me-page-title': me_page_title,
    'me-grid': me_grid,
    'me-cell': me_cell,
    'me-card': me_card,
    'me-input': me_input,
    'me-h1': me_h1,
    'me-button': me_button,
    'me-userprofile-api-client': me_userprofile_api_client
  },
  data: function() {
    return {
      user_object: {
        fullname: null,
        username: null,
        email: null
      },
      fields: {
        username_error: false,
        fullname_error: false,
        email_error: false
      },
      user_settings: {
        datetime_formats: {
          datetime_format: null,
          show_24h: false
        }
      },
      changed: false,
      user_settings_changed: false,
      saving: false,
      saving_user_settings: false,
      loaded_clients: false,
      loading_refresh: false
    }
  },
  watch: {
    changed: function() {
      // Update the 'show' attribute of the 'save-account' item in the local-actions for the
      // command palette
      this.$store.commit('local_actions_set_show', {
        id: 'save-account',
        show: this.changed
      })
    },
    user_settings_changed: function() {
      // Update the 'show' attribute of the 'save-profile' item in the local-actions for the
      // command palette
      this.$store.commit('local_actions_set_show', {
        id: 'save-profile',
        show: this.user_settings_changed
      })
    }
  },
  computed: {
    user_session_expire_period: function() {
      let today = new Date();
      let difference = (this.$store.state.api_data.user_token_object.expiration.getTime() - today.getTime()) / 1000;
      let difference_minutes = Math.round(difference / 60);
      let difference_hours = Math.round(difference / 3600);

      if (difference_minutes > 59) {
        return difference_hours + ' hours';
      } else {
        return difference_minutes + ' minutes';
      }
    },
    user_session_refreshable: function() {
      // Method to check if a user-session is refreshable
      if (this.$store.state.api_data.user_token_object.expiration) {
        let today = new Date();
        let difference = (this.$store.state.api_data.user_token_object.expiration.getTime() - today.getTime()) / 1000;
        let difference_hours = difference / 3600;
        return difference_hours < 23;
      }

      // Return false if all of above wasn't true
      return false;
    },
    password_age: function() {
      // Computed property for the password age
      let today = new Date(new Date().toDateString());
      let pw_date = new Date(this.$store.state.api_data.user_object.password_date.toDateString())
      let age = (today - pw_date) / 1000 / 3600 / 24;
      return age;
    },
    example_datetime_format: function() {
      let format = this.user_settings.datetime_formats.datetime_format;
      if (format) {
        return strftime(format);
      } else {
        return 'Please fill in a datetime format'
      }
    }
  },
  methods: {
    refresh_token: function() {
      // Local this
      let vue_this = this;
      this.loading_refresh = true;

      refresh_user_token({
        success: function() {
          // Display a success toast
          vue_this.loading_refresh = false;
          $('body').toast({
              position: 'bottom center',
              message: 'Your usersession is refreshed',
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'success'
          });
        },
        failed: function() {
          vue_this.loading_refresh = false;
          $('body').toast({
              position: 'bottom center',
              message: 'Something went wrong while refreshing your usersession',
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'error'
          });
        },
      });
    },
    set_field_values: function() {
      // Method to reset the form to the default values

      // Local this
      var vue_this = this;

      // Set the fields for the profile
      this.$store.commit('api_update_user_object', {
          success: function(data) {
              vue_this.user_object.fullname = data.fullname;
              vue_this.user_object.username = data.username;
              vue_this.user_object.email = data.email;
          }
      });

      // Reset 'changed'
      this.changed = false;
    },
    set_clients: function(force = false) {
      // Method to set the API clients

      // Local this
      var vue_this = this;

      // Set the fields for the profile
      this.$store.commit('api_update_api_clients', {
          success: function(data) {
            vue_this.loaded_clients = true;
          },
          failed: function() {
            vue_this.loaded_clients = true;
            $('body').toast({
              position: 'bottom center',
              message: 'Something went wrong while retrieving the API clients',
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'error'
            });
          },
          force: force
      });
    },
    set_clients_forced: function() {
      this.loaded_clients = false;
      this.set_clients(true);
    },
    save_profile: function() {
      // Method to save the profile

      if (this.changed) {
        this.saving = true;
        this.changed = false;

        // Local this
        var vue_this = this;

        // Set all errors to false
        this.fields.username_error = false;
        this.fields.fullname_error = false;
        this.fields.email_error = false;

        // Local this
        this.$store.commit('api_save_user_object', {
          user_object: {
            fullname: this.user_object.fullname,
            username: this.user_object.username,
            email: this.user_object.email
          },
          success: function() {
            // Succes! The profile is saved
            vue_this.saving = false;

            $('body').toast({
              position: 'bottom center',
              message: 'Your userprofile is saved',
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'success'
            });
          },
          failed: function(error) {
            // The API failed
            vue_this.changed = true;
            vue_this.saving = false;

            // Create a error text based on the given error
            let error_text = 'unknown error'
            if (error == 'username_in_use') { error_text = 'username is already in use'; vue_this.fields.username_error = true; }
            if (error == 'username_invalid') { error_text = 'username is not valid'; vue_this.fields.username_error = true; }
            if (error == 'fullname_invalid') { error_text = 'full name is not valid'; vue_this.fields.fullname_error = true; }
            if (error == 'email_in_use') { error_text = 'e-mailaddress is already in use'; vue_this.fields.email_error = true; }
            if (error == 'email_invalid') { error_text = 'e-mailaddress is invalid'; vue_this.fields.email_error = true; }
            
            // Show an error
            $('body').toast({
              position: 'bottom center',
              message: 'Couldn\'t save your userprofile; ' + error_text,
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'error'
            });
          }
        });
      }
    },
    show_change_password_dialog: function() {
      // Show the change password dialog
      eventbus.$emit('show_modal', 'modal_change_password');
    },
    show_disable_2nd_factor_dialog: function() {
      // Show the disable 2nd factor dialog
      eventbus.$emit('show_modal', 'modal_disable_2nd_factor');
    },
    show_enable_2nd_factor_dialog: function() {
      // Show the enable 2nd factor dialog
      eventbus.$emit('show_modal', 'modal_enable_2nd_factor');
    },
    rename_session: function() {
      eventbus.$emit('show_modal', 'modal_set_session_title');
    },
    set_user_settings_field_values: function() {
      // Local this
      let vue_this = this;

      this.user_settings_changed = false;

      // Set the user settings
      this.$store.commit('update_user_settings', {
        success: function(data) {
          // Set the local settings
          vue_this.user_settings.datetime_formats.show_24h = data.datetime_formats['show_24h'];
          vue_this.user_settings.datetime_formats.datetime_format = data.datetime_formats.datetime_format;
        },
        failed: function() {
          $('body').toast({
            position: 'bottom center',
            message: 'Couldn\'t retrieve your user settings',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        }
      });
    },
    save_user_settings: function() {
      // Local this
      let vue_this = this;

      this.saving_user_settings = true;
      this.user_settings_changed = false;

      // Save the user settings
      this.$store.commit('save_user_settings', {
        config: this.user_settings,
        success: function(data) {
          vue_this.saving_user_settings = false;
          // Set the local settings
          $('body').toast({
            position: 'bottom center',
            message: 'Saved user settings',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'success'
          });
        },
        failed: function(error) {
          vue_this.saving_user_settings = false;
          $('body').toast({
            position: 'bottom center',
            message: 'Couldn\'t save your user settings',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        }
      });
    }
  },
  created: function() {
    // Set the fields
    this.set_field_values();

    // Set the user settings
    this.set_user_settings_field_values();

    // Set the API clients
    this.set_clients();

    // Local this
    let vue_this = this;

    // Add the local actions for this page. These actions will be visible in the command palette
    // TODO: Make sure these are only visible when there was a change
    this.$store.commit('add_local_actions', [
      {
        id: 'save-account',
        icon: 'save',
        title: 'Save user account settings',
        type: 'action',
        action: function(vue_instance) {
            vue_this.save_profile();
        },
        show: vue_this.changed
      },
      {
        id: 'save-profile',
        icon: 'save',
        title: 'Save user profile settings',
        type: 'action',
        action: function(vue_instance) {
            vue_this.save_user_settings();
        },
        show: vue_this.user_settings_changed
      }
    ]);

    // We don't need a sidebar on this page. Disable it.
    this.$store.commit('set_sidebar_availability', false);
  },
  beforeRouteLeave: function(to, from, next) {
    // When the user tries to leave the page before saving or resetting the information, we give the
    // user a warning and a chance to save the form first

    // Local this
    let vue_this = this;

    // Check if something has changed
    if (this.changed || this.user_settings_changed) {
      $('body').toast({
        message: 'You haven\'t saved the form yet. Are you sure you want to leave?',
        displayTime: 0,
        class: 'white',
        position: 'top center',
        title: 'Profile changed',
        actions: [
          {
            text: 'Yes',
            class: 'green',
            click: function() {
              vue_this.$store.commit('remove_local_actions');
              next(true);
            }
          }, {
            text: 'No',
            class: 'red',
            click: function() {
              next(false);
            }
          }
        ]
      });
    }
    else {
      this.$store.commit('remove_local_actions');
      next(true);
    }
  }
}
</script>
