<!-- Vue component for the login-form -->
<template>
    <div v-bind:class='[ "me-flexline", { "no_wrap": nowrap } ]'>
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
    }
};
</script>