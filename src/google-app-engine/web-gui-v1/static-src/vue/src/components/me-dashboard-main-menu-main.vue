<template>
    <div class='menu' id='menu-main'>
      <div v-for='menuitem in menuitems' class='menu-section'>
        <h1>{{ menuitem.group }}</h1>
        <ul>
          <li v-for='subitem in menuitem.items'><i v-bind:class='[ subitem.icon, "icon" ]'></i><span>{{ subitem.title }}</span></li>
        </ul>
      </div>
    </div>
</template>

<script>
export default {
  name: 'me-dashboard-main-menu-main',
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