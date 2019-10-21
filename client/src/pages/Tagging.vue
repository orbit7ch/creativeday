<template>
  <div>
    <div v-if="currentImage">
      <v-container grid-list-md>
        <v-layout row wrap>
          <v-flex xs12 sm6>
            <img :src="currentImage.url800x800"/>
          </v-flex>
          <v-flex xs12 sm6>
            <h3 class="headline mb-0">{{currentImage.title}} ({{currentImage.pk}})</h3>
            <tags-input element-id="tags"
                        ref="tags"
                        v-model="selectedTags"
                        :existing-tags="existingTags"
                        :typeahead="true"></tags-input>
            <v-btn small v-on:click="prev()" :disabled="prevDisabled">prev</v-btn>
            <v-btn small v-on:click="next()" :disabled="nextDisabled">Next</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
  </div>
</template>

<script>
  import store from '@/store/core'
  import IMAGES_QUERY from '@/graphql/gql/images'
  import UPDATE_IMAGES_MUTATION from '@/graphql/gql/updateImage'
  import apolloClient from '../graphql/client'

  export default {
    data() {
      return {
        store: store,
        images: [],
        currentIndex: 0,
        selectedTags: [],
        existingTags: {},
        initial: true,
        currentEndCursor: null,
        currentStartCursor: null,
        hasNextPage: true,
        hasPreviousPage: false
      }
    },
    methods: {
      next: function () {
        this.updateCurrentImage(() => {
          this.currentIndex = Math.min(this.currentIndex + 1, this.images.length - 1)
          if (this.currentIndex > this.images.length - 10) {
            this.loadImages()
          }
        })
      },
      prev: function () {
        this.currentIndex = Math.max(this.currentIndex - 1, 0)
      },
      updateCurrentImage: function (callback) {
        apolloClient.mutate({
          mutation: UPDATE_IMAGES_MUTATION,
          variables: {
            'input':
              {
                'id': this.currentImage.id,
                'image': {
                  'tagSlugs': this.selectedTags.join()
                }
              }
          }
        }).then((res) => {
          if (res.data.updateImage.updatedImage) {
            this.images[this.currentIndex] = res.data.updateImage.updatedImage
            this.existingTags = Object.assign(...res.data.updateImage.tags.map(d => ({[d.slug]: d.name})))
          }
          callback()
        })
      },
      loadImages: function (forward = true) {
        var variables = {}

        if (forward) {
          variables.after = this.currentEndCursor
          if (!this.hasNextPage) {
            return
          }
        } else {
          variables.before = this.currentStartCursor
          if (!this.hasPreviousPage) {
            return
          }
        }

        this.$apollo.addSmartQuery('container', {
          query: IMAGES_QUERY,
          fetchPolicy: 'network-only',
          variables: variables,
          manual: true,
          result({data, loading, networkStatus}) {
            if (!loading) {
              if (data.images) {
                var items = data.images.edges.map(entry => ({...entry.node}))
                if (forward) {
                  this.images = this.images.concat(items)
                  this.currentEndCursor = data.images.pageInfo.endCursor
                  this.hasNextPage = data.images.pageInfo.hasNextPage
                } else {
                  this.images = items.concat(this.images)
                  this.currentStartCursor = data.images.pageInfo.startCursor
                  this.hasPreviousPage = data.images.pageInfo.hasPreviousPage
                }
              }
              if (data.tags && Object.keys(this.existingTags).length === 0) {
                this.existingTags = Object.assign(...data.tags.map(d => ({[d.slug]: d.name})))
              }
            }
          }
        })
      }
    },
    watch: {
      // whenever question changes, this function will run
      currentImage: function (prev, current) {
        this.selectedTags = this.currentImage.tagsList.map(x => x.slug)
        if (this.$refs.tags) {
          this.$refs.tags.$el.querySelector('input').focus()
        }
      }
    },
    computed: {
      currentImage: function () {
        return this.images[this.currentIndex]
      },
      nextDisabled: function () {
        return this.images.length - 1 === this.currentIndex
      },
      prevDisabled: function () {
        return this.currentIndex === 0
      }
    },
    mounted() {
      this.$setDisplay('v-progress-linear', 'none')
      if (this.images.length === 0) {
        this.loadImages()
        document.onkeydown = e => {
          switch (e.keyCode) {
            case 37:
              this.prev()
              break
            case 39:
              this.next()
              break
          }
        }
      }
    }
  }
</script>

<style lang="scss">
  .tags-input-default-class {
    background-color: rgba(255, 255, 255, 0.3);
    // font-size: 1.2rem;
    margin-bottom: 5px;
    padding: .5rem;
    border-radius: 0;

    ::placeholder, input { /* Chrome, Firefox, Opera, Safari 10.1+ */
      color: #212529;
    }
  }

  img {
    max-width: 100%;
  }

  .badge-light {
    color: #212529;
    background-color: #dbdbdb;;
  }

  .badge {
    font-size: 1.2rem;
    font-weight: initial;
  }

  .tags-input-remove {
    width: 0.8rem;
    height: 0.8rem;
  }

  .badge-pill {
    border-radius: 3px;
  }
</style>
