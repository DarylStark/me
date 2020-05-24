<template>
    <div class='me-page-title'>
        <me-flexline>
            <div class='title'>
                <i v-bind:class='[ { icon: icon }, icon ]' v-if='icon'></i>
                <slot></slot>
            </div>
            <div class='spacer'></div>
            <div class='actions'>
                <slot name='actions'></slot>
            </div>
        </me-flexline>
    </div>
</template>

<script>
import me_flexline from './me-flexline';

export default {
    name: 'me-page-title',
    components: {
        'me-flexline': me_flexline
    },
    props: {
        icon: { type: String, default: false }
    }
};
</script>
