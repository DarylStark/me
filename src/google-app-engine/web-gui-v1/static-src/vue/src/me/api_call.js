/***************************************************************************************************
 * JavaScript module for a function that can be used to do API requests
 **************************************************************************************************/
import store from '../store';
import axios from 'axios';

export default function(options) {
    // Function to do a API call

    // Create a object with the default values
    let api_options = {
        api_url: null, // The URL of the API
        user_token: null, // The user token for the logged on user
        method: 'GET', // The HTTP method to use for the request
        group: null, // The API group of the request
        endpoint: null, // The API endpoint of the request
        data: null // The data to send
    };

    // Object with API URLs
    let api_urls = {
        production: 'https://me-dstark-nl-test.appspot.com/api/v1',
        development: 'http://127.0.0.1:2610/api/v1'
    };

    // Set the correct API URL
    let environment = store.state.app.environment;
    if (environment in api_urls) {
        api_options.api_url = api_urls[environment];
    } else {
        // If we cannot find the enviroment, we trow an error
        throw 'Cannot find environment "' + environment + '"';
    }

    // Get the user token
    api_options.user_token = store.state.app.user_token;
    if (!api_options.user_token) {
        // If we can't find a API token, trow an error
        throw 'User API Token not found!';
    }

    // Loop through the given object and set the values to the local object
    for (let key of Object.keys(options)) {
        api_options[key] = options[key];
    }

    // Generate the full URL for the request
    let full_url =
        api_options.api_url +
        '/' +
        api_options.group +
        '/' +
        api_options.endpoint;

    // Return a Promise that does the correct code
    return axios({
        method: api_options.method,
        url: full_url,
        data: api_options.data,
        headers: { 'X-ME-Auth-User': api_options.user_token }
    });
}
/**************************************************************************************************/
