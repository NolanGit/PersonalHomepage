<template>
  <LineChart :name="name" :rows="rows" :columns="columns"></LineChart>
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
      rows: [],
      columns: []
    };
  },
  methods: {
    async goldPriceGet() {
      try {
        const { data: res } = await axios.post(api.goldData);
        this.rows = [];
        this.columns = ["日期", "价格"];
        for (let x = 0; x < res.data.length; x++) {
          this.rows.push({
            "日期": res.data[x]["update_time"],
            "价格": res.data[x]["price"]
          });
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
