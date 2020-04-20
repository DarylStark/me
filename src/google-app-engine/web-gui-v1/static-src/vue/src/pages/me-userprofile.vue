<template>
  <div id='me-content-userprofile'>
    <me-page-title icon='user circle'>
      User profile
      <template v-slot:actions>
        <!-- Component -->
        <button class='ui primary button' disabled='enabled'>Save</button>
        <!-- /Component -->
      </template>
    </me-page-title>
    <me-grid hcenter>
      <me-grid-column>
        <me-card raised>
          <me-h1 inverted>User profile</me-h1>
          <form class='ui form'>
            <me-input label='Username' id='username' placeholder='Username' icon='user'></me-input>
            <me-input label='Full name' id='fullname' placeholder='Full name' icon='user circle'></me-input>
            <me-input label='E-mail address' id='email' placeholder='E-mail address' icon='user'></me-input>
          </form>
        </me-card>
      </me-grid-column>
      <me-grid-column>
        <me-card raised>
          <me-h1 inverted>Authentication options</me-h1>
          <div class='padding' id='authentication'>
            <div>
              <div><i class='lock icon'></i> Reset password</div>
              <div>
                <me-button primary>Change password</me-button>
              </div>
            </div>
            <div>
              <div><i class='key icon'></i> Two factor authentication</div>
              <div>
                <me-button primary>Disable</me-button>
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
  created: function() {
    // TODO: Retrieve the user details

    // We don't need a sidebar on this page. Disable it.
    this.$store.commit('set_sidebar_availability', false);
  }
}
</script>
