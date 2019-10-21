<template>
  <v-container>

    <v-dialog v-model="showConfirmation" max-width="290">
      <v-card class="contact-confirmation">
        <v-card-text class="pa-4">
          {{item.value.confirmation_message}}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn depressed color="secondary" @click.native="showConfirmation=false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field v-if="item.value.show_name" id="name" v-model="name" :rules="nameRules" class="pa-0"
                    placeholder="Name"
                    required></v-text-field>
      <v-text-field v-if="item.value.show_email" id="email" v-model="email" :rules="emailRules" class="pa-0"
                    placeholder="Email"
                    required></v-text-field>
      <v-text-field v-if="item.value.show_phone" id="phone" v-model="phone" :rules="phoneRules" class="pa-0"
                    placeholder="Telefon"
                    required></v-text-field>
      <v-textarea v-if="item.value.show_message" id="message" v-model="message" class="pt-4"
                  auto-grow
                  height="60"
                  placeholder="Schreibe uns eine Nachricht"></v-textarea>
    </v-form>
    <v-btn class="submit-form" color="secondary" depressed @click.stop="submit()">Absenden</v-btn>
  </v-container>
</template>

<script>
  import STORE_EVENT_MUTATION from '@/graphql/gql/storeEvent'
  import apolloClient from '@/graphql/client'
  import store from '@/store/core'

  export default {
    props: [
      'item'
    ],

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

      submit() {
        if (this.$refs.form.validate()) {
          this.$setDisplay('v-progress-linear', 'block')
          this.$gtm.trackEvent({
            event: 'ev-submitForm',
            category: this.item.value.form_name,
            action: 'submit',
            label: 'submit',
            value: 0
          })

          apolloClient.mutate({
            mutation: STORE_EVENT_MUTATION,
            variables: {
              'input': {
                'event':
                  {
                    'title': this.item.value.form_name,
                    'data': JSON.stringify(
                      {
                        name: this.name,
                        email: this.email,
                        phone: this.phone,
                        message: this.message,
                        urls: store.getHistory()
                      }
                    )
                  }
              }
            }
          }).then((res) => {
            this.$refs.form.reset()
            this.showConfirmation = true
            this.$setDisplay('v-progress-linear', 'none')
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
            event: 'ev-submitForm-invalid',
            category: this.item.value.form_name,
            action: 'invalid-submit',
            label: label.join('-'),
            value: 0
          })
        }
      }
    }

  }
</script>
