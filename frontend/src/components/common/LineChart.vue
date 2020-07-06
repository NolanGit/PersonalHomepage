<template>
  <ve-line :data="chartData" :legend-visible="false"></ve-line>
</template>
<script>
export default {
  name: "LineChart",
  props: {
    name: String,
    rows: Array,
    columns: Array
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
      chartData: {
        columns: [],
        rows: []
      }
    };
  },
  methods: {
    dataInit(newVal) {
      this.chartData.columns = this.columns;
      this.chartData.rows = this.rows;
    }
  },
  mounted() {
    this.chartData.columns = this.columns;
    this.chartData.rows = this.rows;
  }
};
</script>
<style scoped>
</style>
