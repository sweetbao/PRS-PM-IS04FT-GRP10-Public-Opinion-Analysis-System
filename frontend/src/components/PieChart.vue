<script>
import { Pie } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'


Chart.register(...registerables);

export default {
  name: 'PieChart',
  components: { Pie },
  props: {
    chartData: {
        type: Object,
        required: true
      },
    chartOptions: {
      type: Object,
      default: () => {}
    }
  }
 
  
}
</script>

<template>
  <Pie :chart-data="chartData" :chart-options="chartOptions" />
</template>