<template>
  <ve-line :data="chartData" ref="chart" :legend-visible="false"></ve-line>
</template>
<script>
import axios from "axios";
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
    WidgetButton
  },
  watch: {
    flush(newVal, oldVal) {
      if (newVal) {
        this.$nextTick(_ => {
          this.$refs[`chart`].echarts.resize();
        });
      }
    }
  },
  data() {
    return {
      name: "黄金价格",
      chartData: {
        columns: [],
        rows: []
      }
    };
  },
  methods: {
    async goldPriceGet() {
      try {
        const { data: res } = await axios.post(api.goldData);
        this.chartData.rows = [];
        this.chartData.columns = ["日期", "价格"];
        for (let x = 0; x < res.data.length; x++) {
          this.chartData.rows.push({
            "日期": res.data[x]["update_time"],
            "价格": res.data[x]["price"]
          });
        }
        this.flush = true;
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
