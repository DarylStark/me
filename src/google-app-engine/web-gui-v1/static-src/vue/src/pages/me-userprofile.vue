<template>
  <div id='me-content-userprofile'>
    <me-page-title icon='user circle'>
      User profile
      <template v-slot:actions>
        <me-button primary :disabled='!changed'>Save</me-button>
      </template>
    </me-page-title>
    <me-grid hcenter>
      <me-grid-column>
        <me-card raised>
          <me-h1 inverted>User profile</me-h1>
          <form class='ui form'>
            <me-input label='Username' id='username' placeholder='Username' icon='user' v-model='user_object.username' v-on:input='changed = true'></me-input>
            <me-input label='Full name' id='fullname' placeholder='Full name' icon='user circle' v-model='user_object.fullname' v-on:input='changed = true'></me-input>
            <me-input label='E-mail address' id='email' placeholder='E-mail address' icon='user' v-model='user_object.email' v-on:input='changed = true'></me-input>
          </form>
        </me-card>
      </me-grid-column>
      <me-grid-column>
        <me-card raised>
          <me-h1 inverted>Authentication options</me-h1>
          <div id='authentication'>
            <div>
              <div>Your password is 98793845 days old.</div>
              <div>
                <me-button>Change password</me-button>
              </div>
            </div>
            <div>
              <div>You have enabled two-factor authentication. Good for you!</div>
              <div>
                <me-button>Disable</me-button>
              </div>
            </div>
          </div>
        </me-card>
      </me-grid-column>
    </me-grid>
  </div>
</template>

<script>
import me_page_title from '../components/me-page-title'
import me_grid from '../components/me-grid'
import me_grid_column from '../components/me-grid-column'
import me_card from '../components/me-card'
import me_input from '../components/me-input'
import me_h1 from '../components/me-h1'
import me_button from '../components/me-button'
import me_api_call from '../me/api_call'

export default {
  name: 'me-content-userprofile',
  components: {
    'me-page-title': me_page_title,
    'me-grid': me_grid,
    'me-grid-column': me_grid_column,
    'me-card': me_card,
    'me-input': me_input,
    'me-h1': me_h1,
    'me-button': me_button
  },
  data: function() {
    return {
      user_object: {
        fullname: null,
        username: null,
        email: null
      },
      changed: false
    }
  },
  created: function() {
    // Local this
    var vue_this = this;

    // Make sure there is a user profile
    this.$store.commit('api_update_user_object', {
        success: function(data) {
            vue_this.user_object.fullname = data.fullname;
            vue_this.user_object.username = data.username;
            vue_this.user_object.email = data.email;
        }
    });

    // We don't need a sidebar on this page. Disable it.
    this.$store.commit('set_sidebar_availability', false);
  }
}
</script>
