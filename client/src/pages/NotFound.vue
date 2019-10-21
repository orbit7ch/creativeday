<template>
  <div>
    <v-container>
      <v-layout
        column
        align-center
        justify-center
      >
        <h1 class="mb-3">Page Not Found</h1>
        <Logo class="logo-hero"></Logo>

        <v-btn
          class="secondary mt-5"
          dark
          large
          depressed
          :to="'/search'"
          router
          exact
        >
          Start
        </v-btn>

      </v-layout>
    </v-container>
  </div>
</template>

<script>

  import Logo from '../assets/img/logo-dark.svg'

  export default {
    name: 'how-it-works',
    components: {
      Logo
    },
    mounted() {
      this.$setDisplay('v-progress-linear', 'none')
    }
  }
</script>
