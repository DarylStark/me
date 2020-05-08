<template>
  <div class='user_token'>
    <me-flexline class='ui segment'>
      <div class='grower client_title'>
          <p v-if='user_token.description' class='title'>{{ user_token.description }}</p>
          <p v-if='!user_token.description' class='title'>No title given</p>
          <p v-if='user_token.expiration'>Will expire on: {{ expire }} <span v-if='expired' class='expired'>(expired)</span></p>
          <p v-if='!user_token.expiration'>This token will not expire</p>
      </div>
      <div class='actions' v-show='!renaming'>
        <span data-tooltip='Disable user token' data-position='top left' v-if='user_token.enabled'>
          <me-button icon='power off' class='red' v-bind:loading='loading_disable' v-bind:disabled='loading_disable' v-on:click='disable_token'></me-button>
        </span>
        <span data-tooltip='Enable user token' data-position='top left' v-if='!user_token.enabled'>
          <me-button icon='play' class='green' v-bind:loading='loading_disable' v-bind:disabled='loading_disable' v-on:click='enable_token'></me-button>
        </span>
        <span data-tooltip='Reveal token' data-position='top left'>
          <me-button icon='key' v-on:click='show_token = !show_token' v-bind:class='{ "green": show_token }'></me-button>
        </span>
        <span data-tooltip='Rename token' data-position='top left'>
          <me-button icon='edit' v-on:click='rename_token'></me-button>
        </span>
        <div class='inline'>
          <div class='ui calendar' ref='expire_date_button'>
            <span data-tooltip='Set expire date and time' data-position='top right'>
              <me-button icon='clock outline' class='calendar' v-bind:loading='loading_date' v-bind:disabled='loading_date'></me-button>
            </span>
          </div>
        </div>
        <span data-tooltip='Set to not expire' data-position='top right'>
          <me-button icon='infinity' v-bind:loading='loading_infinity' v-bind:disabled='loading_infinity || !user_token.expiration' v-on:click='set_token_infinite'></me-button>
        </span>
        <span data-tooltip='Remove token' data-position='top right'>
          <me-button icon='trash' class='red' v-on:click='delete_token' v-bind:loading='loading_delete' v-bind:disabled='loading_delete'></me-button>
        </span>
      </div>
    </me-flexline>
    <me-flexline  v-if='show_token' class='token_line'>
      <div class='grower' ref='token'>{{ user_token.token }}</div>
      <div class='ui icon button' data-tooltip='Copy token' data-position='top right' v-on:click='copy_token' v-if='!copied'>
        <i class='copy icon'></i>
      </div>
      <div class='ui button' data-tooltip='Copy token' data-position='top right' v-on:click='copy_token' v-if='copied'>
        Copied to clipboard!
      </div>
    </me-flexline>
    <me-flexline v-if='renaming' class='rename'>
      <div class='grower'>
        <me-input id='new_name' placeholder='Enter a name for this token' fluid v-model='description' ref='new_name' transparent v-on:enter='rename_token_send' v-on:escape='cancel_rename'></me-input>
      </div>
      <div>
        <span data-tooltip='Save' data-position='top right'>
          <me-button icon='times' class='red' v-on:click='cancel_rename' v-bind:disabled='loading'></me-button>
          <me-button icon='check' class='green' v-on:click='rename_token_send' v-bind:loading='loading' v-bind:disabled='loading'></me-button>
        </span>
      </div>
    </me-flexline>
  </div>
</template>

<script>
import me_flexline from './me-flexline'
import me_button from './me-button'
import me_input from './me-input'
import Vue from 'vue'

export default {
  name: 'me-userprofile-api-user',
  computed: {
    expire: function() {
      let date_options = { year: 'numeric', month: 'long', day: 'numeric' };
      return this.user_token.expiration.toLocaleTimeString(undefined, date_options);
    },
    expired: function() {
      let today = new Date();
      return this.user_token.expiration < today;
    }
  },
  data: function() {
    return {
      show_token: false,
      copied: false,
      loading: false,
      loading_date: false,
      loading_disable: false,
      renaming: false,
      description: null,
      loading_delete: false,
      loading_infinity: false
    }
  },
  methods: {
    copy_token: function() {
      // Copy the token code to the clipboard

      // Local this
      let vue_this = this;

      // Copy the token the the clipboard
      navigator.clipboard.writeText(this.user_token.token).then(function() {
        vue_this.copied = true;

        setTimeout(function() { vue_this.copied = false; }, 2000);
      });
    },
    rename_token: function() {
      // Start the renaming
      this.renaming = true;
      this.show_token = false;

      // Local this
      let vue_this = this;

      // Focus the rename input
      Vue.nextTick().then(function() {
        vue_this.$refs.new_name.focus();
        vue_this.$refs.new_name.select();
      });
    },
    cancel_rename: function() {
      // Cancel the renaming
      this.renaming = false;
      this.description = this.user_token.description;
    },
    rename_token_send: function() {
      // Method that actually updates the tokenname
      this.loading = true;

      // Local this
      let vue_this = this;

      // We have the time, let's update the user token
      this.$store.commit('api_update_api_user_token', {
        success: function() {
          vue_this.loading = false;
          vue_this.renaming = false;
          $('body').toast({
            position: 'bottom center',
            message: 'Updated description',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'success'
          });
        },
        failed: function() {
          vue_this.loading = false;
          $('body').toast({
            position: 'bottom center',
            message: 'Something went wrong while updating the description',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        },
        fields: {
          description: this.description,
          id: this.user_token.id,
        }
      })
    },
    disable_token: function() {
      // Method that actually updates the tokenname
      this.loading_disable = true;

      // Local this
      let vue_this = this;

      // We have the time, let's update the user token
      this.$store.commit('api_update_api_user_token', {
        success: function() {
          vue_this.loading_disable = false;
          vue_this.renaming = false;
          $('body').toast({
            position: 'bottom center',
            message: 'Disabled token',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'success'
          });
        },
        failed: function() {
          vue_this.loading_disable = false;
          $('body').toast({
            position: 'bottom center',
            message: 'Something went wrong while disabling the token',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        },
        fields: {
          enabled: false,
          id: this.user_token.id,
        }
      })
    },
    enable_token: function() {
      // Method that actually updates the tokenname
      this.loading_disable = true;

      // Local this
      let vue_this = this;

      // We have the time, let's update the user token
      this.$store.commit('api_update_api_user_token', {
        success: function() {
          vue_this.loading_disable = false;
          vue_this.renaming = false;
          $('body').toast({
            position: 'bottom center',
            message: 'Enabled token',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'success'
          });
        },
        failed: function() {
          vue_this.loading_disable = false;
          $('body').toast({
            position: 'bottom center',
            message: 'Something went wrong while enabeling the token',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        },
        fields: {
          enabled: true,
          id: this.user_token.id,
        }
      });
    },
    set_token_infinite: function() {
      // Method that actually updates the tokenname
      this.loading_infinity = true;

      // Local this
      let vue_this = this;

      // We have the time, let's update the user token
      this.$store.commit('api_update_api_user_token', {
        success: function() {
          vue_this.loading_infinity = false;
          vue_this.renaming = false;
          $('body').toast({
            position: 'bottom center',
            message: 'Set token to not expire',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'success'
          });
        },
        failed: function() {
          vue_this.loading_infinity = false;
          $('body').toast({
            position: 'bottom center',
            message: 'Something went wrong while setting the token to not expire',
            closeIcon: true,
            displayTime: 'auto',
            showIcon: 'user',
            class: 'error'
          });
        },
        fields: {
          expire: null,
          id: this.user_token.id,
        }
      });
    },
    delete_token: function() {
      // Local this
      let vue_this = this;

      this.loading_delete = true;

      // Ask the user if he is sure to remove this token
      $('body').toast({
        message: 'Do you really want to remove this user token?',
        displayTime: 0,
        class: 'white',
        position: 'top center',
        actions:	[{
          text: 'Yes',
          icon: 'check',
          class: 'green',
          click: function() {
              vue_this.$store.commit('api_update_api_delete_user_token', {
                success: function() {
                  vue_this.loading_delete = false;
                  vue_this.renaming = false;
                  $('body').toast({
                    position: 'bottom center',
                    message: 'Deleted token',
                    closeIcon: true,
                    displayTime: 'auto',
                    showIcon: 'user',
                    class: 'success'
                  });
                },
                failed: function() {
                  vue_this.loading_disable = false;
                  $('body').toast({
                    position: 'bottom center',
                    message: 'Something went wrong while deleting the token',
                    closeIcon: true,
                    displayTime: 'auto',
                    showIcon: 'user',
                    class: 'error'
                  });
                },
                fields: {
                  enabled: true,
                  id: vue_this.user_token.id,
                }
              })
          }
        },{
          icon: 'ban',
          text: 'No',
          class: 'red',
          click: function() {
            vue_this.loading_delete = false;
          }
        }]
      });
    },
    expire_date_set: function(date, mode) {
      if (mode == 'minute') {
        this.loading_date = true;

        // Local this
        let vue_this = this;

        // We have the time, let's update the user token
        this.$store.commit('api_update_api_user_token', {
          success: function() {
            vue_this.loading_date = false;
            $('body').toast({
              position: 'bottom center',
              message: 'Updated expiration date and time',
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'success'
            });
          },
          failed: function() {
            vue_this.loading_date = false;
            $('body').toast({
              position: 'bottom center',
              message: 'Something went wrong while updating the expiration date and time',
              closeIcon: true,
              displayTime: 'auto',
              showIcon: 'user',
              class: 'error'
            });
          },
          fields: {
            expire: date,
            id: this.user_token.id,
          }
        })
      }
    }
  },
  components: {
    'me-flexline': me_flexline,
    'me-button': me_button,
    'me-input': me_input
  },
  props: {
    user_token: { mandatory: true }
  },
  created: function(){
    this.description = this.user_token.description;
  },
  mounted: function() {
    // Create the calendar object
    $(this.$refs.expire_date_button).calendar({
      firstDayOfWeek: 1,
      onSelect: this.expire_date_set,
      selectAdjacentDays: true
    });
  }
}
</script>
