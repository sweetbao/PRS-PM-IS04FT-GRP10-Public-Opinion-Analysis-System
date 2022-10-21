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
  <div v-if="text===''" class="cocol-md-2"><Topic/></div> 
    <div class="row" v-else>
    <div class="row mb-4">
        <div class="col-lg-12 col-md-6 mb-md-1 mb-4">
          <div class="card">
            <div class="card-header pb-0">
              <div class="row">
                <div class="col-lg-6 col-7">
                  <h6>Projects</h6>
                  <p class="text-sm mb-0">
                    <i class="fa fa-check text-info" aria-hidden="true"></i>
                    <span class="font-weight-bold ms-1">30 done</span> this month
                  </p>
                </div>
                <div class="col-lg-6 col-5 my-auto text-end">
                  <div class="dropdown float-lg-end pe-4">
                    <a class="cursor-pointer" id="dropdownTable" data-bs-toggle="dropdown" aria-expanded="false">
                      <i class="fa fa-ellipsis-v text-secondary"></i>
                    </a>
                    <ul class="dropdown-menu px-2 py-3 ms-sm-n4 ms-n5" aria-labelledby="dropdownTable">
                      <li><a class="dropdown-item border-radius-md" href="javascript:;">Action</a></li>
                      <li><a class="dropdown-item border-radius-md" href="javascript:;">Another action</a></li>
                      <li><a class="dropdown-item border-radius-md" href="javascript:;">Something else here</a></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-body px-0 pb-2">
    <div class="table-resonsive">
      <Line :chart-data="chartData" :chart-options="chartOptions" />
      </div>
              </div>
            </div>
              </div>
            </div>
          </div>

</template>



