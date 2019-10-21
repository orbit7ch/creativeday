<template>
  <section class="text-xs-center py-5 LogoBlock--section" v-bind:class="{ primary: item.value.style =='dark' }">
    <LogoWhite v-if="item.value.style =='dark'" class="logo-hero"/>
    <LogoDark v-else class="logo-hero"/>
    <div v-html="item.value.text"></div>
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

  .LogoBlock--section.primary {
    color: #ffffff;
  }

</style>

<script>
  import LogoWhite from '@/assets/img/logo-white.svg'
  import LogoDark from '@/assets/img/logo-dark.svg'

  export default {
    props: [
      'item'
    ],
    components: {
      LogoDark,
      LogoWhite
    }
  }
</script>
