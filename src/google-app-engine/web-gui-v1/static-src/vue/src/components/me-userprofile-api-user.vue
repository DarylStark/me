<template>
  <div class='user_token'>
    <me-flexline>
      <div>
          <p v-if='user_token.description' class='title'>{{ user_token.description }}</p>
          <p v-if='!user_token.description' class='title'>No title given</p>
          <p v-if='user_token.expiration'>{{ expire }}</p>
          <p v-if='!user_token.expiration'>This token will not expire</p>
      </div>
      <div class='spacer'></div>
      <div class='actions'>
        <div class='ui icon red button' data-tooltip='Disable user token' data-position='top left' v-if='user_token.enabled' ><i class='power off icon'></i></div>
        <div class='ui icon green button' data-tooltip='Enable user token' data-position='top left' v-if='!user_token.enabled'><i class='play icon'></i></div>
        <div class='ui icon button' data-tooltip='Reveal token' data-position='top left' v-on:click='show_token = !show_token'><i class='key icon'></i></div>
        <div class='ui icon button' data-tooltip='Rename token' data-position='top center'><i class='edit icon'></i></div>
        <div v-bind:class='[ "ui", { disabled: !user_token.expiration }, "icon", "button" ]' data-tooltip='Refresh token' data-position='top right'><i class='sync icon'></i></div>
        <div class='ui icon red button' data-tooltip='Remove token' data-position='top right'><i class='trash icon'></i></div>
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
  </div>
</template>

<script>
import me_flexline from './me-flexline'

export default {
  name: 'me-userprofile-api-user',
  computed: {
    expire: function() {
      let date_options = { year: 'numeric', month: 'long', day: 'numeric' };
      return this.user_token.expiration.toLocaleTimeString(undefined, date_options);
    }
  },
  data: function() {
    return {
      show_token: false,
      copied: false
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
    }
  },
  components: {
    'me-flexline': me_flexline
  },
  props: {
    user_token: { mandatory: true }
  }
}
</script>