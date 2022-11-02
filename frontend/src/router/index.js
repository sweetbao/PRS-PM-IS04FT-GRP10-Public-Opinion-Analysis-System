import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
import TopicView from '../views/TopicView.vue'
import TweetsView from '../views/TweetsView.vue'


const routes = [
  {
    path: "/",
    name: "Home",
    component: TopicView,
  },
  {
    path: "/Tweets/",
    name: "Tweets",
    component: TweetsView
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;