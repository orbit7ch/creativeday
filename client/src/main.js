/* eslint-disable import/first */

// ordering is crucial for overwriting styles ...

require('vuetify/src/stylus/app.styl')

import 'babel-polyfill'
import '@voerro/vue-tagsinput/dist/style.css'
import 'swiper/dist/css/swiper.css'
import Vue from 'vue'
import VueApollo from 'vue-apollo'
import VueGtm from 'vue-gtm'
import router from './router'
import apolloClient from './graphql/client'
import axios from 'axios'
import VueAxios from 'vue-axios'
import * as VueGoogleMaps from 'vue2-google-maps'
// import VoerroTagsInput from '@voerro/vue-tagsinput'
import VueAwesomeSwiper from 'vue-awesome-swiper'

import {
  Vuetify,
  VApp,
  VToolbar,
  VAvatar,
  VBtn,
  VMenu,
  VCard,
  VCarousel,
  VDialog,
  VTextField,
  VDivider,
  VGrid,
  VIcon,
  VForm,
  VList,
  VImg,
  VNavigationDrawer,
  VTextarea,
  VRating,
  VChip,
  transitions
} from 'vuetify'

import App from './App'

Vue.config.productionTip = false

var debug = process.env.NODE_ENV !== 'production'

window.$setDisplay = function (classSelector, value) {
  var e = document.getElementsByClassName(classSelector)
  if (e && e.length) {
    e[0].style.display = value
  } else {
    console.info('"' + classSelector + '" not found. Set to "' + value + '"')
  }
}

Object.defineProperty(Vue.prototype, '$setDisplay', {value: window.$setDisplay})


const apolloProvider = new VueApollo({
  defaultClient: apolloClient
})

Vue.use(VueApollo)
Vue.use(VueAxios, axios)
Vue.use(VueAwesomeSwiper)


Vue.use(Vuetify, {
  components: {
    VApp,
    VAvatar,
    VToolbar,
    VBtn,
    VCard,
    VCarousel,
    VDialog,
    VMenu,
    VDivider,
    VTextField,
    VGrid,
    VIcon,
    VList,
    VImg,
    VForm,
    VNavigationDrawer,
    VTextarea,
    transitions,
    VRating,
    VChip
  },
  theme: {
    primary: '#3a2099',
    secondary: '#fa6400'
  }
})

// Vue.component('tags-input', VoerroTagsInput)

Vue.use(VueGtm, {
  id: window.$gtm_id, // Your GTM ID
  enabled: true, // defaults to true. Plugin can be disabled by setting this to false for Ex: enabled: !!GDPR_Cookie (optional)
  debug: debug,
  vueRouter: router
})

Vue.prototype.$getFilter = function () {
  return [
    'Filter 1',
    'Filter 2',
    'Filter 3',
    'Filter 4',
    'Filter 5',
    'Filter 6'
  ]
}

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyB4RBCUxLb9OsUTsc5p5h_Kl3D48shaKHk',
    libraries: 'places'
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  apolloProvider,
  render: h => h(App)
})




