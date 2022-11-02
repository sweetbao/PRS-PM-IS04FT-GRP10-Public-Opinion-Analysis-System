<script>
import { Line } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: 'LineChart',
  components: { Line },
  props: {
    chartData: {
        type: Object,
        required: true
      },
    chartOptions: {
      type: Object,
      default: () => {}
    }
  },

 
}
</script>


<template>
    <div class="table-resonsive">
      <Line :chart-data="chartData" :chart-options="chartOptions" />
    </div>
</template>



