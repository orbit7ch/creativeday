<template>
  <v-container class="py-0">
    <section>
      <div v-html="item.value.text"></div>
    </section>
  </v-container>
</template>

<script>
  export default {
    props: [
      'item'
    ]
  }
</script>

