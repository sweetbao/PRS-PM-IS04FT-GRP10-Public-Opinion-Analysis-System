<script>
import axios from 'axios'
import { reactive, onMounted, toRefs } from 'vue'
import useEventsBus from './eventbus'
import router from '../router'
import moment from 'moment';




export default {
  name: 'Topics',

  methods: {
    selectTopic(topicname) {
      EventBus.assign(topicname);
      router.push({ name: 'Paper' });
    },
   
    dateTime(value) {
      return moment(value).format("DD/MM/YYYY hh:mm:ss");
    },

  },



  setup() {
    let base_url = "http://127.0.0.1:8000/api/Topics/";
    const Topic_blank = { url: '', name: '', rank: 0 };
   
    const { emit } = useEventsBus()

    const state = reactive({
      Topic_list: [],
      Topic: Object.assign({}, Topic_blank),
      currentFilterValue:'',
      fliter_list:[]
    });


    const getTopic = () => {
      axios.get(base_url).then(res => {
        state.Topic_list = res.data;
        state.Topic = Object.assign({}, Topic_blank);
        reassign()
      }).catch(err => {
        console.log(err);
      })
    };

    const selectT = (text) => {
      emit('selectedtopic', text)

    }

    const filterdata=(data)=>{
  
      if(state.currentFilterValue != ''){
      	return data.filter(function(d){
         
      		return d.name.toLowerCase().includes(state.currentFilterValue.slice().toLowerCase());
       
      	});          
      }
      else{
       return data
      }    	

    }

    const reassign=()=>{
      state.fliter_list=filterdata( state.Topic_list)

    }

    onMounted(() => {
      getTopic();
  
    });

    return {
      ...toRefs(state),
      selectT,
      
      filterdata,
      reassign
    }


  }
}

</script>

<template>
  <div class="row">
    <div class="row mb-12">
      <div class="col-lg-11 col-md-12 ">
        <div class="card">
          <div class="card-header pb-0">
            <div class="row">
              <div class="col-lg-50 col-50">
                <h6>Previous Top 10 topics in twitter</h6>
               
              </div>
              <div class="col-lg-12 col-12 my-auto text-end">
                <input placeholder="filter value" v-model="currentFilterValue" />
                <input type="submit" value="filter" @click="reassign()">
              </div>
            </div>
          </div>
          <div class="card-body px-0 pb-2">
            <div class="table-resonsive">
              <!-- <table class="table align-items-center mb-0"> -->
              <div>
                <ol>
                  <li v-for="item in fliter_list" :key="item.url" @click="selectT(item.name)"
                    class="alert alert-primary alert-dismissible text-white">
                    {{item.rank}}. {{ item.name }} -  <span>Record time: </span>{{dateTime( item.time)}} - <span>Amount: </span>{{item.volume}} - 
                    <span>Positive: </span> {{100* Number(item.positiveNumber) /(Number(item.negativeNumber)+Number(item.positiveNumber)+Number(item.neutralNumber))}}% - 
                    <span>Negative: </span> {{100*Number(item.negativeNumber) /(Number(item.negativeNumber)+Number(item.positiveNumber)+Number(item.neutralNumber))}}%
                  </li>
                </ol>
                
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

