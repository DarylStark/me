<!-- Vue component for the login-form -->
<template>
  <div id='me-loginform'>
    <me-card raised>
      <div ref='credentials' id='form-login' v-bind:class='{ hidden: second_factor_show }'>
        <me-h1 inverted>Login</me-h1>
        <form class='ui form' v-on:submit.prevent='login'>
          <me-input label='Username' v-model='fields.username' ref='username' id='username' icon='user' placeholder='Username' v-bind:disabled='status_waiting'></me-input>
          <me-input label='Password' v-model='fields.password' ref='password' id='password' icon='lock' placeholder='Password' v-bind:disabled='status_waiting' type='password'></me-input>
          <button class='fluid ui primary button' v-bind:class='{ loading: status_waiting }' v-bind:disabled='login_can_continue'>Login</button>
        </form>
      </div>
      <div ref='second_factor' id='form-second-factor' v-bind:class='{ visible: second_factor_show }'>
        <me-h1 inverted>Please provide second factor</me-h1>
        <form class='ui form' v-on:submit.prevent='login'>
          <p>Please provide the code from your authenticator app</p>
          <me-input ref='second_factor_field' v-model='fields.second_factor' id='2nd-factor' icon='key' placeholder='Second factor code' v-bind:disabled='status_waiting'></me-input>
          <button class='fluid ui primary button' v-bind:class='{ loading: status_waiting }' v-bind:disabled='login_can_continue'>Login</button>
        </form>
      </div>
    </me-card>
  </div>
</template>

<script>
// Import the needed components
import vue_cookies from 'vue-cookies'
import me_card from './components/me-card'
import me_h1 from './components/me-h1'
import me_input from './components/me-input'
import axios from 'axios'

// Export the form
export default {
  name: 'me-loginform',
  components: {
    'me-card': me_card,
    'me-h1': me_h1,
    'me-input': me_input,
  },
  data: function() {
    return {
      fields: {
        username: null,
        password: null,
        second_factor: null
      },
      second_factor_show: false,
      status_waiting: false
    }
  },
  computed: {
    login_can_continue: function() {
      return (this.fields.username == null || this.fields.password == null || this.fields.username == '' || this.fields.password == '' || this.status_waiting);
    }
  },
  methods: {
    focus: function(field) {
      // Method to focus a specific field
      this.$refs[field].focus();
    },
    login: function() {
      // Create the data to use to log in
      let login_data = {
        'username': this.fields.username,
        'password': this.fields.password
      }

      // Set to loading
      this.status_waiting = true;

      // Check if we have a second factor. If we do, add it to the options
      if (this.fields.second_factor) {
        login_data.second_factor = this.fields.second_factor;
      }

      // Local this
      let vue_this = this;

      // Send the login-request
      axios({
        method: 'POST',
        url: '/ui/client/login',
        data: login_data
      }).then(function(data) {
        if ('2nd_factor_required' in data.data) {
          // A second factor is needed. Present the correct form to the user
          vue_this.status_waiting = false;
          vue_this.$refs.second_factor_field.select();
          vue_this.second_factor_show = true;
        } else {
          vue_cookies.set('user_token', data.data.user_token, Infinity);
          window.location.replace('/ui/home');
        }
      }).catch(function(error) {
        // Whoops, something went wrong. Redirect the user back
        vue_this.$refs.username.select();
        vue_this.second_factor_show = false;
        vue_this.fields.username = null;
        vue_this.fields.password = null;
        vue_this.fields.second_factor = null;
        vue_this.status_waiting = false;

        $('body').toast({
          position: 'top center',
          message: 'The credentials you entered were not correct',
          closeIcon: true,
          displayTime: 'auto',
          showIcon: 'user',
          class: 'error'
        });
      });
    }
  },
  mounted: function() {
    // When the object is mounted, we can set focus to the username
    this.$refs.username.focus();
  }
}
</script>