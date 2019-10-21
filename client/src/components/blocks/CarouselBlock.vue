<template>
  <v-container fluid grid-list-sm class="pa-0">
    <v-carousel hide-delimiters :cycle="false">
      <v-carousel-item
        v-for="(image,i) in item.images"
        :key="i"
        :src="image.image.url800x800"
      >
      </v-carousel-item>
    </v-carousel>
  </v-container>
</template>

<script>
  export default {
    props: [
      'item'
    ]
  }
</script>

<style lang="scss">
</style>

