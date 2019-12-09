<template>
  <div class="dealRegSearch">
    <PartNumberSearch/>
  </div>
</template>

<script>
// @ is an alias to /src
import PartNumberSearch from '@/components/PartNumberSearch.vue'

export default {
  name: 'dealRegSearch',
  components: {
    PartNumberSearch
  }
}
</script>
