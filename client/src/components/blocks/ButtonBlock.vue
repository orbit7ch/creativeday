<template>
  <div class="text-xs-center">
    <v-btn
      class="secondary"
      dark
      large
      depressed
      :to="getTo()"
      router
      exact
    > {{item.value.text}}
    </v-btn>
  </div>
</template>

<script>
  export default {
    props: [
      'item'
    ],
    methods: {
      getTo() {
        var url = this.item.pageUrl
        if (!url) {
          url = 'search'
        }
        return this.item.value.search_text ? url + '?q=' + this.item.value.search_text : url
      }
    }
  }
</script>
