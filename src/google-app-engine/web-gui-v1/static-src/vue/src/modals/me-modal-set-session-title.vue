<template>
  <me-modal id='modal_set_session_title' title='Set session title' ref='modal' v-on:hidden='reset' v-on:showing='show'>
    <p v-if='$store.state.api_data.user_token_object.description'>The current name for this session is <b>{{ $store.state.api_data.user_token_object.description }}</b></p>
    <p v-if='!$store.state.api_data.user_token_object.description'>This session has <b>no name</b> currently</p>
    <me-input id='new_name' fluid v-model='description' ref='input' :disabled='saving' v-on:enter='submit'></me-input>
    <template v-slot:actions>
      <me-button v-on:click='close' :disabled='saving'>Cancel</me-button>
      <me-button primary label_icon='edit' label_position='right' v-on:click='submit' :loading='saving' :disabled='saving'>Update</me-button>
    </template>
  </me-modal>
</template>

<script>
import Vue from 'vue'
import me_modal from './me-modal'
import me_button from './../components/me-button'
import me_input from './../components/me-input'

export default {
  name: 'me-modal-set-session-title',
  data: function() {
    return {
      saving: false,
      description: null
    }
  },
  components: {
    'me-modal': me_modal,
    'me-button': me_button,
    'me-input': me_input
  },
  methods: {
    show: function() {
      // Reset the fields
      this.reset()

      // Local this
      let vue_this = this;

      // Select the text in the input
      Vue.nextTick(function () {
        vue_this.$refs.input.select();
      });
    },
    close: function() {
      this.$refs.modal.hide();
    },
    reset: function() {
      this.description = this.$store.state.api_data.user_token_object.description;
    },
    submit: function() {
      if (!this.saving) {
        // Save the new description
        this.saving = true;

        // Local this
        let vue_this = this;

        // Execute the API
        this.$store.commit('api_update_api_user_token_title', {
          success: function() {
            vue_this.saving = false;
            vue_this.close();
            $('body').toast({
              position: 'bottom center',
              message: 'Your session is renamed',
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'success'
            });
          },
          failed: function() {
            vue_this.saving = false;
            $('body').toast({
              position: 'bottom center',
              message: 'Something went wrong while renaming your session',
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'error'
            });
          },
          description: this.description
        });
      }
    }
  }
}
</script>