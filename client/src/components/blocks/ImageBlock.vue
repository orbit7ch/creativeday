<template>
  <section>
    <v-img
      :src="item.image.url800x800"
      class="ImageBlock--image">
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

  .ImageBlock--image {
    height: 65vh;
  }

</style>

<script>

  export default {
    props: [
      'item'
    ]
  }
</script>
