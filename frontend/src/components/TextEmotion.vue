<script>
import axios from "axios";
import { reactive, onMounted, toRefs, watch } from "vue";
import useEventsBus from "./eventbus";
import PieChart from "./PieChart.vue";
import Topic from "./Topic.vue";

import Loading from "./Loading.vue";

export default {
  name: "Tweets",
  components: {
    PieChart,
    Topic,
    Loading
  },
  setup() {
    let base_url = "http://127.0.0.1:8000/";
    const Topic_blank = {
      rank: "",
      name: "",
      postive: Number,
      negative: Number,
      neutral: Number,
    };
    const state = reactive({
      Tweets_list: [],
      Topic: Object.assign({}, Topic_blank),
      Id: "",
      SearchText: "",
      text:""
    });



    const getTweetbyId = () => {
      axios
        .get(base_url + "tweets/" + state.Id)
        .then((res) => {
          state.Tweets_list = res.data.tweets;
          state.Topic.name = res.data.topic.name;
          state.Topic.rank = res.data.topic.rank;
          state.Topic.postive = Number(res.data.topic.positiveNumber);
          state.Topic.negative = Number(res.data.topic.negativeNumber);
          state.Topic.neutral = Number(res.data.topic.neutralNumber);
        })
        .catch((err) => {
          console.log(err);
        });
    };


    const getTweetbyText = () => {
      axios
        .get(base_url + "tweet/search/" + state.text)
        .then((res) => {
        
          state.Tweets_list = res.data.tweets;
          state.Topic.name = state.SearchText;
          state.Topic.postive = Number(res.data.prediction.positive);
          state.Topic.negative = Number(res.data.prediction.negative);
          state.Topic.neutral = Number(res.data.prediction.neutral);
   
        })
        .catch((err) => {
          console.log(err);
        });
    };



    const { bus,emit } = useEventsBus();

    watch(
      () => bus.value.get("selectedtopic"),

      (text) => {
    
        
        // destruct the parameters
        if (bus.value.get("ishot")[0]) {
          state.Tweets_list=[];
          state.Id = text;
          getTweetbyId();
        }
        else {
          state.Tweets_list=[];
          state.text=text;
          getTweetbyText();
        }
      }
    );



    const Assign = () => {
      emit('selectedtopic', state.SearchText)
      emit('ishot', false)
    };

    const Clear = () => {
      state.text = "";
      state.Id = "";
      state.SearchText=""
    };

    onMounted(() => {

    });

    return {
      ...toRefs(state),

      getTweetbyId,
      getTweetbyText,
      Assign,
      Clear,
    };
  },
};
</script>

<template>
  <!-- search bar -->

  <div style="width: 52%">
    <form class="d-flex form-wrapper" role="search" @submit.prevent="submitFunc">

      <input class="form-control me-2" id="search" type="text" placeholder="Search for your interested topics"
        aria-label="Search" v-model="SearchText" required />
      <small style="color:rebeccapurple;font-size: xx-small;" v-if="SearchText!=''">Hint: Long waits will result from unpopular topics.</small>
      <input class="btn btn-outline-success" type="submit" @click="Assign()" value="Search" id="submit">


    </form>
  </div>
  <!-- end search bar -->

  <div style="display: flex">
    <div v-if="Id === ''&& text===''">
      <Topic />
    </div>
    <div class="row" v-else>
      <div v-if="Tweets_list.length==0"><Loading/></div>
      <div style="display: flex" v-else>
        <div class="row" style="min-width: 200%; max-width: 350px;">
          <div class="">
            <div class="card">
              <div class="card-header pb-0">
                <div class="row">
                  <div class="col-lg-13 col-12">
                    <h6 style="display: flex; align-items: center;">
                      <a style="cursor: pointer;" @click="Clear()"> <i class="fa fa-toggle-left" title="Back"
                          style="margin-right:5px ;font-size:28px;color:red"></i></a>

                      The tweets related to <span style="margin-left: 5px;">{{ Topic.name }}</span> <img
                        icon="twitterlogo" src="./icons/twitterlogo.png" style="width: 5%;margin-left: 5px;" />
                    </h6>

                    <p class="text-sm mb-0">
                      <i class="fa fa-check text-info" aria-hidden="true"></i>
                      <span class="font-weight-bold ms-1">See the details</span>
                    </p>
                  </div>
                  <div class="col-lg-6 col-5 my-auto text-end"></div>
                </div>
              </div>
              <div class="card-body pb-2">
                <div class="table-resonsive cocol-md-10">
                  <table class="table align-items-center mb-0">
                    <thead>
                      <tr>
                        <th>Comment</th>
                     
                        <th>Attitude</th>
                      </tr>
                    </thead>
                    <tbody >

                        <tr v-for="item in Tweets_list">
                        <td>{{ item.comment }}</td>
                       
                        <td>{{ item.attitude }}</td>
                      </tr>

                    </tbody>
  
                  
                   
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div>
          <PieChart :chart-data="{
            labels: ['Negative', 'Neutral', 'Positive'],
            datasets: [
              {
                label: 'My First Dataset',
                data: [(Topic.negative / (Topic.negative + Topic.neutral + Topic.postive)).toFixed(3),
                (Topic.neutral / (Topic.negative + Topic.neutral + Topic.postive)).toFixed(3),
                (Topic.postive / (Topic.negative + Topic.neutral + Topic.postive)).toFixed(3)],
                backgroundColor: [
                  'rgb(255, 99, 132)',
                  'rgb(54, 162, 235)',
                  'rgb(255, 205, 86)',
                ],
                hoverOffset: 4,
              },
            ],
          }" />
        </div>
      </div>
    </div>
   
  </div>


</template>


<style>
.form-wrapper {
  background-color: #f6f6f6;
  background-image: -webkit-gradient(linear, left top, left bottom, from(#f6f6f6), to(#eae8e8));
  background-image: -webkit-linear-gradient(top, #f6f6f6, #eae8e8);
  background-image: -moz-linear-gradient(top, #f6f6f6, #eae8e8);
  background-image: -ms-linear-gradient(top, #f6f6f6, #eae8e8);
  background-image: -o-linear-gradient(top, #f6f6f6, #eae8e8);
  background-image: linear-gradient(top, #f6f6f6, #eae8e8);
  border-color: #dedede #bababa #aaa #bababa;
  border-style: solid;
  border-width: 1px;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  border-radius: 10px;
  -webkit-box-shadow: 0 3px 3px rgba(255, 255, 255, .1), 0 3px 0 #bbb, 0 4px 0 #aaa, 0 5px 5px #444;
  -moz-box-shadow: 0 3px 3px rgba(255, 255, 255, .1), 0 3px 0 #bbb, 0 4px 0 #aaa, 0 5px 5px #444;
  box-shadow: 0 3px 3px rgba(255, 255, 255, .1), 0 3px 0 #bbb, 0 4px 0 #aaa, 0 5px 5px #444;
  margin-top: 15px;
  margin-bottom: 10px;
  overflow: hidden;
  padding: 8px;
}

.form-wrapper #search {
  border: 1px solid #CCC;
  -webkit-box-shadow: 0 1px 1px #ddd inset, 0 1px 0 #FFF;
  -moz-box-shadow: 0 1px 1px #ddd inset, 0 1px 0 #FFF;
  box-shadow: 0 1px 1px #ddd inset, 0 1px 0 #FFF;
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
  color: rgb(0, 0, 0);
  float: left;
  font: 16px Lucida Sans, Trebuchet MS, Tahoma, sans-serif;
  height: 41px;
  padding: 10px;
  width: 75%;
}

.form-wrapper #search:focus {
  border-color: #aaa;
  -webkit-box-shadow: 0 1px 1px #bbb inset;
  -moz-box-shadow: 0 1px 1px #bbb inset;
  box-shadow: 0 1px 1px #bbb inset;
  outline: 0;
}

.form-wrapper #search:-moz-placeholder,
.form-wrapper #search:-ms-input-placeholder,
.form-wrapper #search::-webkit-input-placeholder {
  color: #999;
  font-weight: normal;
}

.form-wrapper #submit {
  background-color: #0483a0;
  background-image: -webkit-gradient(linear, left top, left bottom, from(#31b2c3), to(#0483a0));
  background-image: -webkit-linear-gradient(top, #31b2c3, #0483a0);
  background-image: -moz-linear-gradient(top, #31b2c3, #0483a0);
  background-image: -ms-linear-gradient(top, #31b2c3, #0483a0);
  background-image: -o-linear-gradient(top, #31b2c3, #0483a0);
  background-image: linear-gradient(top, #31b2c3, #0483a0);
  border: 1px solid #00748f;
  -moz-border-radius: 3px;
  -webkit-border-radius: 3px;
  border-radius: 3px;
  -webkit-box-shadow: 0 1px 0 rgba(255, 255, 255, 0.3) inset, 0 1px 0 #FFF;
  -moz-box-shadow: 0 1px 0 rgba(255, 255, 255, 0.3) inset, 0 1px 0 #FFF;
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.3) inset, 0 1px 0 #FFF;
  color: #fafafa;
  cursor: pointer;
  height: 42px;
  float: right;
  font: 15px Arial, Helvetica;
  padding: 3px;
  text-transform: uppercase;
  text-shadow: 0 1px 0 rgba(0, 0, 0, .3);
  width: 20%;
}

.form-wrapper #submit:hover,
.form-wrapper #submit:focus {
  background-color: #31b2c3;
  background-image: -webkit-gradient(linear, left top, left bottom, from(#0483a0), to(#31b2c3));
  background-image: -webkit-linear-gradient(top, #0483a0, #31b2c3);
  background-image: -moz-linear-gradient(top, #0483a0, #31b2c3);
  background-image: -ms-linear-gradient(top, #0483a0, #31b2c3);
  background-image: -o-linear-gradient(top, #0483a0, #31b2c3);
  background-image: linear-gradient(top, #0483a0, #31b2c3);
}

.form-wrapper #submit:active {
  -webkit-box-shadow: 0 1px 4px rgba(0, 0, 0, 0.5) inset;
  -moz-box-shadow: 0 1px 4px rgba(0, 0, 0, 0.5) inset;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.5) inset;
  outline: 0;
}

.form-wrapper #submit::-moz-focus-inner {
  border: 0;
}
</style>