<script>
import axios from 'axios'
import { reactive, onMounted, toRefs, watch } from 'vue'
import  useEventsBus  from "./eventbus"





export default {
  name: "Tweets",

  setup() {
    let base_url = "http://127.0.0.1:8000/api/Tweets/";
    const TE_blank = { url: "", title: "", author: "", comment: "", attitude: ""  };
    const state = reactive({
      Tweet_list: [],
      Tweet: Object.assign({}, TE_blank),
      text: ""
    });
    const getTweet = () => {
      axios.get(base_url + "?title=" + state.text).then(res => {
        state.Tweet_list = res.data;
        state.Tweet = Object.assign({}, TE_blank);
      }).catch(err => {
        console.log(err);
      });
    };

    const { bus } = useEventsBus()

    watch(() => bus.value.get('selectedtopic'), (text) => {
      // destruct the parameters
       state.text=text;
       getTweet();
    })


    const editTE = (item) => {
      state.Tweet.url = item.url;
      state.Tweet.title = item.title;
      state.Tweet.author = item.author;
      state.Tweet.comment = item.comment;
      state.Tweet.attitude = item.attitude;
    };

    const saveTE = () => {
      let newdata = {
        title: state.Tweet.title,
        author: state.Tweet.author,
        comment: state.Tweet.comment,
        attitude: state.Tweet.attitude,
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
      state.text="";
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

  <div>
    <form class="d-flex" role="search" @submit.prevent="submitFunc">
      <keep-alive>
        <input class="form-control me-2" id="search" type="search" placeholder="Search" aria-label="Search"
          v-model="text">
      </keep-alive>
      <button class="btn btn-outline-success" type="submit" @click="Assign()">Search</button>
      <button class="btn btn-outline-info" type="submit" style="margin-left:10px" @click="Clear()">Clear</button>

    </form>
  </div>
  <div class="row">
    <div class="col-md-8">
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>topic</th>
            <th>author</th>
            <th>content</th>
            <th>attitude</th>
            <th>action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in Tweet_list" :key="item.url">
            <td>{{item.title}}</td>
            <td>{{item.author}}</td>
            <td>{{item.comment}}</td>
            <td>{{item.attitude}}</td>
            <td><button class="btn btn-success" tilte="edit" @click="editTE(item)" style="margin:0 10px ;">edit</button>
              <button class="btn btn-danger" title="delete" @click="deleteTE(item)">delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="col-md-4">
      <input type="hidden" v-model="Tweet.url">
      <div class="form-group">
        <label for="title">topic: </label>
        <input type="text" id="title" class="form-control" v-model="Tweet.title">
      </div>
      <div class="form-group">
        <label for="author">author: </label>
        <input type="text" id="author" class="form-control" v-model="Tweet.author">
      </div>
      <div class="form-group">
        <label for="comment">comment: </label>
        <textarea id="comment" rows="10" class="form-control" v-model="Tweet.comment"></textarea>
      </div>
      <div class="form-group">
        <label for="attitude">attitude: </label>
        <input id="attitude" class="form-control" v-model="Tweet.attitude">
      </div>
      <div class="form-group">
        <button class="btn btn-warning" @click="saveTE()">confirm</button>
      </div>
    </div>

  </div>
</template>

