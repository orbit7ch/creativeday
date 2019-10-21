<template>
  <div>
    <v-container v-if="operators">
      <h1 class="mb-2">Operators</h1>
    </v-container>
    <OperatorsList v-if="operators" :operators="operators" :listName="'OperatorsListPage'"></OperatorsList>
  </div>
</template>

<script>
  import OperatorsList from '@/components/OperatorsList'
  import OPERATORS_QUERY from '@/graphql/gql/operators.gql'

  export default {
    components: {
      OperatorsList
    },
    apollo: {
      operators() {
        return {
          query: OPERATORS_QUERY,
          result({data, loading, networkStatus}) {
            if (!loading) this.$setDisplay('v-progress-linear', 'none')
          }
        }
      }
    }
  }
</script>
