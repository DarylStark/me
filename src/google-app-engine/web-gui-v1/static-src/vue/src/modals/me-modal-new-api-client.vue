<template>
    <me-modal id='modal_new_api_client' ref='modal' v-bind:title='title' v-on:hidden='reset' v-on:showing='showing'>
        <form class='ui form'>
            <me-input :disabled='saving' :error='name_error' icon='lock' id='name' label='Application name' type='text' v-model='fields.name' v-on:enter='submit'></me-input>
            <me-input :disabled='saving' :error='version_error' icon='lock' id='version' label='Application version' type='text' v-model='fields.version' v-on:enter='submit'></me-input>
            <me-input :disabled='saving' :error='publisher_error' icon='lock' id='publisher' label='Publisher' type='text' v-model='fields.publisher' v-on:enter='submit'></me-input>
        </form>
        <template v-slot:actions>
            <me-button :disabled='saving' v-on:click='close'>Cancel</me-button>
            <me-button :disabled='saving' :loading='saving' label_icon='desktop' label_position='right' primary v-on:click='submit'>{{ button_text }}</me-button>
        </template>
    </me-modal>
</template>

<script>
import me_modal from './me-modal';
import me_input from './../components/me-input';
import me_button from './../components/me-button';
import me_api_call from '../me/api_call';
import eventbus from '../eventbus';

export default {
    name: 'me-modal-new-api-client',
    data: function() {
        return {
            mode: 'new',
            saving: false,
            name_error: false,
            version_error: false,
            publisher_error: false,
            fields: {
                id: null,
                name: null,
                version: null,
                publisher: null
            }
        };
    },
    computed: {
        title: function() {
            // The title is dependant on the mode of the modal
            if (this.mode == 'new') {
                return 'New API client';
            }
            return 'Edit API client';
        },
        button_text: function() {
            // The 'save' button-text is dependant on the mode of the modal
            if (this.mode == 'new') {
                return 'Add client';
            }
            return 'Save';
        }
    },
    components: {
        'me-modal': me_modal,
        'me-input': me_input,
        'me-button': me_button
    },
    methods: {
        showing: function() {
            // Check if this modal was shown using a object. If it was, we have to edit a token
            // instead of creating one
            if (this.$refs.modal.event === Object(this.$refs.modal.event)) {
                this.mode = 'edit';

                // Set the fields
                this.fields.id = this.$refs.modal.event.client.id;
                this.fields.name = this.$refs.modal.event.client.app_name;
                this.fields.version = this.$refs.modal.event.client.app_version;
                this.fields.publisher = this.$refs.modal.event.client.app_publisher;
            } else {
                this.mode = 'new';
            }
        },
        close: function() {
            this.$refs.modal.hide();
        },
        reset: function() {
            this.saving = false;

            this.fields.name = null;
            this.fields.version = null;
            this.fields.publisher = null;
            this.name_error = false;
            this.version_error = false;
            this.publisher_error = false;
        },
        is_valid: function() {
            // Returns true if the form is valid, false if the from is invalid
            let errors = 0;

            // Reset all errors
            this.name_error = false;
            this.version_error = false;
            this.publisher_error = false;

            // Verify all fields
            if (this.fields.name == '' || this.fields.name == null) {
                errors++;
                this.name_error = true;
            }

            if (this.fields.version == '' || this.fields.version == null) {
                errors++;
                this.version_error = true;
            }

            if (this.fields.publisher == '' || this.fields.publisher == null) {
                errors++;
                this.publisher_error = true;
            }

            if (errors > 0) {
                return false;
            }
            return true;
        },
        submit: function() {
            // Add the new client
            this.saving = true;

            // Local this
            let vue_this = this;

            if (this.is_valid()) {
                if (this.mode == 'new') {
                    this.$store.commit('add_api_client', {
                        success: function() {
                            vue_this.close();
                            $('body').toast({
                                position: 'bottom center',
                                message: 'Added client',
                                closeIcon: true,
                                displayTime: 'auto',
                                showIcon: 'user',
                                class: 'success'
                            });
                        },
                        failed: function(error) {
                            vue_this.saving = false;

                            if (error == 'duplicate') {
                                $('body').toast({
                                    position: 'bottom center',
                                    message:
                                        'There is already a API client with that name',
                                    closeIcon: true,
                                    displayTime: 'auto',
                                    showIcon: 'user',
                                    class: 'error'
                                });
                            } else {
                                $('body').toast({
                                    position: 'bottom center',
                                    message: "Couldn't add client",
                                    closeIcon: true,
                                    displayTime: 'auto',
                                    showIcon: 'user',
                                    class: 'error'
                                });
                            }
                        },
                        fields: this.fields
                    });
                } else {
                    this.$store.commit('api_update_api_client_token', {
                        success: function() {
                            vue_this.close();
                            $('body').toast({
                                position: 'bottom center',
                                message: 'Changed client',
                                closeIcon: true,
                                displayTime: 'auto',
                                showIcon: 'user',
                                class: 'success'
                            });
                        },
                        failed: function(error) {
                            vue_this.saving = false;

                            $('body').toast({
                                position: 'bottom center',
                                message:
                                    'Something went wrong while changing API client: ' +
                                    error,
                                closeIcon: true,
                                displayTime: 'auto',
                                showIcon: 'user',
                                class: 'error'
                            });
                        },
                        fields: this.fields
                    });
                }
            } else {
                this.saving = false;
            }
        }
    }
};
</script>