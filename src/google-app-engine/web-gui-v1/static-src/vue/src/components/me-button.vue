<template>
  <button v-bind:class='[ "ui", { primary: primary}, { disabled: disabled }, { loading: loading }, { right: label_icon && label_position == "right" }, { labeled: label_icon }, { icon: label_icon || icon }, "button" ]' v-on:click='$emit("click");'>
    <i v-bind:class='[ label_icon, icon, "icon" ]' v-if='label_icon != null || icon != null'></i>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'me-button',
  props: {
      primary: { type: Boolean, default: false },
      disabled: { type: Boolean, default: false },
      loading: { type: Boolean, default: false },
      label_icon: { type: String, default: null },
      label_position: { type: String, default: "left" },
      icon: { type: String, default: null }
  }
}
</script>
