<!-- Vue component for the a input -->
<template>
  <div class='field' v-bind:class='{ disabled: disabled }'>
    <label v-if='label'>{{ label }}</label>
    <div class='ui' v-bind:class='[ { [icon_position]: icon && icon_position, icon: icon && icon_position }, "input" ]'>
      <input v-bind:type='type' v-bind:id='id' v-model='value' v-bind:placeholder='placeholder' ref='input_field'>
      <i class='icon' v-bind:class='icon' v-if='icon'></i>
    </div>
  </div>
</template>

<!-- The script that gets exported from the file -->
<script>
export default {
  name: 'me-input',
  props: {
    id: { type: String, required: true },
    label: { type: String },
    icon: { type: String },
    icon_position: { type: String, default: 'left' },
    placeholder: { type: String },
    type: { type: String, default: 'text' },
    disabled: { type: Boolean, default: false }
  },
  data: function() {
    return {
      value: null
    };
  },
  methods: {
    focus: function() {
      this.$refs.input_field.focus();
    }
  }
}
</script>