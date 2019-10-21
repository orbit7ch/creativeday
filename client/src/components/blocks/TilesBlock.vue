<template>
  <v-container fluid grid-list-sm class="pa-0">
    <h2 class="mb-2 TilesBlock--heading" v-if="item.value.heading">Styles</h2>
    <v-layout row wrap>
      <v-flex xs6 sm4 v-for="(image, i) in item.images" v-bind:key="i">
        <router-link
          :to="getTo(image)"
          class="router">
          <v-img class="TilesBlock--image" :src="image.image.url400x400"></v-img>
          <div v-if="image.label">
            <h4 class="TilesBlock--label"><v-icon v-if="image.searchText">search</v-icon> {{image.label}}</h4>
          </div>
        </router-link>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    props: [
      'item'
    ],
    methods: {
      getTo(image) {
        if (image.pageUrl) {
          return image.searchText ? image.pageUrl + '?q=' + image.searchText : '/' + image.pageSlug
        }
        return image.searchText ? '/search?q=' + image.searchText : {name: 'service', params: {pk: image.image.pk}}
      }
    }
  }
</script>

<style lang="scss">
  .tiles {
    padding-bottom: 3px;
  }

  .TilesBlock--image {
    height: 200px;
  }

</style>

