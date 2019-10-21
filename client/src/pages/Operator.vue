<template>
  <div class="mb-5" v-if="operator">

    <v-carousel hide-delimiters :hide-controls="operator.portrait.length > 0 ? false : true" :cycle="false" class="limited">
      <v-carousel-item
        v-for="(item,i) in operator.portrait"
        :key="i"
        :src="item.image.url800x800"
      >
      </v-carousel-item>
    </v-carousel>

    <v-container class="text pb-2">
      <h1>{{operator.fullName}}</h1>
      <div class="mt-2">
        {{operator.bio}}
      </div>

      <div v-if="operator.portfolio">
        <h2 class="mt-4">Mein Arbeiten</h2>
        <div class="text--tags" v-html="operator.tags"></div>
      </div>
    </v-container>

    <ServicesList v-if="operator.portfolio" :images="portfolio" @click="openCarousel"></ServicesList>

    <v-container>
      <div v-if="operator.companies && operator.companies.length > 0">
        <h2 class="mt-4 pb-2 text">Wo ich arbeite</h2>
        <GoogleMap :coordinates="operator.companies"></GoogleMap>
        <CompaniesList :companies="operator.companies"></CompaniesList>
      </div>

      <div v-if="operator.reviews && operator.reviews.length > 0" class="mt-4 text">
        <h2>Was Kunden über mich sagen</h2>
        <v-card v-for="(review, index) in operator.reviews" :key="index" class="mb-1 elevation-0">


          <v-layout row wrap class="pa-3">
            <v-flex xs12 sm6>
              <span class="h4">{{review.value.name}}</span>
            </v-flex>
            <v-flex xs12 sm6 class="text-sm-right">
              <v-rating v-if="review.value.rating" :value="review.value.rating" primary readonly small></v-rating>
            </v-flex>
          </v-layout>

          <v-card-text class="pt-0 pb-2 px-3">
            {{review.value.text}}
          </v-card-text>
        </v-card>
      </div>
    </v-container>

    <Contact :visible="showContact" :operator="operator" @close="showContact=false; showAppointmentButton=true"/>

    <ServicesCarousel
      :visible="showServicesCarousel"
      :images="portfolio"
      :operator="operator"
      :selectedIndex="selectedIndex"
      @close="showServicesCarousel=false"
      @contact="showContact=true"/>

    <v-btn
      class="v-btn v-btn--bottom v-btn--fixed v-btn--center theme--dark secondary v-btn--consultation open-appointment-dialog"
      color="secondary"
      block
      v-if="!showContact"
      @click.stop="openAppointmentDialog()">Kostenlos anfragen
    </v-btn>

  </div>
</template>


<script>
  import CompaniesList from '@/components/CompaniesList'
  import ServicesCarousel from '@/components/ServicesCarousel'
  import Contact from '@/components/Contact'
  import ServicesList from '@/components/ServicesList'
  import GoogleMap from '@/components/GoogleMap'

  import OPERATOR_QUERY from '@/graphql/gql/operator.gql'

  export default {
    components: {
      CompaniesList,
      Contact,
      ServicesCarousel,
      GoogleMap,
      ServicesList
    },

    data() {
      return {
        showContact: false,
        showServicesCarousel: false,
        selectedIndex: null
      }
    },

    props: {
      slug: {
        type: String,
        required: true
      }
    },

    computed: {
      portfolio: function () {
        return this.operator.portfolio.map(x => {
          return {...x.image}
        })
      }
    },

    methods: {
      openAppointmentDialog: function () {
        this.showContact = true
        this.$gtm.trackEvent({
          event: 'ev-OpenAppointmentDialog',
          category: 'Appointment',
          action: 'Start',
          label: 'open',
          value: 0
        })

        let products = [{
          name: this.operator.fullName,
          id: this.operator.id,
          price: '1',
          category: 'Operator',
          quantity: 1
        }]

        this.$gtm.trackEvent({
          event: 'ec-AddToCart',
          category: 'Ecommerce',
          action: 'Add To Cart',
          ecommerce: {
            add: {
              products: products
            }
          }
        })

        this.$gtm.trackEvent({
          event: 'ec-checkout',
          category: 'Ecommerce',
          action: 'Checkout',
          ecommerce: {
            checkout: {
              products: products
            }
          }
        })
      },

      openCarousel: function (img, index) {
        this.$gtm.trackEvent({
          event: 'ev-OpenServiceCarousel',
          category: 'Operators',
          action: 'click',
          label: 'open',
          value: 0
        })

        this.selectedIndex = index
        this.showServicesCarousel = true
      }
    },

    created() {
      this.$setDisplay('intercom-launcher-frame', 'none')
    },

    destroyed() {
      this.$setDisplay('intercom-launcher-frame', 'block')
    },

    apollo: {
      operator() {
        return {
          query: OPERATOR_QUERY,
          variables() {
            return {
              slug: this.slug
            }
          },
          result({data, loading, networkStatus}) {
            if (!loading) this.$setDisplay('v-progress-linear', 'none')

            this.$gtm.trackEvent({
              event: 'ec-productDetail',
              category: 'Ecommerce',
              action: 'Product Detail',
              ecommerce: {
                detail: {
                  products: [{
                    name: data.operator.fullName,
                    id: data.operator.id,
                    price: '1',
                    category: 'Operator'
                  }]
                }
              }
            })
          }
        }
      }
    }
  }
</script>
