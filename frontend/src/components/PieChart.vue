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

    <div class="row mb-4" style="position: fixed;width:fit-content;margin-left: 3%; ">
        <div class="col-lg-12 col-md-6 mb-md-0 mb-2">
          <div class="card" >
            <div class="card-header pb-0">
              <div class="row">
                <div class="col-lg-6 col-7">
                  <h6>Topic Emotion</h6>
                  <p class="text-sm mb-0">
                    <span class="font-weight-bold ms-1">See the public altitudes</span>
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
      <Pie :chart-data="chartData" :chart-options="chartOptions" /> 
      </div>
              </div>
            </div>
              </div>
            </div>



</template>