<!-- Vue component for the login-form -->
<template>
  <div id='me-loginform'>
    <me-grid vcenter hcenter pageheight>
      <me-cell padding center v-bind:span=2>
        <me-card raised>
          <div ref='credentials' id='form-login'>
            <me-h1 inverted>{{ texts.header_credentials }}</me-h1>
            <form class='ui form' v-on:submit.prevent='login'>
              <me-input v-bind:label='texts.field_username' v-model='fields.username' ref='username' id='username' icon='user' v-bind:placeholder='texts.field_username_placeholder' v-bind:disabled="status_waiting"></me-input>
              <me-input v-bind:label='texts.field_password' v-model='fields.password' ref='password' id='password' icon='lock' v-bind:placeholder='texts.field_password_placeholder' v-bind:disabled="status_waiting" type='password'></me-input>
              <button class='fluid ui primary button' v-bind:class='{ loading: status_waiting }'>{{ texts.button_login }}</button>
            </form>
          </div>
          <div ref='second_factor' id='form-second-factor'>
            <me-h1 inverted>{{ texts.header_2nd_factor }}</me-h1>
            <form class='ui form' v-on:submit.prevent='login'>
              <p>Please provide the code from your authenticator app</p>
              <me-input ref='second_factor_field' v-model='fields.second_factor' id='2nd-factor' icon='key' v-bind:placeholder='texts.field_2nd_factor_placeholder' v-bind:disabled="status_waiting"></me-input>
              <button class='fluid ui primary button' v-bind:class='{ loading: status_waiting }'>{{ texts.button_login }}</button>
            </form>
          </div>
        </me-card>
      </me-cell>
    </me-grid>
  </div>
</template>

<script>
// Import the needed components
import vue_cookies from 'vue-cookies'
import me_grid from './components/me-grid'
import me_cell from './components/me-cell'
import me_card from './components/me-card'
import me_h1 from './components/me-h1'
import me_input from './components/me-input'
import axios from 'axios'
import jquery from 'jquery'

// Export the form
export default {
  name: 'me-loginform',
  components: {
    'me-grid': me_grid,
    'me-cell': me_cell,
    'me-card': me_card,
    'me-h1': me_h1,
    'me-input': me_input,
  },
  data: function() {
    return {
      texts: {
        header_credentials: 'Log in',
        header_2nd_factor: 'Second factor needed',
        field_username: 'Username',
        field_password: 'Password',
        field_2nd_factor: 'Second factor',
        field_username_placeholder: 'Username',
        field_password_placeholder:' Password',
        field_2nd_factor_placeholder: 'Second factor',
        button_login: 'Log in'
      },
      fields: {
        username: null,
        password: null,
        second_factor: null
      },
      status_waiting: false,
      status: 'login'
    }
  },
  methods: {
    focus: function(field) {
      // Method to focus a specific field
      this.$refs[field].focus();
    },
    login: function() {
      // Method to login the user

      // Create a variable that can be used as 'this' in the callback of the Axios request
      var vue_this = this;

      // Verify if the needed fields are filled in
      if (this.status == 'login') {
        if (this.fields.username == "" || this.fields.username == null ||
            this.fields.password == "" || this.fields.password == null) {
            return;
        }
      } else if (this.status == '2nd_factor') {
        if (this.fields.second_factor == "" || this.fields.second_factor == null) {
            return;
        }
      }

      // Make sure the form 'block's the needed fields
      this.status_waiting = true;

      // Create a data-object for Axios
      var login_data = {
        username: this.fields.username,
        password: this.fields.password
      }

      // Add Second Factor if it filled in
      if (this.fields.second_factor != "" && this.fields.second_factor != null) {
        login_data.second_factor = this.fields.second_factor;
      }

      // Send the POST to the login-backend
      axios.post('/ui/client/login', login_data).then(function(response) {
        vue_this.login_success(response);
      }).catch(function(error) {
        vue_this.login_failed(error);
      });
    },
    login_failed: function(error) {
      // Method that gets run when the logging in fails

      // Empty the password field
      this.fields.password = '';
      this.$refs.password.focus();

      // Make sure the form isn't blocked anymore
      this.status_waiting = false;

      // Transform back to the 'login' status
      this.transform('login');
    },
    login_success: function(data) {
      // Method that gets run when the logging in was a success

      // Check what response we got
      if ('2nd_factor_required' in data.data) {
        // We need a second-factor

        // Make sure the form isn't blocked anymore
        this.status_waiting = false;

        // Transform to second-factor form
        this.transform('2nd_factor');
      } else if ('user_token' in data.data) {
        // Correct credentials were given

        // Set as cookie and redirect the user to the homepage
        vue_cookies.set('user_token', data.data.user_token, Infinity);
        window.location.replace('/ui/home')
      } else {
        self.login_failed();
      }
    },
    transform: function(new_status) {
      // Method to transfer from one state to the other. From 'login' to '2nd factor' for instance

      // Create a variable that can be used as 'this' in the callback of the Axios request
      var vue_this = this;

      // From login > 2nd-factor
      if (this.status == 'login' && new_status == '2nd_factor') {
        // Set the stacking order
        jquery(this.$refs.second_factor).css('z-index', 20);
        jquery(this.$refs.credentials).css('z-index', 10);

        this.status = new_status;

        // Do the animation
        jquery(this.$refs.second_factor).animate({
          'margin-left': '0'
        }, {
          duration: 250,
          easing: 'swing',
          queue: false,
          complete: function() { vue_this.$refs.second_factor_field.focus(); }
        });
        jquery(this.$refs.credentials).animate({
          'margin-left': '-100%'
        }, {
          duration: 1000,
          easing: 'swing',
          queue: false
        });
      }

      // From 2nd-factor > login
      if (this.status == '2nd_factor' && new_status == 'login') {
        // Set the stacking order
        jquery(this.$refs.second_factor).css('z-index', 10);
        jquery(this.$refs.credentials).css('z-index', 20);

        // Empty the 2nd-factor field
        this.$refs.second_factor_field.value = undefined;

        this.status = new_status;

        // Do the animation
        jquery(this.$refs.second_factor).animate({
          'margin-left': '100%'
        }, {
          duration: 1000,
          easing: 'swing',
          queue: false
        });
        jquery(this.$refs.credentials).animate({
          'margin-left': '0'
        }, {
          duration: 250,
          easing: 'swing',
          queue: false,
          complete: function() { vue_this.$refs.password.focus(); }
        });
      }
    }
  },
  mounted: function() {
    // When the object is mounted, we can set focus to the username
    this.$refs.username.focus();
  }
}
</script>