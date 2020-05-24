<template>
    <div>{{ $store.state.app.user_config }}</div>
</template>

<script>
import me_h1 from '../components/me-h1';
import me_grid from '../components/me-grid';
import me_cell from '../components/me-cell';

export default {
    name: 'me-content-feed',
    components: {
        'me-h1': me_h1,
        'me-grid': me_grid,
        'me-cell': me_cell
    }
};
</script>
