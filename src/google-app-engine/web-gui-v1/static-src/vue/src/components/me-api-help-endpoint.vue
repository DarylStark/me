<template>
    <div>
        <me-flexline class='endpoint' v-on:click='show_methods = !show_methods'>
            <div class='collapse'>
                <i class='plus square outline icon' v-if='!show_methods'></i>
                <i class='minus square outline icon' v-if='show_methods'></i>
            </div>
            <div class='name grower'>{{ endpoint.name }}</div>
            <div class='grower description'>{{ endpoint.description }}</div>
        </me-flexline>
        <template v-if='show_methods'>
            <me-flexline class='method' v-bind:key='method.method' v-bind:nowrap='$store.state.ui.media_type == "desktop"' v-for='method in methods'>
                <div class='collapse'></div>
                <div class='name grower'>{{ method.method }}</div>
                <div class='grower description'>
                    <p class='title'>Requied permission:</p>
                    <p>
                        <span>{{ method.permission }}</span>
                        <span v-if='endpoint.user_token_needed'>(user)</span>
                        <span v-if='!endpoint.user_token_needed'>(client)</span>
                    </p>
                    <template v-if='method.documentation.description'>
                        <p class='title'>Description:</p>
                        <p>{{ method.documentation.description }}</p>
                    </template>
                    <template v-if='method.documentation.data'>
                        <p class='title'>Description:</p>
                        <p>{{ method.documentation.data }}</p>
                    </template>
                    <template v-if='method.documentation.return'>
                        <p class='title'>Description:</p>
                        <p>{{ method.documentation.return }}</p>
                    </template>
                </div>
            </me-flexline>
        </template>
    </div>
</template>

<script>
import me_flexline from '../components/me-flexline';

export default {
    name: 'me-api-help-group',
    components: {
        'me-flexline': me_flexline
    },
    props: {
        endpoint: {
            mandatory: true
        }
    },
    data: function() {
        return {
            show_methods: false
        };
    },
    computed: {
        methods: function() {
            // To get the methods for this API, we have to get the methods from the permissions and
            // add the documentation to it
            let methods = new Array();
            let methods_permissions = Object.keys(this.endpoint.permissions);

            // Local this
            let vue_this = this;

            methods_permissions.forEach(function(method) {
                // Create a empty object
                let method_object = {
                    method: method,
                    permission: vue_this.endpoint.permissions[method],
                    documentation: null
                };

                // Check if there is a documentation available
                if (vue_this.endpoint.documentation) {
                    if (method in vue_this.endpoint.documentation) {
                        method_object.documentation =
                            vue_this.endpoint.documentation[method];
                    }
                }

                // Add it to the returning array
                methods.push(method_object);
            });

            return methods;
        }
    }
};
</script>
