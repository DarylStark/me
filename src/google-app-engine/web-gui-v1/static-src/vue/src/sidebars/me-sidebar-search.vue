<!-- Vue component for the login-form -->
<template>
    <div id='me-sidebar-search'>
        <h1>Search preferences</h1>
        <div class='ui fluid selection dropdown'>
            <i class='dropdown icon'></i>
            <div class='menu'>
                <div class='item'>Searchprofile 1</div>
                <div class='item'>Searchprofile 2</div>
                <div class='item'>Searchprofile 3</div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'me-sidebar-search',
    mounted: function() {
        // Create the dropdown
        $('.ui.dropdown').dropdown({
            action: 'activate',
            clearable: true
        });
    }
};
</script>