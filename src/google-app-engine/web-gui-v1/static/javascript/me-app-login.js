// Document is ready. Let's start with the form
var loginform = new Vue({
    el: '#login',
    data: {
        texts: {
            header: 'Login',
            field_username: 'Username',
            field_username_placeholder: 'Username',
            field_password: 'Password',
            field_password_placeholder: 'Password',
            button_login: 'Log in'
        },
        fields: {
            username: null,
            password: null
        },
        status_waiting: false
    },
    methods: {
        focus: function(field) {
            if (field == 'username') {
                this.$refs.username.focus();
            } else if (field == 'password') {
                this.$refs.password.focus();
            }
        },
        login: function(form) {
            // Make sure the form 'block's the needed fields
            this.status_waiting = true;

            // Do the API-request to authenticate
        }
    }
});

// Do the start methods
loginform.focus('username');