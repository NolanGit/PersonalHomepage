<template>
  <div class="gold-main">
    <el-main class="noPadding" style="height: 300px">
      <el-row type="flex" justify="center">
        <div class="widget-label">黄金价格</div>
      </el-row>
      <ve-line
        height="228px"
        :settings="chartSettings"
        :data="chartData"
        ref="chart"
        :legend-visible="false"
      ></ve-line>
    </el-main>
    <el-footer
      height="31px"
      style="justify-content: center; display: flex"
      v-if="user_id != 0"
    >
      <WidgetButton
        :user_id="user_id"
        :widget_id="widget_id"
        :buttons="buttons"
        @add="add()"
        @sort="sort()"
        @notify="notify()"
        @setting="setting()"
      ></WidgetButton>
    </el-footer>

    <el-dialog title="提醒" :visible.sync="notifyVisible" width="40%">
      <PushEdit
        :user_id="user_id"
        :widget_id="widget_id"
        v-if="notifyVisible"
        @done="notify()"
      ></PushEdit>
    </el-dialog>

    <!--编辑界面-->
    <el-dialog
      title="修改提醒阈值"
      :visible.sync="settingForm.visible"
      width="40%"
    >
      <el-form ref="form" :model="settingForm" size="mini">
        <el-form-item label="当价格不在此范围内时提醒我">
          <div class="div-flex">
            <el-input
              size="mini"
              v-model="settingForm.pushThresholdMin"
              placeholder="最小值"
            ></el-input
            >~
            <el-input
              size="mini"
              v-model="settingForm.pushThresholdMax"
              placeholder="最大值"
            ></el-input>
          </div>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" @click="settingConfirm()"
          >确定</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>
<script>
import axios from "axios";
import WidgetButton from "../common/WidgetButton.vue";
import PushEdit from "../common/PushEdit.vue";

const api = {
  get: "/gold/get",
  edit: "/gold/edit",
};

export default {
  name: "gold",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
    flush: Number,
  },
  components: {
    WidgetButton,
    PushEdit,
  },
  watch: {},
  data() {
    this.chartSettings = {
      min: ["dataMin"],
      max: ["dataMax"],
    };
    return {
      name: "黄金价格",
      chartData: {
        columns: [],
        rows: [],
      },
      notifyVisible: false,
      settingForm: {
        visible: false,
        pushThresholdMin: 0,
        pushThresholdMax: 0,
      },
    };
  },
  methods: {
    notify() {
      this.notifyVisible = !this.notifyVisible;
    },
    setting() {
      this.settingForm.visible = true;
    },
    async settingConfirm() {
      try {
        const { data: res } = await axios.post(api.edit, {
          user_id: this.user_id,
          threshold_min: this.settingForm.pushThresholdMin,
          threshold_max: this.settingForm.pushThresholdMax,
        });
        this.$message({
          message: res.msg,
          type: "success",
        });
        this.goldPriceGet();
        this.settingForm.visible = false;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async goldPriceGet() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
        });
        this.chartData.rows = [];
        this.chartData.columns = ["日期", "价格"];
        for (let x = 0; x < res.data.price_list.length; x++) {
          this.chartData.rows.push({
            日期: res.data.price_list[x]["update_time"],
            价格: res.data.price_list[x]["price"],
          });
        }
        this.$nextTick((_) => {
          this.$refs[`chart`].echarts.resize();
        });
        if (res.data.threshold.length != 0) {
          this.settingForm.pushThresholdMin = res.data.threshold[0];
          this.settingForm.pushThresholdMax = res.data.threshold[1];
        }
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
  },
  mounted() {
    this.goldPriceGet();
    this.timer = window.setInterval(this.goldPriceGet, this.flush);
  },
  beforeDestroy() {
    window.clearInterval(this.timer);
  },
};
</script>
</style>
