<template>
    <div class='menu' id='menu-main'>
      <div v-for='menuitem in $store.state.ui.menus.main' class='menu-section' v-bind:key='menuitem.dst'>
        <h1 v-if='menuitem.display_group_title'>{{ menuitem.group }}</h1>
        <ul>
          <router-link v-bind:to='subitem.dst' v-for='subitem in menuitem.items' tag='li' v-bind:key='subitem.dst'>            
            <i v-bind:class='[ subitem.icon, "icon" ]'></i>
            <span>{{ subitem.title }}</span>
          </router-link>
        </ul>
      </div>
    </div>
</template>

<script>
export default {
  name: 'me-dashboard-main-menu-main'
}
</script>
