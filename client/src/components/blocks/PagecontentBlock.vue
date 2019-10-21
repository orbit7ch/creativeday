<template>
  <section>
    <div v-for="(subItem, i) in item.page" :key="i"
         :class="[subItem.value.space_after, subItem.block_type]">
      <component :is="subItem.block_type" :item="subItem"></component>
    </div>
  </section>
</template>

<script>

  import ButtonBlock from '@/components/blocks/ButtonBlock'
  import LogoBlock from '@/components/blocks/LogoBlock'
  import TextBlock from '@/components/blocks/TextBlock'
  import IconBlock from '@/components/blocks/IconBlock'

  export default {
    components: {
      ButtonBlock,
      LogoBlock,
      TextBlock,
      IconBlock
    },
    props: [
      'item'
    ]
  }
</script>
