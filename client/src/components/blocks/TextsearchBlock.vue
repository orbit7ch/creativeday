<template>
  <section class="text-xs-left" id="search-top">
    <v-container fluid grid-list-sm class="pb-0 pt-4">
      <v-text-field v-model="searchInput"
                    hide-details
                    label="Search Services"
                    class="search-field"
                    placeholder=""
                    solo
                    :append-icon="'search'"
                    @click:append="textSearch(searchInput)"
                    @keyup.enter="textSearch(searchInput)"
      ></v-text-field>
    </v-container>

  </section>
</template>

<script>
  export default {
    props: [
      'item'
    ],
    data() {
      return {
        searchInput: ''
      }
    },

    methods: {
      textSearch(text) {
        this.$gtm.trackEvent({
          event: 'ev-textSearch',
          category: 'Search',
          action: 'Text Search',
          label: text,
          value: 0
        })
        this.$router.push({path: this.item.pageUrl, query: {q: text}})
      }
    }
  }
</script>
