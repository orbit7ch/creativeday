<template>
  <div>
    <v-container grid-list-sm class="px-0">
      <div v-for="(company, index) in companies" :key="index">
        <router-link :to="company.url" class="router">
          <v-layout row wrap class="mb-3">
            <v-flex xs2>
              <v-avatar size=100 class="mt-2 v-avatar--responsive">
                <v-img
                  :src="company.mainPortrait.url200x200"
                  alt="Avatar"
                ></v-img>
              </v-avatar>
            </v-flex>

            <v-flex xs10 class="pl-2">
              <h3 class="text--link  text text--left">{{company.name}}</h3>
              <div class="mb-1 mt-1  text text--left">{{company.bio}}</div>
              <swiper :options="swiperOption">
                <swiper-slide v-for="(operator, i) in company.operators" :key="i">
                  <v-img
                    :src="operator.mainPortrait.url200x200"
                    alt="operators"
                    aspect-ratio="1"
                  ></v-img>
                </swiper-slide>
              </swiper>
            </v-flex>
          </v-layout>
        </router-link>
      </div>
    </v-container>
  </div>
</template>

<script>
  import {swiper, swiperSlide} from 'vue-awesome-swiper'

  export default {
    name: 'company-list',
    props: ['companies'],
    components: {
      swiper,
      swiperSlide
    },
    data() {
      return {
        swiperOption: {
          slidesPerView: 5,
          spaceBetween: 1
        }
      }
    }
  }
</script>
