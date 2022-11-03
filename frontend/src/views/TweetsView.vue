<script>

import TextEmotion from '../components/TextEmotion.vue'
import PieChart from '../components/PieChart.vue'

export default {
    name: 'TopicView',
    components: {
        TextEmotion,
        PieChart
    }

  }

</script>

<template>
  <main>
    <TextEmotion />
    <PieChart/>
  </main>
</template>
