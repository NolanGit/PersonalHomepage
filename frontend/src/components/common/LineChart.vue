<template>
  <v-chart :options="option" />
</template>
<script>
import ECharts from 'vue-echarts'
import 'echarts/lib/component/title'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/legend'
import 'echarts/lib/chart/line'

export default {
  name: "myLine",
  props: {
    name: String,
    xdata: Array,
    ydata: Array,
  },
  components: {
    'v-chart': ECharts
  },
  watch: {
    xdata(newVal, oldVal) {
      this.dataInit(newVal);
    },
    ydata(newVal, oldVal) {
      this.dataInit(newVal);
    }
  },
  data() {
    return {
      option: {
        title: {
          text: 'test',
          textStyle: {
            fontSize: 14
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: []
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          type: 'line',
          showSymbol: false,
          data: [],
          smooth: true,
          animationEasing: function (k) {
            if ((k *= 2) < 1) { return 0.5 * k * k * k; }
            return 0.5 * ((k -= 2) * k * k + 2);          }
        }],
        color: function (params) {
          var colorList = [
            '#C1232B', '#B5C334', '#FCCE10', '#E87C25', '#27727B',
            '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD',
            '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0',
            '#008080', '#DB7093', '#FFB5C5', '#AB82FF', '#4169E1',
            '#9370DB', '#32CD32', '#DAA520', '#A52A2A', '#8B4513',
            '#556B2F', '#808000', '#3CB371', '#008B8B', '#191970',
            '#5F9EA0', '#2F4F4F', '#2E8B57', '#FFA500', '#FA8072',
            '#8B008B', '#8B0000', '#00008B', '#363636', '#00688B',
            '#4A708B', '#473C8B', '#8B475D', '#FF4500', '#A0522D',
          ];
          return colorList[Math.round(Math.random() * 20)]
        }
      },
    };
  },
  methods: {
    dataInit(newVal) {
      this.option.title.text = this.name
      this.option.xAxis.data = this.xdata
      this.option.series[0].data = this.ydata
    }
  },
  mounted() {
    this.option.title.text = this.name
    this.option.xAxis.data = this.xdata
    this.option.series[0].data = this.ydata
  }
};
</script>
<style scoped>
.echarts {
  width: 100%;
  height: 100%;
}
</style>
