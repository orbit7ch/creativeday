<template>
  <v-container fluid grid-list-sm class="pa-0" style="min-height: 100vh">
    <v-layout row wrap>
      <v-flex xs4 md3 v-for="(item, index) in images" v-bind:key="index">
        <v-img
          :src="item.url400x400"
          class="TilesBlock--image pointer"
          @click="click(item, index)"
        ></v-img>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    props: ['images'],

    methods: {
      click(img, index) {
        if (this.$listeners && this.$listeners.click) {
          this.$emit('click', img, index)
        } else {
          this.$router.push({name: 'service', params: {pk: img.pk}})
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
</style>
