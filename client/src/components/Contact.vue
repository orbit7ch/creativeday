<template>
  <div>
    <v-dialog v-model="showConfirmation" max-width="290">
      <v-card class="contact-confirmation">
        <v-card-text class="pa-4">
          <div class="speech-bubble speech-bubble--bottom">
            Vielen Dank {{name}}. Ich werde mich bei dir zur Terminvereinbarung melden
          </div>

          <div class="text-xs-center pt-2">
            <v-avatar size="50px">
              <v-img
                :src="operator.mainPortrait.url800x800"
                alt="operator"
              ></v-img>
            </v-avatar>
            <div class="mt-2">{{operator.fullName}}</div>
          </div>

        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn depressed color="secondary" @click.native="closeConfirmation">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-if="!showConfirmation" v-model="show" scrollable persistent max-width="500px">
      <v-card>

        <v-card-title class="py-0 pr-0">
          <h3 class="h4">Anfragen</h3>
          <v-spacer></v-spacer>
          <v-btn flat icon depressed @click.stop="abort()">
            <v-icon>close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pt-0">
          <div style="max-width: 180px; margin:auto">
            <div class="speech-bubble speech-bubble--bottom text-xs-center">
              Ich freue mich über deine Nachricht.
            </div>
          </div>
          <div class="text-xs-center pt-2">
            <v-avatar size="50px">
              <v-img
                :src="operator.mainPortrait.url800x800"
                alt="operator"
              ></v-img>
            </v-avatar>
            <div class="mt-2">{{operator.pseudonym}}</div>
          </div>

          <v-container grid-list-md class="container--fix pa-0">
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field v-model="name" :rules="nameRules" class="pa-0 " id="name" placeholder="Name"
                            required></v-text-field>
              <v-text-field v-model="email" :rules="emailRules" class="pa-0" id="email" placeholder="Email"
                            required></v-text-field>
              <!--
              <v-text-field v-model="phone" :rules="phoneRules" class="pa-0" id="phone" placeholder="Telefon"
                            required></v-text-field>
                            -->
              <v-textarea v-model="message" class="pt-4"
                          auto-grow
                          height="60"
                          id="message"
                          placeholder="Hast du Ideen, Vorstellungen oder Fragen?"></v-textarea>
            </v-form>
          </v-container>

        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="submit-appointment" color="secondary" depressed @click.stop="submit()">Absenden
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import STORE_EVENT_MUTATION from '@/graphql/gql/storeEvent'
  import apolloClient from '@/graphql/client'
  import store from '@/store/core'

  export default {
    props: ['visible', 'operator'],

    data() {
      return {
        showConfirmation: false,
        message: '',
        name: '',
        valid: true,
        nameRules: [
          v => !!v || 'Bitte einen Namen eingeben'
        ],
        email: '',
        emailRules: [
          v => !!v || 'Gib bitte deine Email-Adresse an',
          v => /.+@.+/.test(v) || 'Gib bitte eine gültige Email-Adresse an'
        ],
        phone: '',
        phoneRules: [
          v => !!v || 'Gib bitte deine Telefonnummer an'
        ]
      }
    },

    methods: {
      abort() {
        this.show = false
        this.$gtm.trackEvent({
          event: 'ev-abortAppointment',
          category: 'Appointment',
          action: 'abort',
          label: 'abort',
          value: 0
        })

        this.$gtm.trackEvent({
          event: 'ec-removeFromCart',
          category: 'Ecommerce',
          action: 'Remove From Cart',
          ecommerce: {
            remove: {
              products: [{
                name: this.operator.fullName,
                id: this.operator.id,
                price: '1',
                category: 'Operator',
                quantity: 1
              }]
            }
          }
        })

        this.$emit('close')
      },

      closeConfirmation() {
        this.showConfirmation = false
        this.$emit('close')
      },

      submit() {
        if (this.$refs.form.validate()) {
          this.showConfirmation = true
          this.$gtm.trackEvent({
            event: 'ev-submitAppointment',
            category: 'Appointment',
            action: 'submit',
            label: 'submit',
            value: 0
          })

          this.$gtm.trackEvent({
            event: 'ec-purchase',
            category: 'Ecommerce',
            action: 'Purchase',
            ecommerce: {
              purchase: {
                actionField: {
                  // ugly way to get a transaction id ....
                  'id': 'ID-' + Math.random().toString(36).replace(/[^a-z]+/g, ''),
                  'revenue': '10',
                  'tax': '0',
                  'shipping': '0'
                },
                products: [{
                  name: this.operator.fullName,
                  id: this.operator.id,
                  price: '1',
                  category: 'Operator',
                  quantity: 1
                }]
              }
            }
          })

          apolloClient.mutate({
            mutation: STORE_EVENT_MUTATION,
            variables: {
              'input': {
                'event':
                  {
                    'title': 'Appointment Request',
                    'data': JSON.stringify(
                      {
                        name: this.name,
                        email: this.email,
                        // phone: this.phone,
                        message: this.message,
                        urls: store.getHistory()
                      }
                    )
                  }
              }
            }
          }).then((res) => {
            // FIXME Error Handling
            // console.info(res)
          })
        } else {
          var label = []
          for (var i = 0; i < this.$refs.form.$children.length; i++) {
            var c = this.$refs.form.$children[i]
            if (c.errorBucket.length) {
              label.push(c.$attrs.id)
            }
          }
          this.$gtm.trackEvent({
            event: 'ev-submitAppointment-invalid',
            category: 'Appointment',
            action: 'invalid-submit',
            label: label.join('-'),
            value: 0
          })
        }
      }
    },

    computed: {
      show: {
        get() {
          return this.visible
        },
        set(value) {
          if (!value) {
            this.$emit('close')
          }
        }
      }
    }
  }
</script>
