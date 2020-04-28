<template>
  <me-modal id='modal_change_password' title='Change your password' ref='modal'>
    <form class='ui form'>
      <me-input type='password' v-on:enter='submit' label='Current password' id='current_pw' icon='lock' :disabled='saving' v-model='fields.current_pw' :error='current_pw_error'></me-input>
      <me-input type='password' v-on:enter='submit' label='New password' id='new_pw_1' icon='lock' :disabled='saving' v-model='fields.new_pw_1' :error='new_pw_1_error'></me-input>
      <me-input type='password' v-on:enter='submit' label='Repeat new password' id='new_pw_2' icon='lock' :disabled='saving' v-model='fields.new_pw_2' :error='new_pw_2_error'></me-input>
    </form>
    <template v-slot:actions>
      <me-button v-on:click='close' :disabled='saving'>Cancel</me-button>
      <me-button primary label_icon='lock' label_position='right' v-on:click='submit' :loading='saving' :disabled='saving'>Change password</me-button>
    </template>
  </me-modal>
</template>

<script>
import me_modal from './me-modal'
import me_input from './../components/me-input'
import me_button from './../components/me-button'
import me_api_call from '../me/api_call'

export default {
  name: 'me-modal-changepassword',
  data: function() {
    return {
      fields: {
        current_pw: null,
        new_pw_1: null,
        new_pw_2: null
      },
      current_pw_error: false,
      new_pw_1_error: false,
      new_pw_2_error: false,
      saving: false
    }
  },
  computed: {
    valid: function() {
      return !this.current_pw_error && !this.new_pw_1_error && !this.new_pw_2_error
    }
  },
  components: {
    'me-modal': me_modal,
    'me-input': me_input,
    'me-button': me_button
  },
  methods: {
    close: function() {
      this.$refs.modal.hide();
      this.fields.current_pw = null;
      this.fields.new_pw_1 = null;
      this.fields.new_pw_2 = null;
      this.saving = false;
    },
    validate: function() {
      // Validate the fields
      if (this.fields.current_pw == null || this.fields.current_pw == "") { this.current_pw_error = true; } else { this.current_pw_error = false; }
      if (this.fields.new_pw_1 == null || this.fields.new_pw_1 == "") { this.new_pw_1_error = true; } else { this.new_pw_1_error = false; }
      if (this.fields.new_pw_2 == null || this.fields.new_pw_2 == "") { this.new_pw_2_error = true; } else { this.new_pw_2_error = false; }
      if (this.fields.new_pw_1 != this.fields.new_pw_2) { this.new_pw_1_error = true; this.new_pw_2_error = true; }
    },
    submit: function() {
      // Validate the fields
      this.validate();

      if (this.valid) {
        // Everything was valid. Save the new password
        this.saving = true;

        // Local this
        let vue_this = this;

        me_api_call({
          group: 'aaa', endpoint: 'change_password',
          method: 'PATCH',
          data: {
            'current_pw': this.fields.current_pw,
            'new_pw': this.fields.new_pw_1
          }
        }).then(function(data) {
          if (data.data.success) {
            // Success! Close the modal
            vue_this.close();

            // Given an success toast
            $('body').toast({
              position: 'bottom center',
              message: 'Your password is changed',
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'success'
            });

            // Set the new password date in the store
            vue_this.$store.commit('api_save_user_object_password_date');
          } else {
            // API was not a succes
            return Promise.reject(data.data.data_text);
          }
        }).catch(function(data) {
          // Generate a decent error text
          let error_text = 'Unknown error';;

          if (data == 'new_pw_too_short') {
            error_text = 'The new password is too short';
            vue_this.new_pw_1_error = true;
            vue_this.new_pw_2_error = true;
          } else if (data == 'current_pw') {
            error_text = 'The current password is incorrect'
            vue_this.current_pw_error = true;
          } else if (data == 'new_pw_equal_to_current') {
            error_text = 'The new password should be different from the current password'
            vue_this.new_pw_1_error = true;
            vue_this.new_pw_2_error = true;
          }

          // Stop the loading
          vue_this.saving = false;

          // Show an error
          $('body').toast({
            position: 'bottom center',
            message: error_text,
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        });
      }
    }
  }
}
</script>