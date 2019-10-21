<template>
  <section>
    <v-img
      class="HerotextBlock--image"
      :src="item.backgroundImage.url800x800">
      <v-layout
        column
        align-center
        justify-center
        class="white--text pa-2"
        :class="{'HerotextBlock--img-overlay': item.value.use_img_overlay }"
      >
        <div class="h2 text-xs-center HerotextBlock--text" v-html="item.value.text"></div>
        <v-btn
          v-if="item.value.button_text"
          class="secondary mt-5"
          dark
          large
          depressed
          :to=" '/search'"
          router
          exact
        >
          {{item.value.button_text}}
        </v-btn>
      </v-layout>
    </v-img>
  </section>
</template>

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
