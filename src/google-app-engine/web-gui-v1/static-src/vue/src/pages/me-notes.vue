<template>
    <div id='me-content-notes'>
        <me-h1>Notes</me-h1>
        {{ changed }}
        <button v-on:click='toggle'>Change</button>
    </div>
</template>

<script>
import me_h1 from '../components/me-h1';

export default {
    name: 'me-content-notes',
    data: function() {
        return {
            changed: false
        };
    },
    components: {
        'me-h1': me_h1
    },
    methods: {
        toggle: function() {
            this.changed = !this.changed;
        }
    },
    created: function() {
        // We do need a sidebar on this page. Enable it.
        this.$store.commit('set_sidebar_availability', true);
    },
    beforeRouteLeave: function(to, from, next) {
        next(!this.changed);
    }
};
</script>
