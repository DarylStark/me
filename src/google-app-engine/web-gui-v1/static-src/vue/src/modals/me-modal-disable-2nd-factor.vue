<template>
  <me-modal id='modal_disable_2nd_factor' title='Disable two-factor authentication' ref='modal' v-on:hidden='reset'>
    <div class='description'>
      <div class='ui header'>Are you sure you want to disable two-factor authentication?</div>
      <p>Doing this greatly reduces the security of your account and should only be done when you know exactly what you're doing!</p>
    </div>
    <template v-slot:actions>
      <me-button v-on:click='close' :disabled='saving'>Cancel</me-button>
      <me-button primary label_icon='lock open' label_position='right' v-on:click='submit' :loading='saving' :disabled='saving'>Disable</me-button>
    </template>
  </me-modal>
</template>

<script>
import me_modal from './me-modal'
import me_button from './../components/me-button'
import me_api_call from '../me/api_call'

export default {
  name: 'me-modal-disable-2nd-factor',
  data: function() {
    return {
      saving: false
    }
  },
  components: {
    'me-modal': me_modal,
    'me-button': me_button
  },
  methods: {
    close: function() {
      this.$refs.modal.hide();
    },
    reset: function() {
      this.saving = false;
    },
    submit: function() {
      // The user wants to disable two-factor authentication
      this.saving = true;

      // Local this
      let vue_this = this;

      // Start the correct endpoint in the API
      me_api_call({
        group: 'aaa', endpoint: 'disable_two_factor',
        method: 'PATCH',
      }).then(function(data) {
        // Success! Close the modal
        vue_this.close();

        // Given an success toast
        $('body').toast({
          position: 'bottom center',
          message: 'Disabled two-factor authentication',
          closeIcon: true,
          displayTime: 'auto',
          showIcon: 'user',
          class: 'success'
        });

        // Set the new password date in the store
        vue_this.$store.commit('api_set_user_object_2nd_factor', false);
      }).catch(function(data) {
        vue_this.saving = false;

        // Show an error
        $('body').toast({
          position: 'bottom center',
          message: data,
          closeIcon: true,
          displayTime: 'auto',
          showIcon: 'user',
          class: 'error'
        });
      });
    }
  }
}
</script>