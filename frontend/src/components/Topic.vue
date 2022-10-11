<script>
import axios from 'axios'
import { reactive, onMounted, toRefs  } from 'vue'
import useEventsBus from './eventbus' 






export default {
  name: 'Topics',

  methods:{
      selectTopic(topicname){
         EventBus.assign( topicname);
      }

    },

  setup() {
    let base_url = "http://127.0.0.1:8000/api/Topics/";
    const Topic_blank = { url: '', name: '', rank:0 }
  
    const {emit}=useEventsBus()

    const state = reactive({
      Topic_list: [],
      Topic: Object.assign({}, Topic_blank),
 
    });


    const getTopic = () => {
        axios.get(base_url).then(res => {
        state.Topic_list = res.data;
        state.Topic = Object.assign({}, Topic_blank)
      }).catch(err => {
        console.log(err);
      })
    };
    
    const selectT=(text)=>{
      emit('selectedtopic',text)

    }
   

    onMounted(() => {
      getTopic();
   
    });

    return {
      ...toRefs(state),
      selectT
    }


  }
}

</script>

<template>
<div >
<ol >
  <li v-for="item in Topic_list" :key="item.url"  @click="selectT(item.name)">
   {{ item.name }} 
  </li>
</ol>
  </div>
</template>

