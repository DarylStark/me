<template>
  <div class='client'>
    <me-flexline class='client_title'>
      <div>
        <p class='title'>{{ client.app_name }} <span class='publisher'>({{ client.app_publisher }})</span></p>
        <p class='version'>Version: {{ client.app_version }}</p>
      </div>
      <div class='spacer'></div>
      <div>
        <me-button>Add user token</me-button>
      </div>
    </me-flexline>
    <me-userprofile-api-user v-for='user_token in client.user_tokens' v-bind:key='user_token.id' v-bind:user_token='user_token'></me-userprofile-api-user>
  </div>
</template>

<script>
import me_flexline from './me-flexline'
import me_button from './me-button'
import me_userprofile_api_user from './me-userprofile-api-user'

export default {
  name: 'me-userprofile-api-client',
  components: {
    'me-flexline': me_flexline,
    'me-button': me_button,
    'me-userprofile-api-user': me_userprofile_api_user
  },
  props: {
    client: { mandatory: true }
  }
}
</script>