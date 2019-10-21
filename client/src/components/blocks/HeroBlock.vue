<template>
  <section>

    <v-img :src="item.backgroundImage.url800x800" class="HeroBlock--image">
      <v-carousel
        hide-controls
        :hide-delimiters="!(item.slides && item.slides.length > 0)"
        :cycle="item.value.slides_interval > 0"
        :interval="item.value.slides_interval" class="HeroBlock--carousel"
        :class="{'HerotextBlock--img-overlay': item.value.use_img_overlay }">
        <v-carousel-item>
          <v-layout
            column
            align-center
            justify-center
            class="white--text pa-2"
          >
            <div class="text-xs-center" v-if="item.value.show_logo">
              <LogoWhite class="logo-hero"></LogoWhite>
            </div>
            <h1 class="mt-4 h3 HerotextBlock--heading text-xs-center">{{item.value.text}}</h1>
            <v-btn
              v-if="item.value.button_text"
              class="secondary mt-4"
              dark
              large
              depressed
              :to="this.item.buttonPageUrl ? this.item.buttonPageUrl : '/search'"
              router
              exact
            >
              {{item.value.button_text}}
            </v-btn>
          </v-layout>
        </v-carousel-item>

        <v-carousel-item
          v-for="(slide,i) in item.slides"
          :key="i"
        >
          <v-layout
            column
            align-center
            justify-center
            class="white--text pa-2"
          >
            <div class="text-xs-center">
              <img height="120" width="120" :src="slide.image.url"/>
            </div>
            <h2 class="h3 mt-2 HerotextBlock--heading text-xs-center" v-if="slide.text">{{slide.text}}</h2>
          </v-layout>

        </v-carousel-item>
      </v-carousel>
    </v-img>

  </section>
</template>

<style lang="scss">
  .v-responsive__content {
    display: flex;
    justify-content: center;
  }

  p {
    margin: 5px 0;
  }

  .HeroBlock--image {
    height: 65vh;
  }

</style>

<script>
  import LogoWhite from '@/assets/img/logo-white.svg'

  export default {
    components: {
      LogoWhite
    },
    props: [
      'item'
    ]
  }
</script>
