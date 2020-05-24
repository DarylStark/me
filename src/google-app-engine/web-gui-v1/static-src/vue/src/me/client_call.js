/***************************************************************************************************
 * JavaScript module for a function that can be used to do client requests
 **************************************************************************************************/
import store from '../store';
import axios from 'axios';

export default function(options) {
    // Function to do a API call

    // Create a object with the default values
    let api_options = {
        environment: null, // The environment to use
        api_url: null, // The URL of the client
        method: 'GET', // The HTTP method to use for the request
        endpoint: null, // The endpoint of the request
        data: null // The data to send
    };

    // Loop through the given object and set the values to the local object
    for (let key of Object.keys(options)) {
        api_options[key] = options[key];
    }

    // Object with API URLs
    let api_urls = {
        production: 'https://me-dstark-nl-test.appspot.com/ui/client',
        development: 'http://127.0.0.1:2610/ui/client'
    };

    // Set the correct API URL
    let environment = api_options.environment;
    if (environment == null) {
        environment = store.state.app.environment;
    }
    if (environment in api_urls) {
        api_options.api_url = api_urls[environment];
    } else {
        // If we cannot find the environment, we trow an error
        throw 'Cannot find environment "' + environment + '"';
    }

    // Generate the full URL for the request
    let full_url = api_options.api_url + '/' + api_options.endpoint;

    if (environment == 'development') {
        if (store.state.app.user_token) {
            full_url += '?user_token=' + store.state.app.user_token;
        }
    }

    // Return a Promise that does the correct code
    return axios({
        method: api_options.method,
        url: full_url,
        data: api_options.data
    });
}
/**************************************************************************************************/
