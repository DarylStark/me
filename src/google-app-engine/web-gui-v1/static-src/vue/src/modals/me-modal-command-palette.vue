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
      // Create a empty return list
      let return_list = [];

      // Create a empty list for the items
      let commands = new Array();

      // Get the items from the main menu
      this.$store.state.ui.menus.main.forEach(function(menu) {
        menu.items.forEach(function(menu_item) {
          // Create a new item
          let new_item = {
            title: menu_item.title,
            category: 'Main menu',
            icon: menu_item.icon,
            type: 'link',
            uri: menu_item.dst
          }

          // Add the item to the commands
          commands.push(new_item);
        });
      });

      // Get the actions from the store
      this.$store.state.ui.actions.forEach(function(action) {
        // Create a new item
          let new_item = {
            title: action.title,
            category: 'Global action',
            icon: action.icon,
            type: action.type,
            uri: action.dst,
            action: action.action
          }

          // Add the item to the commands
          commands.push(new_item);
      });

      // Return the list
      return commands.sort(function(item_a, item_b) {
        if (item_a.title > item_b.title) { 
          return 1;
        }
        if (item_a.title < item_b.title) { 
          return -1;
        }
        return 0;
      });
    }
  },
  data: function() {
    return {
      query: ''
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
