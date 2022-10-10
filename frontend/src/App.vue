<script >
import { RouterLink, RouterView } from 'vue-router'
import TextEmotion from './components/TextEmotion.vue'

export default {
  name:'App',
  components:{
    TextEmotion
  }
}

</script>

<template>
  <div class="row">
  <TextEmotion/>
  </div>
</template>
