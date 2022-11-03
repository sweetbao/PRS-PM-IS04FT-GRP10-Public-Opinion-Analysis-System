import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
import TopicView from '../views/TopicView.vue'
import HistoryView from '../views/HistoryView.vue'


const routes = [
  {
    path: "/",
    name: "Home",
    component: TopicView,
  },
  {
    path: "/History/",
    name: "history",
    component: HistoryView
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;