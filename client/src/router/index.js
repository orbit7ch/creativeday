import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store/core'

const routerOptions = [
  {path: '/', component: 'Page', name: 'home'},
  {path: '/operators', component: 'Operators', name: 'operators'},
  {path: '/companies', component: 'Companies', name: 'companies'},
  {
    path: '/services/:pk',
    component: 'Service',
    name: 'service',
    props: true,
    meta: {showBackButton: true}
  },
  {
    path: '/operators/:slug',
    component: 'Operator',
    name: 'operator',
    props: true,
    meta: {showBackButton: true}
  },
  {
    path: '/companies/:slug',
    component: 'Company',
    name: 'company',
    props: true,
    meta: {showBackButton: true}
  },

  {path: '/:slug', component: 'Page', name: 'pages', props: true},

  // admin
  // {path: '/admin/tagging', component: 'Tagging', name: 'tagging'},

  // catch all
  {path: '*', component: 'NotFound', name: 'not-found'}
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/pages/${route.component}.vue`)
  }
})

Vue.use(Router)

var router = new Router({
  routes,
  mode: 'history',
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    if (to.hash) {
      return {
        selector: to.hash,
        offset: {x: 0, y: -3}
      }
    }

    if (to.params.ignoreScrollTop) {
      return
    }

    return {x: 0, y: 0}
  }
})

router.beforeEach((to, from, next) => {
  store.addHistory(to.path)

  window.$setDisplay('v-progress-linear', 'block')
  next()
})

export default router
