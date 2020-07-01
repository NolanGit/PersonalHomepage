<template>
  <LineChart></LineChart>
</template>
<script>
import axios from "axios";
import LineChart from "./common/LineChart.vue";
import WidgetButton from "./common/WidgetButton.vue";

const api = {
  goldData: "/gold/get"
};

export default {
  name: "gold",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
    flush: Boolean
  },
  components: {
    WidgetButton,
    LineChart
  },
  watch: {
    flush(newVal, oldVal) {
      if (newVal) {
        this.weatherData();
      }
    }
  },
  data() {},
  methods: {},
  created() {},
  mounted() {}
};
</script>
</style>
