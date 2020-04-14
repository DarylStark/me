<!-- Vue component for the a 'menu button' in the dashboard header -->
<template>
  <div id='me-dashboard-button-options'>

    <div class="ui pointing dropdown top right" ref='dropdown'>
      <i class="ellipsis vertical icon"></i>
      <div class="menu">
        <div class="item" v-if='$store.state.ui.sidebar_available'>
          <i class="bars icon"></i>
            Show sidebar
        </div>
        <div class="divider" v-if='$store.state.ui.sidebar_available'></div>
        <div class="item">
          <i class="terminal icon"></i>
            Command palette
        </div>
        <div class="item">
          <i class="redo icon"></i>
            Reload page
        </div>
      </div>
    </div>

  </div>
</template>

<!-- The script that gets exported from the file -->
<script>

import '../../semantic/dist/semantic'
import '../../semantic/dist/components/dropdown'

export default {
  name: 'me-dashboard-button-options',
  mounted: function() {
    // Add the 'dropdown' functionality of Semantic UI to the dropdown
    $(this.$refs.dropdown).dropdown({ action: 'hide' });
  }
}
</script>