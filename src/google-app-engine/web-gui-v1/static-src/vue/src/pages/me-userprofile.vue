<template>
  <div id='me-content-userprofile'>
    <me-h1>
      <i class="user circle icon"></i>
      User Profile
    </me-h1>
  </div>
</template>

<script>
import me_h1 from '../components/me-h1'

export default {
  name: 'me-content-userprofile',
  components: {
    'me-h1': me_h1
  }
}
</script>
