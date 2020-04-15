<!-- Vue component for the login-form -->
<template>
  <div id='me-dashboard-main-menu'>
    <!--Component-->
    <div class='menu' id='menu-main'>
      <div v-for='menuitem in menuitems' class='menu-section'>
        <h1>{{ menuitem.group }}</h1>
        <ul>
          <li v-for='subitem in menuitem.items'><i v-bind:class='[ subitem.icon, "icon" ]'></i><span>{{ subitem.title }}</span></li>
        </ul>
      </div>
    </div>
    <!--/Component-->
    <!--Component-->
    <div class='menu menu-second' id='menu-notebook'>
      <div class='menu-section'>
        <h1>Notes</h1>
        <ul>
          <li><i class='folder open outline icon'></i><span>Een label</span></li>
          <li><i class='folder open outline icon'></i><span>Een label</span></li>
          <li><i class='folder open outline icon'></i><span>Een label</span></li>
          <li><i class='folder open outline icon'></i><span>Een label</span></li>
          <li><i class='markdown icon'></i><span>Een notitie</span></li>
          <li><i class='markdown icon'></i><span>Een notitie</span></li>
          <li><i class='markdown icon'></i><span>Een notitie</span></li>
        </ul>
      </div>
    </div>
    <!--/Component-->
  </div>
</template>

<script>
// Export the dashboard
export default {
  name: 'me-dashboard-main-menu',
  data: function() {
    return {
      menuitems: [
        {
          group: 'Menu',
          items: [ { title: 'Dashboard', icon: 'columns' }, { title: 'Feed', icon: 'list' }, { title: 'Notebook', icon: 'clipboard outline' } ]
        },
        {
          group: 'Music',
          items: [ { title: 'Events', icon: 'music' }, { title: 'Making music', icon: 'guitar' } ]
        }
      ]
    }
  }
}
</script>