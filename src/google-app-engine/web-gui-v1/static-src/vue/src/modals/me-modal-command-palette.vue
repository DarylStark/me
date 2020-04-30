<template>
  <me-modal id='modal_command_palette' v-bind:content='false'>
    <me-input id='fuzzy_search' placeholder='Enter a command' transparent icon='search' icon_position='right' fluid v-model='query' v-on:up='up' v-on:down='down' v-on:change='reset_counter'></me-input>
    <div class='commands'>
      <me-flexline v-for='(command, index) in command_list' v-bind:key='command.title' v-bind:class='[ "command", { "selected": index == active_index } ]'>
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
import Vue from 'vue'
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
      query: '',
      active_index: 0,
      commands: [
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
        },
        {
          icon: 'sign out alternate',
          group: 'User account',
          title: 'Logout2',
          type: 'action',
          action: function() { console.log('c'); }
        },
        {
          icon: 'sign out alternate',
          group: 'User account',
          title: 'Logout3',
          type: 'action',
          action: function() { console.log('c'); }
        },
        {
          icon: 'sign out alternate',
          group: 'User account',
          title: 'Logout4',
          type: 'action',
          action: function() { console.log('c'); }
        },
        {
          icon: 'sign out alternate',
          group: 'User account',
          title: 'Logou5t',
          type: 'action',
          action: function() { console.log('c'); }
        },
        {
          icon: 'sign out alternate',
          group: 'User account',
          title: 'Logout6',
          type: 'action',
          action: function() { console.log('c'); }
        },
        {
          icon: 'sign out alternate',
          group: 'User account',
          title: 'Logout7',
          type: 'action',
          action: function() { console.log('c'); }
        },
        {
          icon: 'sign out alternate',
          group: 'User account',
          title: 'Logout8',
          type: 'action',
          action: function() { console.log('c'); }
        }
      ]
    }
  },
  watch: {
    query: function() {
      // When the query changes, we have to reset the 'active_index'
      this.reset_counter();
    }
  },
  methods: {
    scroll_to_active: function(position) {
      Vue.nextTick(function() {
        let active_top = $('.command.selected').position().top;
        let parent_top = $('.commands').offset().top;
        let element_top = active_top - parent_top;

        console.log('Active top: ' + active_top);
        console.log('Parent top: ' + parent_top);
        console.log('Element top: ' + element_top);

        if (position == 'top') {
          console.log(element_top);
          $('.commands').scrollTop(element_top);
        }
      });
    },
    up: function() {
      // When the user presses the up key, we move the selected element one up
      this.active_index -= 1;

      // Check if we got out of the list
      if (this.active_index < 0) { this.active_index = this.command_list.length - 1; }

      // Scroll to the item
      this.scroll_to_active('top');
    },
    down: function() {
      // When the user presses the down key, we move the selected element one down
      this.active_index += 1;

      // Check if we got out of the list
      if (this.active_index >= this.command_list.length ) { this.active_index = 0; }

      // Scroll to the item
      this.scroll_to_active('bottom');
    },
    reset_counter: function() {
      // Set the counter back to 0
      console.log('resetting');
      this.active_index = 0;
    }
  }
}
</script>