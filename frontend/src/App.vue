<script >
import { RouterLink, RouterView } from 'vue-router'
import TextEmotion from './components/TextEmotion.vue'
import Topic from './components/Topic.vue'


export default {
  name:'App',
  components:{
    TextEmotion,
    Topic
}
}

</script>

<template>
  <div style="display:flex">
    <div class="cocol-md-2"><Topic/></div>
    <div class="cocol-md-10"><TextEmotion/></div>
</div>
</template>
