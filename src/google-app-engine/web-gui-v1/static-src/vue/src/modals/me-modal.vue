<template>
  <div class='ui small modal' v-bind:id='id' ref='modal'>
    <div class='header'>
      {{ title }}
    </div>
    <div class='content'>
      <slot></slot>
    </div>
    <div class='actions'>
      <slot name='actions'></slot>
    </div>
  </div>
</template>

<script>
import eventbus from '../eventbus'

export default {
  name: 'me-modal',
  props: {
      'id': { type: String, mandatory: true },
      'title': { type: String }
  },
  methods: {
      show: function() {
        $(this.$refs.modal).modal({
          centered: true,
          closable: true,
          transition: 'fade',
          duration: 200
        }).modal('show');
      },
      hide: function() {
          $(this.$refs.modal).modal('hide');
      }
  },
  mounted() {
      // Local this
      let vue_this = this;

      // Listen for 'show_dialog' events
      eventbus.$on('show_modal', function(modal_id) {
        if (vue_this.id == modal_id) {
          vue_this.show();
        }
      });
  }
}
</script>