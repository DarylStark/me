<template>
    <div class='menu' id='menu-main'>
        <div class='menu-section' v-bind:key='menuitem.dst' v-for='menuitem in $store.state.ui.menus.main'>
            <h1 v-if='menuitem.display_group_title'>{{ menuitem.group }}</h1>
            <ul>
                <router-link tag='li' v-bind:key='subitem.dst' v-bind:to='subitem.dst' v-for='subitem in menuitem.items'>
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
};
</script>
