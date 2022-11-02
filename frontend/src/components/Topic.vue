 <script>
import axios from 'axios'
import { reactive, onMounted, toRefs  } from 'vue'
import useEventsBus from './eventbus' 
import router from '../router'





export default {
  name: 'Topics',

  methods:{
      selectTopic(topicname){
         EventBus.assign( topicname);
         router.push({ name: 'Paper'});
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
      <div class="row">
          <div class="row mb-12">
              <div class="col-lg-11 col-md-12 mb-md-12 mb-12">
                <div class="card" style="width:200%">
                  <div class="card-header pb-0">
                    <div class="row">
                      <div class="col-lg-50 col-50">
                        <h6>Top 10 topics in twitter</h6>
                        <p class="text-sm mb-0">
                          <i class="fa fa-check text-info" aria-hidden="true"></i>
                          <span class="font-weight-bold ms-1">most popular topics</span>
                        </p>
                      </div>
                      <div class="col-lg-12 col-12 my-auto text-end">
                        
                      </div>
                    </div>
                  </div>
                  <div class="card-body px-0 pb-2">
          <div class="table-resonsive">
            <!-- <table class="table align-items-center mb-0"> -->
<div >
<ol >
  <li v-for="item in Topic_list" :key="item.url"  @click="selectT(item.name)" class="alert alert-primary alert-dismissible text-white">
   {{ item.name }} 
  </li>
</ol>
<div v-if="text===''" style="position: absolute;right: 20PX;left: 950PX;">
    <Barchart />
    </div>
  </div>
</div>
</div>
</div>  </div>  </div>  </div>

</template>

