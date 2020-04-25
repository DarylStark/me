<template>
  <me-modal id='modal_disable_2nd_factor' title='Disable two-factor authentication' ref='modal'>
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
  name: 'me-modal-disabble-2nd-factor',
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
      this.saving = false;
    },
    submit: function() {
      console.log('Disabling');
      this.saving = true;
    }
  }
}
</script>