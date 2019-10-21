<template>
  <div v-if="show">
    <v-dialog v-model="show" fullscreen scrollable hide-overlay transition="dialog-bottom-transition">
      <v-card>
        <v-card-title>
          <v-avatar size="50px">
            <v-img
              :src="operator.mainPortrait.url800x800"
              alt="mage"
              class="mr-3"
              @click.stop="show=false"
            ></v-img>
          </v-avatar>
          <span class="headline title-pseudonym">{{operator.pseudonym}}</span>

          <v-btn fixed top right flat icon depressed @click.stop="show=false">
            <v-icon>close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-carousel hide-delimiters :cycle="false" v-model="index">
            <v-carousel-item
              v-for="(item,i) in images"
              :key="i"
              :src="item.url800x800"
              :ref="'img'+i"
            >
            </v-carousel-item>
          </v-carousel>
        </v-card-text>
        <v-card-actions>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  export default {
    props: ['visible', 'images', 'operator', 'selectedIndex'],
    data() {
      return {
        index: null,
        imgSet: false
      }
    },

    // what a hack to make it work....
    // the problem is, the first slide is often empty without all those checks
    // (either on the first or 2nd time the dialog is visible)

    updated: function () {
      let item = this.$refs['img' + this.selectedIndex]
      if (item.length > 0 && !this.imgSet) {
        this.$nextTick(function () {
          this.index = this.selectedIndex
          this.imgSet = true
        })
      }
    },

    computed: {
      show: {
        get() {
          return this.visible
        },
        set(value) {
          if (!value) {
            this.index = null
            this.imgSet = false
            this.$emit('close')
          }
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
  .v-card__text {
    padding: 0;
  }

  .title-pseudonym {
    max-width: 200px;
    line-height: 20px !important;

  }

  .v-card__title {
    max-height: 70px;
    padding: 15px 25px;
  }

  .v-carousel {
    height: 80vh;
  }

  .v-card__actions {
    max-height: 65px !important;
    height: 65px !important;
  }

</style>
