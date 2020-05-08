<template>
  <me-modal id='modal_command_palette' ref='modal' v-bind:content='false' v-bind:centered='false' v-on:hidden='reset'>
    <div class='ui fluid search'>
      <input class='prompt' type='text' placeholder='Enter a command' ref='q' v-model='query'>
      <div class='results'></div>
    </div>
  </me-modal>
</template>

<script>
import Vue from 'vue'
import me_modal from './me-modal'
import me_input from './../components/me-input'
import me_flexline from './../components/me-flexline'
import eventbus from '../eventbus'

export default {
  name: 'me-modal-command-palette',
  components: {
    'me-modal': me_modal
  },
  mounted: function() {
    // Initialize the search-box for Fomantic UI
    $('.ui.search').search({
      source: this.command_list,
      type: 'cmdpalette',
      searchDelay: 0,
      maxResults: 256,
      selectFirstResult: true,
      showNoResults: false,
      searchFields: [ 'title', 'category' ],
      onSelect: this.execute_command,
      minCharacters: 0,
      duration: 0,
      templates: {
        cmdpalette: function(response) {
          // Create a empty string
          let responses = '';

          // Loop through the given responses and create divs form them
          response.results.forEach(function(element) {
            let response_div = '<a class="result"><div class="content"><div class="title"><i class="' + element.icon + ' icon"></i> ' + element.title + '</div><div class="category">' + element.category + '</div></div></a>';

            // Add the new div to the response
            responses += response_div;
          });

          // Return the response
          return responses;
        }
      }
    });
  },
  computed: {
    command_list: function() {
      let return_list = [];

      this.commands.forEach(function(command) {
        if (command.type == 'link') {
          command.title = 'Go to <b>' + command.title + '</b>';
        }
        return_list.push(command);
      });

      return return_list;
    }
  },
  data: function() {
    return {
      query: '',
      commands: [
        {
          icon: 'columns',
          category: 'Pages',
          title: 'Dashboard',
          type: 'link',
          uri: '/dashboard'
        },
        {
          icon: 'list',
          category: 'Pages',
          title: 'Feed',
          type: 'link',
          uri: '/feed'
        },
        {
          icon: 'clipboard outline',
          category: 'Pages',
          title: 'Notes',
          type: 'link',
          uri: '/notes'
        },
        {
          icon: 'music',
          category: 'Pages',
          title: 'Events',
          type: 'link',
          uri: '/events'
        },
        {
          icon: 'guitar',
          category: 'Pages',
          title: 'Making music',
          type: 'link',
          uri: '/making_music'
        },
        {
          icon: 'user circle',
          category: 'Pages',
          title: 'User profile',
          type: 'link',
          uri: '/userprofile'
        },
        {
          icon: 'sign out alternate',
          category: 'User account',
          title: 'Logout',
          type: 'action',
          action: function() { console.log('Command to logout'); }
        },
        {
          icon: 'bars',
          category: 'Layout',
          title: 'Toggle menu',
          type: 'action',
          action: function(vue_instance) {
            vue_instance.$store.commit('set_menu_state', 'toggle');
          }
        },
        {
          icon: 'bars',
          category: 'Layout',
          title: 'Toggle sidebar',
          type: 'action',
          action: function(vue_instance) {
            vue_instance.$store.commit('set_sidebar_state', 'toggle');
          }
        },
        {
          icon: 'edit',
          category: 'Session',
          title: 'Set session title',
          type: 'action',
          action: function(vue_instance) {
            eventbus.$emit('show_modal', 'modal_set_session_title');
          }
        }
      ]
    }
  },
  methods: {
    execute_command: function(command, results) {
      // When a item is chosen, this method gets called and we can perform the needed action

      // Close the modal
      this.$refs.modal.hide();

      // Check the command type and execute it
      if (command.type == 'link') {
        if ('uri' in command) {
          // Navigate to the URI
          this.$router.push(command.uri);
        }
      } else if (command.type == 'action') {
        if ('action' in command) {
          // Run the connected method. We set the first argument to 'this' so the calling
          // method can use the Vue Instance. This way, the method can use the store, for
          // instance
          command.action(this);
        }
      }
    },
    reset: function() {
      // Reset the form
      this.query = '';
      this.$refs.q.value = '';
    }
  }
}
</script>
