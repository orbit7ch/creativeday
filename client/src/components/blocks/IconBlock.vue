<template>
  <section class="text-xs-center">
    <v-img
      :src="item.document.url"
      class="margin--auto"
      width="60"
      height="60">
    </v-img>
  </section>
</template>

<script>
  export default {
    props: [
      'item'
    ]
  }
</script>
