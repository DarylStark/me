<template>
  <div id='me-content-userprofile'>
    <me-page-title icon='user circle'>
      User profile
      <template v-slot:actions>
        <!-- Component -->
        <button class='ui primary button' disabled>Save</button>
        <!-- /Component -->
      </template>
    </me-page-title>
    <me-grid>
      <me-grid-column>
        <me-card raised>
          Hier kun je je profiel editten
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

export default {
  name: 'me-content-userprofile',
  components: {
    'me-page-title': me_page_title,
    'me-grid': me_grid,
    'me-grid-column': me_grid_column,
    'me-card': me_card
  },
  created: function() {
    // We don't need a sidebar on this page. Disable it.
    this.$store.commit('set_sidebar_availability', false);
  }
}
</script>
