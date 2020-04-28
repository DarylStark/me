<template>
  <me-modal id='modal_command_palette' v-bind:content='false'>
    <me-input id='fuzzy_search' placeholder='Enter a command' transparent icon='search' icon_position='right' fluid v-model='query'></me-input>
    <div class='commands'>
      <me-flexline v-for='command in command_list' v-bind:key='command.title' extra_class='command'>
        <div>
          <i v-bind:class='[ command.icon, "icon" ]' v-if='command.icon'></i>
          <b>{{ command.group }}</b>: {{ command.title }}
        </div>
        <div class='spacer'></div>
        <div>{{ command.type }}</div>
      </me-flexline>
    </div>
  </me-modal>
</template>

<script>
import me_modal from './me-modal'
import me_input from './../components/me-input'
import me_flexline from './../components/me-flexline'

export default {
  name: 'me-modal-command-palette',
  components: {
    'me-modal': me_modal,
    'me-input': me_input,
    'me-flexline': me_flexline
  },
  computed: {
    command_list: function() {
      // Local this
      var vue_this = this;

      // Return the filtered list
      return this.commands.filter(function(command) { 
        if (vue_this.query == null || vue_this.query == '') { return true; }
        return command.title.toLowerCase().includes(vue_this.query.toLowerCase()) || command.group.toLowerCase().includes(vue_this.query.toLowerCase());
      });
    }
  },
  data: function() {
    return {
      'query': '',
      'commands': [
        {
          icon: 'columns',
          group: 'Pages',
          title: 'Dashboard',
          type: 'link',
          action: function() { console.log('c'); }
        },
        {
          icon: 'list',
          group: 'Pages',
          title: 'Feed',
          type: 'link',
          action: function() { console.log('c'); }
        },
        {
          icon: 'clipboard outline',
          group: 'Pages',
          title: 'Notebook',
          type: 'link',
          action: function() { console.log('c'); }
        },
        {
          icon: 'music',
          group: 'Pages',
          title: 'Events',
          type: 'link',
          action: function() { console.log('c'); }
        },
        {
          icon: 'guitar',
          group: 'Pages',
          title: 'Making music',
          type: 'link',
          action: function() { console.log('c'); }
        },
        {
          icon: 'user circle',
          group: 'Pages',
          title: 'User profile',
          type: 'link',
          action: function() { console.log('c'); }
        },
        {
          icon: 'sign out alternate',
          group: 'User account',
          title: 'Logout',
          type: 'action',
          action: function() { console.log('c'); }
        }
      ]
    }
  }
}
</script>