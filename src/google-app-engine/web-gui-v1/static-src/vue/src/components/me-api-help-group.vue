<template>
    <div>
        <me-flexline class='group'>
            <div class='collapse' v-on:click='show_endpoints = !show_endpoints'>
                <i class='plus square outline icon' v-if='!show_endpoints'></i>
                <i class='minus square outline icon' v-if='show_endpoints'></i>
            </div>
            <div class='name'>{{ group.name }}</div>
            <div class='grower description'>{{ group.description }}</div>
        </me-flexline>
        <template v-if='show_endpoints'>
            <me-api-help-endpoint v-bind:endpoint='endpoint' v-bind:key='endpoint.name' v-for='endpoint in group.endpoints'></me-api-help-endpoint>
        </template>
    </div>
</template>

<script>
import me_flexline from '../components/me-flexline';
import me_api_help_endpoint from '../components/me-api-help-endpoint';

export default {
    name: 'me-api-help-group',
    components: {
        'me-flexline': me_flexline,
        'me-api-help-endpoint': me_api_help_endpoint
    },
    props: {
        group: {
            mandatory: true
        }
    },
    data: function() {
        return {
            show_endpoints: false
        };
    }
};
</script>
