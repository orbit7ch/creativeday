<template>
  <div>
    <v-container grid-list-sm class="py-0">
      <div v-for="(operator, index) in operators" :key="index" @click="click(operator, index)" class="pointer">

        <v-layout row wrap class="mb-4">
          <v-flex xs2>
            <v-avatar size=100 class="v-avatar--responsive">
              <v-img
                :src="operator.mainPortrait.url200x200"
                alt="Avatar"
              ></v-img>
            </v-avatar>
          </v-flex>

          <v-flex xs10 class="pl-2">
            <h3 class="h4 text--link text text--left"><span>{{operator.fullName}}</span></h3>
            <div class="mb-1 text text--left">{{operator.shortBio}}</div>
            <div class="text--tags mb-1" v-html="operator.tags"></div>
            <swiper :options="swiperOption">
              <swiper-slide v-for="(image, i) in operator.portfolio" :key="i">
                <v-img
                  :src="image.image.url200x200"
                  alt="portfolio"
                  aspect-ratio="1"
                ></v-img>
              </swiper-slide>
            </swiper>
          </v-flex>

        </v-layout>

      </div>
    </v-container>
  </div>
</template>

<script>
  import {swiper, swiperSlide} from 'vue-awesome-swiper'

  export default {
    props: ['operators', 'listName'],
    components: {
      swiper,
      swiperSlide
    },
    data() {
      return {
        swiperOption: {
          slidesPerView: 3,
          spaceBetween: 2
        }
      }
    },

    watch: {
      operators:
        {
          // the callback will be called immediately after the start of the observation
          immediate: true,
          handler(val, oldVal) {
            if (this.operators) {
              this.$gtm.trackEvent({
                event: 'ec-productImpression',
                category: 'Ecommerce',
                action: 'Product Impressions',
                ecommerce: {
                  impressions: this.operators.map((operator, index) => {
                      return {
                        name: operator.fullName,
                        id: operator.id,
                        price: '1',
                        category: 'Operator',
                        list: (this.listName ? this.listName : 'OperatorsList'),
                        position: index + 1
                      }
                    }
                  )
                }
              })
            }
          }
        }
    },

    methods: {
      click(operator, index) {
        this.$gtm.trackEvent({
          event: 'ec-productClick',
          category: 'Ecommerce',
          action: 'Product Click',
          ecommerce: {
            click: {
              actionField: {list: (this.listName ? this.listName : 'OperatorsList')},
              products: [{
                name: operator.fullName,
                id: operator.id,
                price: '1',
                category: 'Operator',
                position: index + 1
              }]
            }
          }
        })

        this.$router.push(operator.url)
      }
    }
  }
</script>
