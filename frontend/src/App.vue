<script >
import { RouterLink, RouterView } from 'vue-router'
import TextEmotion from './components/TextEmotion.vue'



export default {
  name:'App',
  components:{
    TextEmotion,
    
}
}

</script>

<template>
  <div style="display:flex">
    
   <div class="cocol-md-10"><TextEmotion/></div>
</div>
</template>
