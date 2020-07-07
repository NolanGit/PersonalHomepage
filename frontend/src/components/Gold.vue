<template>
  <div class="gold-main">
    <el-row type="flex" justify="center">
      <div>
        <div class="widget-label">黄金价格</div>
      </div>
    </el-row>
    <ve-line
      height="250px"
      :settings="chartSettings"
      :data="chartData"
      ref="chart"
      :legend-visible="false"
    ></ve-line>
    <el-row type="flex" justify="center" v-show="user_id!=0">
      <WidgetButton
        :user_id="user_id"
        :widget_id="widget_id"
        :buttons="buttons"
        @add="add()"
        @sort="sort()"
        @notify="notify()"
      ></WidgetButton>
    </el-row>

    <el-dialog title="提醒" :visible.sync="notifyVisible" width="40%">
      <PushEdit :user_id="user_id" :widget_id="widget_id" v-if="notifyVisible" @done="notify()"></PushEdit>
    </el-dialog>
  </div>
</template>
<script>
import axios from "axios";
import WidgetButton from "./common/WidgetButton.vue";
import PushEdit from "./common/PushEdit.vue";

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
    PushEdit
  },
  watch: {
    flush(newVal, oldVal) {
      if (newVal) {
        this.goldPriceGet();
      }
    }
  },
  data() {
    this.chartSettings = {
      min: ["dataMin"],
      max: ["dataMax"]
    };
    return {
      name: "黄金价格",
      chartData: {
        columns: [],
        rows: []
      },
      notifyVisible: false
    };
  },
  methods: {
    notify() {
      this.notifyVisible = !this.notifyVisible;
    },
    async goldPriceGet() {
      try {
        const { data: res } = await axios.post(api.goldData);
        this.chartData.rows = [];
        this.chartData.columns = ["日期", "价格"];
        for (let x = 0; x < res.data.price_list.length; x++) {
          this.chartData.rows.push({
            日期: res.data.price_list[x]["update_time"],
            价格: res.data.price_list[x]["price"]
          });
        }
        this.$nextTick(_ => {
          this.$refs[`chart`].echarts.resize();
        });
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
