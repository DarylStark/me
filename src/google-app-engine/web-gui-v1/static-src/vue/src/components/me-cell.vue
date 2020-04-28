<!-- Vue component for the login-form -->
<template>
  <div v-bind:class='[ "cell", { "span-2": span == 2 }, { "span-3": span == 3 }, { "span-4": span == 4 }, { "span-5": span == 5 }, { "span-6": span == 6 }, { "span-7": span == 7 }, { "span-8": span == 8 }, { "span-9": span == 9 }, { "span-10": span == 10 }, { "span-11": span == 11 }, { "span-12": span == 12 }, { center: center } ]'>
    <div v-bind:class='{ padding: padding }'>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'me-cell',
  props: {
    padding: { type: Boolean, default: false },
    center: { type: Boolean, default: false },
    span: { type: Number, default: 0 }
  }
}
</script>