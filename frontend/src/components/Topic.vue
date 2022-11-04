<script>
import axios from 'axios'
import { reactive, onMounted, toRefs } from 'vue'
import useEventsBus from './eventbus'
import router from '../router'
import BarChart from '../components/Barchart.vue'




export default {
  name: 'Topics',
  components: {
    BarChart,
  },
  methods: {
    selectTopic(topicname) {
      EventBus.assign(topicname);
      router.push({ name: 'Paper' });
    }

  },

  

  setup() {
    let base_url = "http://127.0.0.1:8000/getTopic/";
    const Topic_blank = { url: '', name: '', rank: 0 }

    const { emit } = useEventsBus()

    const state = reactive({
      Topic_list: [],
      Topic: Object.assign({}, Topic_blank),
      name_list:[],
      amount_list:[]
    });


    const getTopic = () => {
      axios.get(base_url).then(res => {
        const name=[];
        const amount=[];
        state.Topic_list = res.data.topics;
        state.name_list=state.Topic_list.name
        state.Topic = Object.assign({}, Topic_blank);
        state.Topic_list.forEach(element => {
         name.push(element.name)
         amount.push(element.amount)
        }); 
         state.name_list=name;
         state.amount_list=amount;
          

        console.log(state.amount_list);
      console.log(state.name_list);
      }).catch(err => {
        console.log(err);
      })
    };

    const selectT = (text) => {
      emit('selectedtopic', text)

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
   <div style="position: fixed; right: 20px; left: 65%">
      <BarChart :chart-data="{
        labels: name_list,
        datasets: [{
          label: 'Tweets Amount',
          backgroundColor: '#f87979',
          data: amount_list
        }]
      }" />
    </div>
  <div class="row">
    <div class="row mb-12" style="min-width: 250%;max-width: 265px;">
      <div class="col-lg-12 ">
        <div class="card">
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
              <div>
                <ol>
                  <li v-for="item in Topic_list" :key="item.url" @click="selectT(item.name)"
                    class="alert alert-primary alert-dismissible text-white">
                       {{item.rank}}. {{ item.name }}
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

