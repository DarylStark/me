/***************************************************************************************************
 * JavaScript module for different functions that can be ran globablly
 **************************************************************************************************/
import store from '../store';
import me_api_call from './api_call';

export function refresh_user_token(options) {
    // Method to refresh the user token

    // Send the API request to refresh the user token
    me_api_call({
        group: 'aaa',
        endpoint: 'refresh_user_token',
        method: 'PATCH'
    })
        .then(function(data) {
            store.commit('set_user_token', data['data']['object']);
            if ('success' in options) {
                options.success();
            }
        })
        .catch(function(data) {
            if ('failed' in options) {
                options.failed();
            }
        });
}
