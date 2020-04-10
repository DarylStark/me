<!-- Vue component for the login-form -->
<template>
  <div id='me-loginform'>
    <me-grid>
      <me-grid-column>
        <me-card raised>
          <me-h1 inverted>{{ texts.header }}</me-h1>
          <form class='ui form' v-on:submit.prevent='login'>
              <me-input v-bind:label='texts.field_username' ref='username' id='username' icon='user' v-bind:placeholder='texts.field_username_placeholder' v-bind:disabled="status_waiting"></me-input>
              <me-input v-bind:label='texts.field_password' ref='password' id='password' icon='lock' v-bind:placeholder='texts.field_password_placeholder' v-bind:disabled="status_waiting" type='password'></me-input>
              <button class='fluid ui primary button' v-bind:class='{ loading: status_waiting }'>{{ texts.button_login }}</button>
          </form>
        </me-card>
      </me-grid-column>
    </me-grid>
  </div>
</template>

<script>
// Import the needed components
import me_grid from './components/me-grid'
import me_grid_column from './components/me-grid-column'
import me_card from './components/me-card'
import me_h1 from './components/me-h1'
import me_input from './components/me-input'
import axios from 'axios'

// Export the form
export default {
  components: {
    'me-grid': me_grid,
    'me-grid-column': me_grid_column,
    'me-card': me_card,
    'me-h1': me_h1,
    'me-input': me_input,
  },
  name: 'me-loginform',
  data: function() {
    return {
      texts: {
        header: 'Login',
        field_username: 'Username',
        field_password: 'Password',
        field_username_placeholder: 'Username',
        field_password_placeholder:' Password',
        button_login: 'Log in'
      },
      status_waiting: false
    }
  },
  methods: {
    focus: function(field) {
      // Method to focus a specific field
      this.$refs[field].focus();
    },
    login: function(form) {
      // Method to login the user

      // Make sure the form 'block's the needed fields
      this.status_waiting = true;

      // Create a variable that can be used as 'this' in the callback of the Axios request
      var vue_this = this;

      // Send the POST to the login-backend
      axios.post('/ui/client/login', {
        username: this.$refs.username.value,
        password: this.$refs.password.value
      }).then(function(response) {
        vue_this.login_success(response);
      }).catch(function(error) {
        vue_this.login_failed(error);
      });
    },
    login_failed: function(error) {
      // Method that gets run when the logging in fails

      // Make sure the form isn't blocked anymore
        this.status_waiting = false;

        console.log('Error: ');
        console.log(error);
    },
    login_success: function(data) {
      // Method that gets run when the logging in was a success

      // Make sure the form isn't blocked anymore
        this.status_waiting = false;

        console.log('Success: ' + data);
        console.log(data);
    },
  },
  mounted: function() {
    this.$refs.username.focus();
  }
}
</script>