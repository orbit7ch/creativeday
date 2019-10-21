<template>
  <v-container fluid grid-list-sm class="pa-0">
    <swiper :options="swiperOption">
      <swiper-slide v-for="(image, i) in item.images" :key="i">

        <router-link
          :to="image.searchText ?  '/search?q='+image.searchText : { name: 'service', params: {pk: image.image.pk}}"
          class="router">
          <v-img :src="image.image.url400x400" alt="image" aspect-ratio="1">
            <div v-if="image.label" class="text-overlay"></div>
          </v-img>
          <h4 v-if="image.label">{{image.label}}</h4>
        </router-link>

      </swiper-slide>
    </swiper>
  </v-container>
</template>

<script>
  export default {
    props: [
      'item'
    ],
    data() {
      return {
        swiperOption: {
          slidesPerView: 3,
          spaceBetween: 2
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
</style>

