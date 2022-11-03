<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'BarChart',
  components: { Bar },
  props: {
    chartData: {
      type: Object,
      required: true
    },
    chartOptions: {
      type: Object,
      default: () => { }
    }
  }
}
</script>

<template>

  <div class="row mb-4" style="position: fixed;">
    <div class="col-lg-12 ">
      <div class="card">
        <div class="card-header pb-0">
          <div class="row">
            <div class="col-lg-10">
              <h6>Top topic tweets  </h6>
              <p class="text-sm mb-0">
                <span class="font-weight-bold ms-1">See the detail number</span>
              </p>
            </div>
            <div class="col-lg-6 col-5 my-auto text-end">
              <div class="dropdown float-lg-end pe-4">
              </div>
            </div>
          </div>
        </div>
        <div class="card-body px-0 pb-2">
          <div class="table-resonsive">
            <Bar :chart-data="chartData" :chart-options="chartOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>


</template>

