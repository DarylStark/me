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
      <me-cell padding v-bind:span='2'>
        <me-card raised wide>
          <me-h1 inverted>User profile</me-h1>
          <form class='ui form'>
            <me-input label='Username' :disabled='saving' id='username' placeholder='Username' icon='user' v-model='user_object.username' v-on:input='changed = true'></me-input>
            <me-input label='Full name' :disabled='saving' id='fullname' placeholder='Full name' icon='user circle' v-model='user_object.fullname' v-on:input='changed = true'></me-input>
            <me-input label='E-mail address' :disabled='saving' id='email' placeholder='E-mail address' icon='user' v-model='user_object.email' v-on:input='changed = true'></me-input>
          </form>
        </me-card>
      </me-cell>
      <me-cell padding v-bind:span='2'>
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

export default {
  name: 'me-content-userprofile',
  components: {
    'me-page-title': me_page_title,
    'me-grid': me_grid,
    'me-cell': me_cell,
    'me-card': me_card,
    'me-input': me_input,
    'me-h1': me_h1,
    'me-button': me_button
  },
  data: function() {
    return {
      user_object: {
        fullname: null,
        username: null,
        email: null
      },
      changed: false,
      saving: false
    }
  },
  computed: {
    password_age: function() {
      // Computed property for the password age
      let today = new Date(new Date().toDateString());
      let pw_date = new Date(this.$store.state.api_data.user_object.password_date.toDateString())
      let age = (today - pw_date) / 1000 / 3600 / 24;
      return age;
    }
  },
  methods: {
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
    save_profile: function() {
      // Method to save the profile

      this.saving = true;
      this.changed = false;

      // Local this
      var vue_this = this;

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
          
          // Show an error
          $('body').toast({
            position: 'bottom center',
            message: 'Couldn\'t save your userprofile; ' + error,
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        }
      });
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
    }
  },
  created: function() {
    // Set the fields
    this.set_field_values();

    // We don't need a sidebar on this page. Disable it.
    this.$store.commit('set_sidebar_availability', false);
  }
}
</script>
