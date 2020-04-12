<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
  <div id='me-dashboard-search' v-bind:class='{ active: search_active }'>
      <me-input id='search' ref='search' icon='search' icon_position='right' transparent='true' placeholder='Search ...' v-show='search_active' v-on:escape='toggle_search' v-on:enter='start_search'></me-input>
      <i class='search icon' v-if='!search_active' v-on:click='toggle_search'></i>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
import me_input from './me-input'

export default {
  name: 'me-dashboard-search',
  components: {
    'me-input': me_input
  },
  data: function() {
    return {
      search_active: false
    }
  },
  methods: {
    toggle_search: function() {
      // Method to activate or deactive the search bar
      this.search_active = !this.search_active;

      // Set focus to the search-input. Because Vue doesn't update the DOM immidiatly, we have to
      // wait for it to do so with the 'nextTick' method.
      this.$nextTick(function() {
        this.$refs.search.focus();
      });
    },
    start_search: function() {
      // Method to start the search
      // TODO: Implement
      console.log('Searching for "' + this.$refs.search.value + '"');
    }
  }
}
</script>