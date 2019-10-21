<template>
  <v-app>
    <div>
      <v-toolbar color="white"> <!-- FIXEME fixed -->
        <v-toolbar-side-icon @click.stop="drawer = !drawer" v-if="!$route.meta.showBackButton"></v-toolbar-side-icon>
        <v-btn v-if="$route.meta.showBackButton" icon @click="$router.go(-1)">
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <v-toolbar-title>
          <router-link :to="{ name: 'home'}" class="router white--text">
            <LogoDark class="logo-toolbar"></LogoDark>
          </router-link>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon :to="'/search'" exact router v-if="!$route.meta.hideSearchButton">
          <v-icon>search</v-icon>
        </v-btn>
      </v-toolbar>

      <v-content>
        <v-fade-transition>
          <router-view></router-view>
        </v-fade-transition>
      </v-content>

      <v-navigation-drawer
        v-model="drawer"
        absolute
        temporary
        dark
      >
        <v-toolbar flat color="primary" dark>
          <v-list>
            <v-list-tile>
              <v-list-tile-title class="title">
                <router-link :to="{ name: 'home'}" class="router white--text">
                  <LogoWhite class="logo-drawer"></LogoWhite>
                  <v-icon v-if="isInternalUser" large class="pl-2 internal-user">insert_emoticon</v-icon>
                </router-link>
              </v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-toolbar>
        <v-divider></v-divider>
        <v-list class="pt-2 nav-list" dense>
          <v-list-tile ripple :to="{ name: 'home'}" exact router>
            <v-list-tile-content>
              <v-list-tile-title class="h4">Home</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile ripple :to="entry.url" v-for="entry in menu.main" :key="entry.url">
            <v-list-tile-content>
              <v-list-tile-title class="h4">{{entry.title}}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-divider class="pt-2"></v-divider>

          <v-list-tile :to="entry.url" ripple v-for="entry in menu.minor" :key="entry.url">
            <v-list-tile-content>
              <v-list-tile-title class="h4 light-text">{{entry.title}}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

        </v-list>

      </v-navigation-drawer>

    </div>
  </v-app>
</template>

<script>

  import LogoWhite from './assets/img/logo-white.svg'
  import LogoDark from './assets/img/logo-dark.svg'
  import gql from 'graphql-tag'

  export default {
    name: 'App',
    components: {
      LogoWhite,
      LogoDark
    },
    data() {
      return {
        drawer: null,
        active: null,
        isInternalUser: document.cookie.indexOf('i_am_internal=true') > -1,
        menu: {}
      }
    },
    apollo: {
      menu: gql`query MenuQuery {menu}`
    }
  }
</script>

<style lang="scss">
  @import "styles/main";
</style>
