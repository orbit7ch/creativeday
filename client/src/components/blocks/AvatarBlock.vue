<template>
  <div>
    <v-container grid-list-sm class="py-0">
      <div>
        <v-layout row wrap>
          <v-flex xs2>
            <v-avatar size=100 class="v-avatar--responsive">
              <v-img
                :src="item.image.url800x800"
                alt="Avatar"
              ></v-img>
            </v-avatar>
          </v-flex>
          <v-flex xs10 class="pl-2">
            <h3 class="h4 text--left">{{item.value.heading}}</h3>
            <div class="mb-1 text text--left" v-html="item.value.text"></div>
          </v-flex>
        </v-layout>
      </div>
    </v-container>
  </div>
</template>

<script>
  export default {
    props: ['item']
  }
</script>
