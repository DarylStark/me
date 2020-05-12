<template>
  <me-modal id='modal_enable_2nd_factor' title='Enable two-factor authentication' ref='modal' v-on:hidden='reset'>
    <div class='description'>
      <div v-show='step == 1'>
        <p>Enabline two-factor authentication requires a app on your smartphone or a plugin in your webbrowser to generate one time passwords. Two apps you can use for this on Android are:</p>
        <ul>
          <li><a href='https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2' target='_blank'>Google Authenticater</a></li>
          <li><a href='https://play.google.com/store/apps/details?id=com.mufri.authenticatorplus' target='_blank'>Authenticater Plus</a></li>
        </ul>
        <p>When you installed a authenticator app, click <b>Next</b></p>
      </div>
      <div v-show='step == 2' class='center'>
        <p>Use the app you installed to scan the following QR-code</p>
        <div class='ui segment' v-if='!loaded_secret'>
          <div class='ui active inverted dimmer'>
            <div class='ui text loader'>Loading</div>
          </div>
        </div>
        <canvas id='canvas' v-show='loaded_secret'></canvas>
        <p>When done, click <b>Next</b></p>
      </div>
      <div v-show='step == 3'>
        <p>Enter the code that the authenitcation app gives you</p>
        <me-input id='code' ref='code' v-model='code' icon='lock' icon_position='left' placeholder='Code' v-on:enter='enable' :disabled='loading'></me-input>
      </div>
    </div>
    <template v-slot:actions>
      <me-button v-on:click='close' :loading='loading'>Cancel</me-button>
      <me-button primary label_icon='caret right' label_position='right' v-on:click='next' v-if='step < 3' :disabled='next_disabled' :loading='loading'>Next</me-button>
      <me-button primary label_icon='lock' label_position='right' v-on:click='enable' v-if='step == 3' :disabled='!code != "" && !code != null' :loading='loading'>Save</me-button>
    </template>
  </me-modal>
</template>

<script>
import me_modal from './me-modal'
import me_button from './../components/me-button'
import me_input from './../components/me-input'
import me_api_call from '../me/api_call'
import QRCode from 'qrcode'

export default {
  name: 'me-modal-enable-2nd-factor',
  data: function() {
    return {
      saving: false,
      step: 1,
      loaded_secret: false,
      code: null,
      loading: false
    }
  },
  computed: {
    next_disabled: function() {
      // Method that determines if the show_next button is visible
      if (this.step == 1) { return false; }
      if (this.step == 2 && this.loaded_secret == true) { return false; }

      return true;
    }
  },
  components: {
    'me-modal': me_modal,
    'me-button': me_button,
    'me-input': me_input
  },
  methods: {
    close: function() {
      this.$refs.modal.hide();
    },
    reset: function() {
      this.saving = false;
      this.step = 1;
      this.loaded_secret = false;
      this.loading = false;
      this.code = null;
    },
    next: function() {
      // Local this
      let vue_this = this;

      // Increase the step
      this.step++;

      // Generate the QRcode is we are on step 2
      if (this.step == 2) {
        this.loading = true;

        // Get the secret from the API
        me_api_call({
          method: 'PATCH',
          group: 'aaa', endpoint: 'enable_two_factor'
        }).then(function(data) {
          // Display the barcode
          vue_this.loaded_secret = true;
          vue_this.loading = false;

          let username = vue_this.$store.state.api_data.user_object.username;
          let data_url = 'otpauth://totp/Me:' + username + '?secret=' + data.data.object.secret + '&issuer=Me&digits=6';

          QRCode.toCanvas(document.getElementById('canvas'), data_url, function(error) {
            if (error) {
              $('body').toast({
                position: 'bottom center',
                message: 'Something went wrong while creating a QR code',
                closeIcon: true,
                displayTime: 'auto',
                showIcon: 'user',
                class: 'error'
              });
            }
          });
        }).catch(function(error) {
          vue_this.loading = false;
          // Show an error
          $('body').toast({
            position: 'bottom center',
            message: 'Couldn\'t retrieve a secret key',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        });
      }

      if (this.step == 3) {
        this.$refs.code.focus();
      }
    },
    enable: function() {
      // When the user entered the code

      // Local this
      let vue_this = this;

      this.loading = true;

      // Verify the given code
      me_api_call({
        method: 'PATCH',
        group: 'aaa', endpoint: 'verify_two_factor',
        data: {
          '2nd_factor': this.code
        }
      }).then(function(data) {
        // Check if it was success
        if (!data.data.success) { raise('incorrect'); }

        // It was
        vue_this.loading = false;
        vue_this.close();
        vue_this.$store.commit('api_set_user_object_2nd_factor', true);

        // Show an notifiaction
        $('body').toast({
          position: 'bottom center',
          message: 'You enabled two-factor authentication!',
          closeIcon: true,
          displayTime: 'auto',
          showIcon: 'user',
          class: 'success'
        });
      }).catch(function(error) {
        vue_this.loading = false;

        // Show an error
        $('body').toast({
          position: 'bottom center',
          message: 'Code isn\'t correct. Try again',
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