<template>
  <div v-if="service && !loading">
    <v-carousel hide-delimiters :hide-controls="images.length > 0 ? false : true" :cycle="false">
      <v-carousel-item
        v-for="(item,i) in images"
        :key="i"
        :src="item.url800x800"
      >
      </v-carousel-item>
    </v-carousel>

    <v-container class="pb-0 text">
      <div class="text--tags mb-1" v-html="service.image.tags"></div>
      <h1 v-if="operators" class="h2 py-3">Hier kriegst du einen solchen Service</h1>
    </v-container>

    <OperatorsList class="mt-1" v-if="serviceOperators" :operators="serviceOperators.operators" :listName="'ServiceDetailPage'"></OperatorsList>

    <div v-if="serviceMore">
      <v-container class="py-2 text">
        <h2>Mehr davon</h2>
      </v-container>

      <ServicesList :images="more" @click="click"></ServicesList>
      <InfiniteLoading
        v-if="watchScrolling"
        @infinite="fetchMore"
        :distance="distance"
        spinner="spiral"
        ref="infiniteLoading">
        <span slot="no-results"></span><span slot="no-more"></span>
      </InfiniteLoading>

    </div>
  </div>
</template>

<script>
  import OperatorsList from '@/components/OperatorsList'
  import ServicesList from '@/components/ServicesList'
  import SERVICE_HERO_QUERY from '@/graphql/gql/service/hero.gql'
  import SERVICE_OPERATORS_QUERY from '@/graphql/gql/service/operators.gql'
  import SERVICE_MORE_QUERY from '@/graphql/gql/service/more.gql'
  import InfiniteLoading from 'vue-infinite-loading'

  export default {
    props: ['pk'],

    components: {
      OperatorsList,
      ServicesList,
      InfiniteLoading
    },

    computed: {
      images: function () {
        return [this.service.image, ...this.service.similar]
      }
    },

    apollo: {
      service() {
        return {
          query: SERVICE_HERO_QUERY,
          variables() {
            return {
              pk: this.pk + ''
            }
          },
          result({data, loading, networkStatus}) {
            if (!loading) {
              this.loading = false
              this.$setDisplay('v-progress-linear', 'none')
            }
          }
        }
      },

      serviceOperators() {
        return {
          query: SERVICE_OPERATORS_QUERY,
          variables() {
            return {
              pk: this.pk + ''
            }
          },
          result({data, loading, networkStatus}) {
            if (!loading) this.$setDisplay('v-progress-linear', 'none')
          }
        }
      },

      serviceMore() {
        return {
          query: SERVICE_MORE_QUERY,
          variables() {
            return {
              pk: this.pk + ''
            }
          },
          result({data, loading, networkStatus}) {
            if (!loading) {
              this.more = data.serviceMore.more

              this.$setDisplay('v-progress-linear', 'none')
              this.watchScrolling = true
            }
          }
        }
      }
    },

    data() {
      return {
        items: [],
        operators: [],
        more: [],
        loading: false,

        watchScrolling: false,
        start: 30,
        size: 30,
        distance: 500
      }
    },

    methods: {
      click(img) {
        this.loading = true
        this.watchScrolling = false
        this.start = 30
        this.$router.push({name: 'service', params: {pk: img.pk}})
      },

      fetchMore($state) {
        this.$apollo.addSmartQuery('serviceMore', {
          query: SERVICE_MORE_QUERY,
          fetchPolicy: 'network-only',
          variables: {pk: this.pk + '', start: this.start, size: this.size},
          manual: true,
          result({data, loading, networkStatus}) {
            if (!loading) {
              this.more = [...this.more, ...data.serviceMore.more]
              this.start = this.start + this.size
              if (data.serviceMore.more.length < this.size) {
                $state.complete()
              } else {
                $state.loaded()
              }
            }
          }
        })
      }
    }
  }
</script>


<style lang="scss">
  .v-carousel {
    height: 65vh;
  }
</style>



