<template>
  <div class='ui small modal' v-bind:id='id' ref='modal'>
    <div class='header'>
      {{ title }}
    </div>
    <div v-bind:class='[ { image: type == "image" }, "content" ]'>
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
      'title': { type: String },
      'type': { type: String, default: null }
  },
  methods: {
      show: function() {
        // Local ths
        let vue_this = this;

        // Show the modal
        $(this.$refs.modal).modal({
          centered: true,
          closable: true,
          transition: 'fade',
          duration: 200,
          onHidden: function() {
            vue_this.$emit('hidden');
          }
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