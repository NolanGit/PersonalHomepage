<template>
  <LineChart :name="name" :xdata="xdata" :ydata="ydata"></LineChart>
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
  data() {
    return {
      name: "黄金价格",
      xdata: [],
      ydata: []
    };
  },
  methods: {
    async goldPriceGet() {
      try {
        const { data: res } = await axios.post(api.goldData);
        this.xdata = [];
        this.ydata = [];
        for (let x = 0; x < res.data.length; x++) {
          for (var key in res.data[x]) {
            this.xdata.push(key);
            this.ydata.push(raw[key]);
          }
        }
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    }
  },
  mounted() {
    this.goldPriceGet();
  }
};
</script>
</style>
