<script>
import axios from 'axios'
import { reactive, onMounted, toRefs, watch } from 'vue'
import useEventsBus from "./eventbus"
import PieChart from './PieChart.vue'
import LineChart from './LineChart.vue'
import Topic from './Topic.vue'



export default {
  name: "Tweets",
  components: {
    PieChart,
    LineChart,
    Topic
  },
  setup() {
    let base_url = "http://127.0.0.1:8000/api/Tweets/";
    const TE_blank = { url: "", title: "", author: "", comment: "", attitude: 0, topic: "" };
    const state = reactive({
      Tweet_list: [],
      Tweet: Object.assign({}, TE_blank),
      text: "",
      testNumber: 0,
    });
    const getTweet = () => {
      axios.get(base_url + "?title=" + state.text).then(res => {
        state.Tweet_list = res.data;
        state.testNumber = state.Tweet_list[0].attitude;
        state.Tweet = Object.assign({}, TE_blank);
      }).catch(err => {
        console.log(err);
      });
    };

    const { bus } = useEventsBus()

    watch(() => bus.value.get('selectedtopic'), (text) => {
      // destruct the parameters
      state.text = text;
      getTweet();
    })


    const editTE = (item) => {
      state.Tweet.url = item.url;
      state.Tweet.title = item.title;
      state.Tweet.author = item.author;
      state.Tweet.comment = item.comment;
      state.Tweet.attitude = item.attitude;
      state.Tweet.topic = item.topic;
    };

    const saveTE = () => {
      let newdata = {
        title: state.Tweet.title,
        author: state.Tweet.author,
        comment: state.Tweet.comment,
        attitude: state.Tweet.attitude,
        topic: state.Tweet.topic
      };
      if (state.Tweet.url == "") {
        axios.post(base_url, newdata).then(() => {
          getTweet();
        }).catch(err => {
          console.log(err);
        });
      }
      else {
        axios.put(state.Tweet.url, newdata).then(() => {
          getTweet();
        }).catch(err => {
          console.log(err);
        });
      }
    };

    const deleteTE = (item) => {
      axios.delete(item.url).then(() => {
        getTweet();
      }).catch(err => {
        console.log(err);
      });
    };

    const Assign = () => {
      getTweet();
    };

    const Clear = () => {
      state.text = "";
      getTweet();
    };

    onMounted(() => {
      getTweet();

    }
    );


    return {
      ...toRefs(state),
      editTE,
      saveTE,
      deleteTE,
      Assign,
      Clear
    };
  }
}

</script>

<template>
       <!-- search bar -->
            
       <div>
          <form class="d-flex" role="search" @submit.prevent="submitFunc">
            <keep-alive>
              <input class="form-control me-2" id="search" type="search" placeholder="Search for your interested topics" aria-label="Search" v-model="text">
            </keep-alive>
            <button class="btn btn-outline-success" type="submit" @click="Assign()">Search </button>
            <button class="btn btn-outline-info" type="submit" style="margin-left:10px" @click="Clear()">Clear</button>
      
          </form>
        </div>
        <!-- end search bar -->

        <div v-if="text===''" class="cocol-md-12"><Topic/></div> 
         <div class="row" v-else>
          <div class="row mb-12">
              <div class="col-lg-6 col-md-6 mb-md-0 mb-4">
                <div class="card">
                  <div class="card-header pb-0">
                    <div class="row">
                      <div class="col-lg-13 col-12">
                        <h6>The tweets related to this topic</h6>
                        <p class="text-sm mb-0">
                          <i class="fa fa-check text-info" aria-hidden="true"></i>
                          <span class="font-weight-bold ms-1">See the details</span>
                        </p>
                      </div>
                      <div class="col-lg-6 col-5 my-auto text-end">
                      </div>
                    </div>
                  </div>
                  <div class="card-body pb-2">

          <div class="table-resonsive cocol-md-10">
            <table class="table align-items-center mb-0">
              <thead>
                <tr>
                  <th>topic</th>
                  <th>author</th>
                  <th>content</th>
                  <th>attitude</th>
                  
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in Tweet_list" :key="item.url">
                  <td>{{item.title}}</td>
                  <td>{{item.author}}</td>
                  <td>{{item.comment}}</td>
                  <td>{{item.attitude}}</td>
                </tr>
              </tbody>
            </table>
          

            
        </div>
      
      </div>
      </div>
      </div>
  </div>
</div> 

      
    <div>
      <PieChart :chart-data="    
      {
        labels: [
          'Negative',
          'Neutral',
          'Positive'
        ],
        datasets: [
          {
            label: 'My First Dataset',
            data: [testNumber,30,20 ],
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
          }
        ]}" />
    </div>
    <div> <LineChart :chart-data=" {
        labels: [1, 2, 3, 4, 5, 6, 7],
        datasets: [
          {
            label: 'Positive',
            data: [10,20,30,40,50,60,70],
            borderColor:'rgb(255, 99, 132)',
            backgroundColor: 'rgb(255, 99, 132)',

          },
          {
            label: 'Neutral',
            data: [70,60,50,40,30,20,10],
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgb(255, 99, 132)',
          },
          {
            label: 'Negative',
            data: [25,25,25,25,25,25,25],
            borderColor: 'rgb(255, 205, 86)',
            backgroundColor: 'rgb(255, 205, 86)',
          }
        ]
      }" /></div>
  <!-- </div> -->
</template>

