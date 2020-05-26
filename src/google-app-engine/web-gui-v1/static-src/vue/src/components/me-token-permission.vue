<template>
    <me-flexline>
        <div class='grower description'>
            {{ permission.description }}
            <p>{{ permission.section }}.{{ permission.subject }}</p>
        </div>
        <div>
            <!-- TOOD: Create a seperate component for this and use it in the userprofile as well! -->
            <div class='ui slider checkbox'>
                <input type='checkbox' v-bind:checked='permission.granted' />
                <label></label>
            </div>
            <!-- /TODO -->
        </div>
    </me-flexline>
</template>

<script>
import me_flexline from './me-flexline';

export default {
    name: 'me-token-permission',
    components: {
        'me-flexline': me_flexline
    },
    props: {
        permission: {
            required: true
        }
    }
};
</script>