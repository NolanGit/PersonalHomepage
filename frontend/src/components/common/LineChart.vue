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
    rows(newVal, oldVal) {
      this.dataInit(newVal);
    },
    columns(newVal, oldVal) {
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
  }
};
</script>
<style scoped>
</style>
