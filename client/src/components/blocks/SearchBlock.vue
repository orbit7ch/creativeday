<template>
  <section class="text-xs-left" id="search-top">
    <v-container fluid grid-list-sm class="pb-0 pt-4">
      <v-layout row wrap>
        <v-flex xs12 mb-3 v-if="item.value.show_text_search">
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
        </v-flex>

        <v-flex xs12 class="mb-3" v-if="item.value.tags && item.value.tags.length">
          <v-chip class="search-chip" color="white" text-color="primary" v-for="(tag, i) in item.value.tags" :key="i"
                  @click="tagClick(tag)">
            {{tag}}
            <v-icon right>search</v-icon>
          </v-chip>
        </v-flex>

        <h2 v-if="item.filters && item.filters.length" class="mb-2 styles-heading">Styles</h2>

        <v-flex xs12 class="mb-3" v-if="item.filters && item.filters.length">
          <swiper :options="swiperOption">
            <swiper-slide v-for="(filter, i) in item.filters" :key="i">
              <div class="style-card pointer"
                   @click="styleClick(filter.text)">
                <v-img
                  :src="filter.image.url200x200"
                  alt="mage"
                  aspect-ratio="1"
                  height="120px"
                >
                  <div class="text-overlay"></div>
                </v-img>
                <h4 v-if="filter.text">{{filter.text}}</h4>
              </div>
            </swiper-slide>
            <div class="swiper-button-prev" slot="button-prev">
              <v-btn fab small icon color="white">
                <v-icon>keyboard_arrow_left</v-icon>
              </v-btn>
            </div>
            <div class="swiper-button-next" slot="button-next">
              <v-btn fab small icon color="white">
                <v-icon>keyboard_arrow_right</v-icon>
              </v-btn>
            </div>
          </swiper>
        </v-flex>

        <v-flex xs12 d-flex>
          <h2 class="mb-2 mt-2 search-term text-xs-left" id="searchTerm"><span v-if="!searchText">Trending</span>{{searchText}}
          </h2>
          <v-menu transition="slide-y-transition" class="parts-menu">
            <v-btn slot="activator" flat right>
              {{bodyPart}}
              <v-icon right dark>keyboard_arrow_down</v-icon>
            </v-btn>
            <v-list>
              <v-list-tile v-for="(item, i) in parts" :key="i" @click="bodyPartClick(item)">
                <v-list-tile-title>{{ item }}</v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-flex>
      </v-layout>
    </v-container>

    <div v-if="noResults">
      <v-container fluid grid-list-sm class="py-2">
        <v-layout row wrap>
          <div class="h5">
            Leider haben wir zu "{{searchText}}" nichts gefunden.
            <span v-if="suggest" @click="suggestionsClick(suggest)" class="pointer secondary--text underline">Probiers mit "{{suggest}}".</span>
          </div>


          <div class="mt-4 text-xs-center" style="width: 100%">
            <v-btn class="secondary" dark large depressed router exact @click="chatAdvice">
              Kostenlose Chat Beratung
            </v-btn>
          </div>

        </v-layout>
      </v-container>
    </div>

    <div style="min-height: 80vh">
      <ServicesList :images="services"></ServicesList>
      <InfiniteLoading
        v-if="watchScrolling && item.value.use_endless_scrolling"
        @infinite="fetchImages"
        :distance="distance"
        spinner="spiral"
        ref="infiniteLoading">
        <span slot="no-results"></span><span slot="no-more"></span>
      </InfiniteLoading>
    </div>

  </section>
</template>

<script>
  import STORE_SEARCH_TERM from '@/graphql/gql/storeUserSearchTerm.gql'
  import SEARCH_QUERY from '@/graphql/gql/search.gql'
  import SUGGEST_QUERY from '@/graphql/gql/suggest.gql'
  import {swiper, swiperSlide} from 'vue-awesome-swiper'
  import ServicesList from '@/components/ServicesList'
  import InfiniteLoading from 'vue-infinite-loading'
  import store from '@/store/core'

  export default {
    props: [
      'item'
    ],
    components: {
      swiper,
      swiperSlide,
      ServicesList,
      InfiniteLoading
    },
    data() {
      return {
        noResults: false,
        searchText: (this.$route.query.q ? this.$route.query.q : (this.item.value.initial_search ? this.item.value.initial_search : '')),
        searchInput: (this.$route.query.q ? this.$route.query.q : (this.item.value.initial_search ? this.item.value.initial_search : '')),
        suggest: '',
        bodyPart: 'Alle',
        swiperOption: {
          slidesPerView: 3,
          spaceBetween: 4,
          navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
          }
        },
        parts: this.$getFilter(),

        watchScrolling: false,
        start: 0,
        size: 30,
        distance: 500,
        services: []
      }
    },

    apollo: {
      serviceSearch() {
        return {
          query: SEARCH_QUERY,
          variables: {searchText: this.searchText, start: this.start, size: this.size},
          result({data, loading, networkStatus}) {
            if (!loading) {
              this.services = data.serviceSearch.map(service => service.image)
              if (this.services.length === 0) {
                this.fetchSuggestions()
                this.noResults = true

                this.$gtm.trackEvent({
                  event: 'ev-noResults',
                  category: 'Search',
                  action: 'No Results',
                  label: this.searchText,
                  value: 0
                })
              } else {
                this.watchScrolling = true
              }
              this.$setDisplay('v-progress-linear', 'none')
            }
          }
        }
      }
    },

    methods: {
      tagClick(text) {
        this.$gtm.trackEvent({
          event: 'ev-tagClick',
          category: 'Search',
          action: 'Filter Tags',
          label: text,
          value: 0
        })

        this.search(text)
        this.searchInput = text
        this.bodyPart = 'Alle'
      },

      styleClick(text) {
        this.$gtm.trackEvent({
          event: 'ev-styleClick',
          category: 'Search',
          action: 'Filter Styles',
          label: text,
          value: 0
        })

        this.search(text)
        this.searchInput = text
        this.bodyPart = 'Alle'
      },

      bodyPartClick(text) {
        this.$gtm.trackEvent({
          event: 'ev-bodyPart',
          category: 'Search',
          action: 'Filter Body Parts',
          label: text,
          value: 0
        })

        this.search(text)
        this.searchInput = text
        this.bodyPart = text
      },

      textSearch(text) {
        this.$gtm.trackEvent({
          event: 'ev-textSearch',
          category: 'Search',
          action: 'Text Search',
          label: text,
          value: 0
        })
        this.search(text)
        this.storeUserSearchTerm(text)
      },

      suggestionsClick(text) {
        this.$gtm.trackEvent({
          event: 'ev-suggestionsClick',
          category: 'Search',
          action: 'Suggestions Click',
          label: text,
          value: 0
        })

        this.search(text)
        this.searchInput = text
        this.bodyPart = 'Alle'
      },

      chatAdvice() {
        this.$gtm.trackEvent({
          event: 'ev-chatAdvice',
          category: 'Search',
          action: 'Chat Advice Click',
          label: 'chat',
          value: 0
        })
      },

      storeUserSearchTerm(text) {
        this.$apollo.mutate({
          mutation: STORE_SEARCH_TERM,
          variables: {
            'input': {
              'term':
                {
                  'data': JSON.stringify(
                    {
                      searchTerm: text,
                      urls: store.getHistory()
                    }
                  )
                }
            }
          }
        })
      },

      fetchSuggestions() {
        this.$apollo.addSmartQuery('suggest', {
          query: SUGGEST_QUERY,
          fetchPolicy: 'network-only',
          variables: {searchText: this.searchText},
          manual: true,
          result({data, loading, networkStatus}) {
            if (!loading) {
              this.suggest = data.suggest
            }
          }
        })
      },

      fetchImages($state) {
        this.$apollo.addSmartQuery('search', {
          query: SEARCH_QUERY,
          fetchPolicy: 'network-only',
          variables: {searchText: this.searchText, start: this.start, size: this.size},
          manual: true,
          result({data, loading, networkStatus}) {
            if (!loading) {
              this.services = [...this.services, ...data.serviceSearch.map(service => service.image)]

              if ((this.start === 0) && (this.services.length === 0)) {
                this.fetchSuggestions()
                this.noResults = true
                this.$setDisplay('v-progress-linear', 'none')

                this.$gtm.trackEvent({
                  event: 'ev-noResults',
                  category: 'Search',
                  action: 'No Results',
                  label: this.searchText,
                  value: 0
                })

                return
              }

              this.start = this.start + this.size

              if ($state) {
                if (data.serviceSearch.length < this.size) {
                  $state.complete()
                } else {
                  $state.loaded()
                }
              } else {
                // manually triggered search
                this.watchScrolling = true
                this.$setDisplay('v-progress-linear', 'none')
              }
            }
          }
        })
      },

      search(searchInput) {
        window.scrollTo({top: document.querySelector('#search-top').offsetTop + 60, behavior: 'smooth'})
        if (searchInput !== this.searchText) {
          if (searchInput) {
            this.$router.push({name: this.$route.name, query: {q: searchInput}, params: {ignoreScrollTop: true}})
            this.searchText = searchInput
          } else {
            this.$router.push({name: this.$route.name})
            this.searchText = ''
          }

          // reset state
          this.services = []
          this.start = 0
          this.watchScrolling = false
          this.noResults = false
          this.suggest = ''
          this.fetchImages()

          document.activeElement.blur()
        }
      }
    }
  }
</script>
