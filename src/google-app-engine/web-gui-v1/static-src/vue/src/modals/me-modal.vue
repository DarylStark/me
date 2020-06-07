<template>
    <div class='ui small modal' ref='modal' v-bind:id='id'>
        <div class='header' v-if='title'>{{ title }}</div>
        <div v-bind:class='[ { image: type == "image" }, { content: content } ]'>
            <slot></slot>
        </div>
        <div class='actions' v-if='show_actions'>
            <slot name='actions'></slot>
        </div>
    </div>
</template>

<script>
import eventbus from '../eventbus';

export default {
    name: 'me-modal',
    props: {
        id: { type: String, mandatory: true },
        title: { type: String, default: null },
        type: { type: String, default: null },
        content: { type: Boolean, default: true },
        centered: { type: Boolean, default: true }
    },
    data: function() {
        return {
            event: null
        };
    },
    computed: {
        show_actions: function() {
            // Return 'true' if action slot is set
            return 'actions' in this.$slots;
        }
    },
    methods: {
        show: function() {
            // Local ths
            let vue_this = this;

            // Show the modal
            $(this.$refs.modal)
                .modal({
                    centered: vue_this.centered,
                    closable: true,
                    transition: 'fade',
                    duration: 200,
                    onHidden: function() {
                        vue_this.$emit('hidden');
                    },
                    onShow: function() {
                        vue_this.$emit('showing');
                    }
                })
                .modal('show');
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
            let show_modal_id = modal_id;
            vue_this.event = modal_id;

            // Check if we got an object
            if (modal_id === Object(modal_id)) {
                show_modal_id = modal_id.id;
            }

            // Show the modal
            if (vue_this.id == show_modal_id) {
                vue_this.show();
            }
        });
    }
};
</script>
