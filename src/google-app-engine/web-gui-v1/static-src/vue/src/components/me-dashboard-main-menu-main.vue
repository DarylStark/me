<template>
    <div class='menu' id='menu-main'>
      <div v-for='menuitem in menuitems' class='menu-section'>
        <h1>{{ menuitem.group }}</h1>
        <ul>
          <li v-for='subitem in menuitem.items'>
            <!-- TODO: make sure the complete LI is clickable -->
            <router-link v-bind:to='subitem.dst'>
              <i v-bind:class='[ subitem.icon, "icon" ]'></i>
              <span>{{ subitem.title }}</span>
            </router-link>
          </li>
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
          items: [
            { title: 'Dashboard', icon: 'columns', dst: '/home' },
            { title: 'Feed', icon: 'list', dst: '/feed' },
            { title: 'Notebook', icon: 'clipboard outline', dst: '/notes' }
          ]
        },
        {
          group: 'Music',
          items: [
            { title: 'Events', icon: 'music', dst: '/home' },
            { title: 'Making music', icon: 'guitar', dst: '/home' }
          ]
        }
      ]
    }
  }
}
</script>
