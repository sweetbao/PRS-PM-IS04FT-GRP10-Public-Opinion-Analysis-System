<script>
import axios from 'axios'
import { reactive, onMounted, toRefs ,ref } from 'vue'







export default {
  name: 'TextEmotion',

 

  setup() {
    let base_url = "http://127.0.0.1:8000/api/TextEmotion/";
    const TE_blank = { url: '', title: '', author: '', comment: '' }
  
    

    const state = reactive({
      TE_list: [],
      TextEmotion: Object.assign({}, TE_blank),
      
      text:""
    });


    const getTextEmotion = () => {
        axios.get(base_url+"?title="+state.text).then(res => {
        state.TE_list = res.data;
        state.TextEmotion = Object.assign({}, TE_blank)
      }).catch(err => {
        console.log(err);
      })
    };
    

    const editTE = (item) => {
      state.TextEmotion.url = item.url;
      state.TextEmotion.title = item.title;
      state.TextEmotion.author = item.author;
      state.TextEmotion.comment = item.comment;
    };

    const saveTE = () => {
      let newdata = {
        title: state.TextEmotion.title,
        author: state.TextEmotion.author,
        comment: state.TextEmotion.comment
      }

      if (state.TextEmotion.url == "") {
        axios.post(base_url, newdata).then(() => {
          getTextEmotion();
        }).catch(err => {
          console.log(err)
        })
      }
      else {
        axios.put(state.TextEmotion.url, newdata).then(() => {
          getTextEmotion();
        }).catch(err => {
          console.log(err)
        })
      }
    };

    const deleteTE = (item) => {
      axios.delete(item.url).then(() => {
        getTextEmotion();
      }).catch(err => {
        console.log(err)
      })
    };

   
    const Assign = () => {
     
      getTextEmotion()
    };
  


    onMounted(() => {
      getTextEmotion()
    });

    return {
      ...toRefs(state),
      editTE,
      saveTE,
      deleteTE,
      Assign,
    }


  }
}

</script>

<template>
  <div>
    <form class="d-flex" role="search"  @submit.prevent="submitFunc">
    <keep-alive>
      <input class="form-control me-2" id="search" type="search" placeholder="Search" aria-label="Search"  v-model="text">
    </keep-alive>
      <button class="btn btn-outline-success" type="submit" @click="Assign()" >Search</button>
   
    </form>
  </div>
    <div>{{text}}</div>
  <div class="row">
    <div class="col-md-8">
      <table class="table table-bordered" >
        <thead>
          <tr>
            <th>title</th>
            <th>author</th>
            <th>content</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in TE_list" :key="item.url">
            <td>{{item.title}}</td>
            <td>{{item.author}}</td>
            <td>{{item.comment}}</td>
            <td><button class="btn btn-success" tilte="edit" @click="editTE(item)" style="margin:0 10px ;">edit</button>
              <button class="btn btn-danger" title="delete" @click="deleteTE(item)">delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="col-md-4">
      <input type="hidden" v-model="TextEmotion.url">
      <div class="form-group">
        <label for="title">title: </label>
        <input type="text" id="title" class="form-control" v-model="TextEmotion.title">
      </div>
      <div class="form-group">
        <label for="author">author: </label>
        <input type="text" id="author" class="form-control" v-model="TextEmotion.author">
      </div>
      <div class="form-group">
        <label for="comment">comment: </label>
        <textarea id="comment" rows="10" class="form-control" v-model="TextEmotion.comment"></textarea>
      </div>
      <div class="form-group">
        <button class="btn btn-warning" @click="saveTE()">confirm</button>
      </div>
    </div>
  </div>
</template>

