<template>
  <me-modal id='modal_change_password' title='Change your password' ref='modal'>
    <form class='ui form'>
      <me-input type='password' label='Current password' id='current_pw' icon='lock'></me-input>
      <me-input type='password' label='New password' id='new_pw_1' icon='lock'></me-input>
      <me-input type='password' label='Repeat new password' id='new_pw_2' icon='lock'></me-input>
    </form>
    <template v-slot:actions>
      <me-button v-on:click='cancel'>Cancel</me-button>
      <me-button primary label_icon='lock' label_position='right'>Change password</me-button>
    </template>
  </me-modal>
</template>

<script>
import me_modal from './me-modal'
import me_input from './../components/me-input'
import me_button from './../components/me-button'

export default {
  name: 'me-modal-changepassword',
  components: {
    'me-modal': me_modal,
    'me-input': me_input,
    'me-button': me_button
  },
  methods: {
    cancel: function() {
      this.$refs.modal.hide();
    }
  }
}
</script>