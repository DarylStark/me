<!-- Vue component for the a h1 -->
<template>
    <div class='me-splashscreen'>
        <h1>Loading</h1>
        <p>{{ $store.state.app.loading_text }}</p>
        <div class='ui tiny indeterminate progress' id='progressbar'>
            <div class='bar'>
                <div class='progress'></div>
            </div>
        </div>
    </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
    name: 'me-splashscreen',
    mounted: function() {
        $('#progressbar').progress();
    }
};
</script>