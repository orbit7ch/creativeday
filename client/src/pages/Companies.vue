<template>
  <div>
    <v-container v-if="companies">
      <h1 class="mb-2">Companies</h1>
    </v-container>
    <div class="px-3">
      <CompaniesList v-if="companies" :companies="companies"></CompaniesList>
    </div>
  </div>
</template>

<script>
  import CompaniesList from '@/components/CompaniesList'
  import COMPANIES_QUERY from '@/graphql/gql/companies.gql'

  export default {
    components: {
      CompaniesList
    },
    apollo: {
      companies() {
        return {
          query: COMPANIES_QUERY,
          result({data, loading, networkStatus}) {
            if (!loading) this.$setDisplay('v-progress-linear', 'none')
          }
        }
      }
    }
  }
</script>
