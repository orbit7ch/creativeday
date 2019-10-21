<template>
  <div v-if="page" :class="['heading--'+page.headingAlignment]">
    <div v-for="(item, i) in page.content" :key="i"
         :class="[item.value.space_after, item.blockType]">
      <component :is="item.blockType" :item="item"></component>
    </div>
  </div>
</template>

<script>
  import PAGE_QUERY from '@/graphql/gql/page.gql'

  import ButtonBlock from '@/components/blocks/ButtonBlock'
  import HeroBlock from '@/components/blocks/HeroBlock'
  import HerotextBlock from '@/components/blocks/HerotextBlock'
  import ImageBlock from '@/components/blocks/ImageBlock'
  import LogoBlock from '@/components/blocks/LogoBlock'
  import TextBlock from '@/components/blocks/TextBlock'
  import TilesBlock from '@/components/blocks/TilesBlock'
  import SwiperBlock from '@/components/blocks/SwiperBlock'
  import CarouselBlock from '@/components/blocks/CarouselBlock'
  import IconBlock from '@/components/blocks/IconBlock'
  import PagecontentBlock from '@/components/blocks/PagecontentBlock'
  import AvatarBlock from '@/components/blocks/AvatarBlock'
  import FormBlock from '@/components/blocks/FormBlock'
  import SearchBlock from '@/components/blocks/SearchBlock'
  import TextsearchBlock from '@/components/blocks/TextsearchBlock'

  export default {
    props: {
      slug: {
        type: String
      }
    },

    components: {
      ButtonBlock,
      HeroBlock,
      HerotextBlock,
      ImageBlock,
      LogoBlock,
      TextBlock,
      TilesBlock,
      SwiperBlock,
      CarouselBlock,
      IconBlock,
      PagecontentBlock,
      AvatarBlock,
      FormBlock,
      SearchBlock,
      TextsearchBlock
    },

    apollo: {
      page() {
        return {
          query: PAGE_QUERY,
          variables() {
            return {
              slug: this.slug
            }
          },
          result({data, loading, networkStatus}) {
            if (!loading) this.$setDisplay('v-progress-linear', 'none')
          },
          error(/* error */) {
            // FIXME check if its a `page not exists` error or something else

            this.$router.push({name: 'not-found'})
          }
        }
      }
    }
  }
</script>

<style scoped>

</style>
