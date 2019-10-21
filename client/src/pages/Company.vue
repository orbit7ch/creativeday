<template>
  <div v-if="company">

    <v-carousel hide-delimiters :hide-controls="company.portrait.length > 0 ? false : true" :cycle="false" class="limited">
      <v-carousel-item
        v-for="(item,i) in company.portrait"
        :key="i"
        :src="item.image.url800x800"
      >
      </v-carousel-item>
    </v-carousel>

    <v-container>
      <h1>{{company.name}}</h1>
      <div class="my-2">
        {{company.bio}}
      </div>

      <GoogleMap :coordinates="[{longitude: company.longitude, latitude: company.latitude}]"></GoogleMap>
      <h2 class="mt-3 mb-2">Operators</h2>
      <OperatorsList v-if="company.operators" :operators="company.operators" :listName="'Company Detail Page'"></OperatorsList>
    </v-container>
  </div>
</template>

<script>
  import OperatorsList from '@/components/OperatorsList'
  import GoogleMap from '@/components/GoogleMap'

  import COMPANY_QUERY from '@/graphql/gql/company.gql'

  export default {
    components: {
      OperatorsList,
      GoogleMap
    },
    props: {
      slug: {
        type: String,
        required: true
      }
    },
    apollo: {
      company() {
        return {
          query: COMPANY_QUERY,
          variables() {
            return {
              slug: this.slug
            }
          },
          result({data, loading, networkStatus}) {
            if (!loading) this.$setDisplay('v-progress-linear', 'none')
          }
        }
      }
    }
  }
</script>
