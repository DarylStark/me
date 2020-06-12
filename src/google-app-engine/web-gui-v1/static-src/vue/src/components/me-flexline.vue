<!-- Vue component for the login-form -->
<template>
    <div v-bind:class='[ "me-flexline", { "no_wrap": nowrap } ]' v-on:click='click'>
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'me-flexline',
    props: {
        nowrap: {
            type: Boolean,
            default: false
        }
    },
    methods: {
        click: function() {
            this.$emit('click');
        }
    }
};
</script>