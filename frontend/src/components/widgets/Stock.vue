<template>
  <div class="stock-main">
    <el-main class="noPadding" style="height: 300px">
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane
          v-for="data in stockData"
          :key="data"
          :label="data.name"
          :name="data.name"
        ></el-tab-pane>
      </el-tabs>
      <a
        class="better_font_style"
        style="width: 98%; font-size: 15px"
        v-show="chartData.rows.length == 0"
      >
        暂无数据
      </a>
      <div
        v-if="chartData.rows.length != 0"
        class="better_font_style"
        style="text-align: left; font-size: 12px"
      >
        <span class="margin_right-medium">{{
          "当前单价：" + latestUnitPrice
        }}</span>
        <span> 涨跌幅： </span>
        <span style="color: #f56c6c" v-if="latestRange > 0"> + </span>
        <span style="color: #f56c6c" v-if="latestRange > 0">
          {{ latestRange }}
        </span>
        <span style="color: #f56c6c" v-if="latestRange > 0"> % </span>
        <span style="color: #67c23a" v-if="latestRange <= 0">
          {{ latestRange }}
        </span>
        <span>
      </div>
      <ve-line
        height="215px"
        :settings="chartSettings"
        :data="chartData"
        ref="chart"
        :legend-visible="false"
        v-show="chartData.rows.length != 0"
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
      :title="edit.title"
      :visible.sync="edit.visible"
      width="40%"
      @close="editFormClose()"
    >
      <el-form ref="form" :model="edit.form" size="mini">
        <el-form-item label="代码">
          <div class="div-flex">
            <el-select
              v-model="edit.market"
              size="small"
              placeholder="请选择市场"
            >
              <el-option label="SH" value="1"> </el-option>
              <el-option label="SZ" value="2"> </el-option>
              <el-option label="HK" value="3"> </el-option>
              <el-option label="US" value="4"> </el-option>
            </el-select>
            <el-input
              size="small"
              v-model="edit.code"
              placeholder="代码"
            ></el-input>
            <el-button size="small" type="primary" plain @click="check()"
              >检查</el-button
            >
          </div>
        </el-form-item>
        <el-form-item label="名称">
          <div class="div-flex">
            <el-input
              size="small"
              v-model="edit.name"
              placeholder="名称"
            ></el-input>
          </div>
        </el-form-item>
        <el-form-item label="推送">
          <div class="div-flex">
            <el-switch style="margin-top: 3px" v-model="edit.push"> </el-switch>
          </div>
        </el-form-item>
        <el-form-item label="当价格不在此范围内时提醒我" v-if="edit.push">
          <div class="div-flex">
            <el-input
              size="mini"
              v-model="edit.threshold_min"
              placeholder="最小值"
            ></el-input
            >~
            <el-input
              size="mini"
              v-model="edit.threshold_max"
              placeholder="最大值"
            ></el-input>
          </div>
        </el-form-item>
        <p v-if="edit.push"
          class="warningInfo"
          style="font-size: 12px; color: #F56C6C; padding-top: 0px; margin-top: 0px; margin-bottom: 0px"
        >*设置推送阈值后，需要打开组件的推送总开关（组件下方的推送按钮）才可以正常推送。</p>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" @click="editSubmit()"
          >确定</el-button
        >
      </span>
    </el-dialog>

    <!--编辑顺序界面-->
    <el-dialog
      title="编辑股票"
      :visible.sync="stockSortEdit.visible"
      width="40%"
    >
      <SlickSort
        v-if="stockSortEdit.visible"
        :list="stockSortEdit.list"
        :can_be_edit="true"
        @submit="stockSortEditSubmit"
        @edit="stockSortEditSetting"
      ></SlickSort>
    </el-dialog>
  </div>
</template>
<script>
import axios from "axios";
import { deepClone } from "../../js/common";
import PushEdit from "../common/PushEdit.vue";
import SlickSort from "../common/SlickSort.vue";
import WidgetButton from "../common/WidgetButton.vue";

const api = {
  get: "/stock/get",
  add: "/stock/add",
  check: "/stock/check",
  edit: "/stock/edit",
};

export default {
  name: "stock",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
    flush: Number,
  },
  components: {
    PushEdit,
    SlickSort,
    WidgetButton,
  },
  watch: {
    activeName(newVal, oldVal) {
      this.activeTabChanged(newVal);
    },
  },
  data() {
    this.chartSettings = {
      min: ["dataMin"],
      max: ["dataMax"],
    };
    return {
      stockData: [],
      chartData: {
        rows: [],
      },
      latestRange: 0,
      latestUnitPrice: 0,
      activeName: "",
      notifyVisible: false,
      edit: {
        title: "",
        name: "",
        visible: false,
        index: Number,
        market: "1",
        code: "",
        push: false,
        min: 0,
        max: 0,
      },
      stockSortEdit: {
        visible: false,
        list: [],
      },
    };
  },
  methods: {
    add() {
      this.edit.title = "增加股票";
      this.edit.visible = true;
    },
    notify() {
      this.notifyVisible = !this.notifyVisible;
    },
    sort() {
      this.stockSortEdit.visible = true;
      this.stockSortEdit.list = deepClone(this.stockData);
    },
    stockSortEditSetting(item, index) {
      console.log(item);
      this.edit.title = "编辑股票";
      this.edit.market = item.market;
      this.edit.code = item.code;
      this.edit.name = item.name;
      this.edit.push = item.push;
      this.edit.threshold_min = item.threshold_min;
      this.edit.threshold_max = item.threshold_max;
      this.edit.index = index;
      this.edit.visible = true;
    },
    editFormClose() {
      this.edit = {
        title: "",
        name: "",
        visible: false,
        index: Number,
        market: "1",
        code: "",
        push: false,
        threshold_min: 0,
        threshold_max: 0,
      };
    },
    async stockSortEditSubmit(list) {
      for (let x = 0; x < list.length; x++) {
        list[x].push = list[x].push ? 1 : 0;
      }
      try {
        const { data: res } = await axios.post(api.edit, {
          user_id: this.user_id,
          stocks: list,
        });
        this.$message({
          message: res["msg"],
          type: "success",
        });
        this.get();
        this.stockSortEdit.visible = false;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async editSubmit() {
      if (this.edit.title == "增加股票") {
        try {
          const { data: res } = await axios.post(api.add, {
            user_id: this.user_id,
            code: this.edit.code,
            name: this.edit.name,
            market: this.edit.market,
            push: this.edit.push ? 1 : 0,
            threshold_max: this.edit.threshold_max,
            threshold_min: this.edit.threshold_min,
          });
          this.$message({
            message: res["msg"],
            type: "success",
          });
          this.get();
          this.edit.visible = false;
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error",
          });
        }
      } else if (this.edit.title == "编辑股票") {
        let index = this.edit.index;
        this.stockSortEdit.list[index].market = this.edit.market;
        this.stockSortEdit.list[index].code = this.edit.code;
        this.stockSortEdit.list[index].name = this.edit.name;
        this.stockSortEdit.list[index].push = this.edit.push;
        this.stockSortEdit.list[index].threshold_min = this.edit.threshold_min;
        this.stockSortEdit.list[index].threshold_max = this.edit.threshold_max;
        this.edit.visible = false;
      }
    },
    // 检查是否合法
    async check() {
      // 美股code应为小写
      if (this.edit.market == 4) {
        let temp = this.edit.code.search(/(([A-Z]([^A-Z]*)?))/g);
        if (temp != -1) {
          this.$message({
            message: "美股代码需为小写字母，已自动修改",
            type: "info",
          });
          this.edit.code = this.edit.code.toLowerCase();
        }
      }

      try {
        const { data: res } = await axios.post(api.check, {
          code: this.edit.code,
          market: this.edit.market,
        });
        if (res.data.name != "") {
          this.edit.name = res.data.name;
          this.$message({
            message: "校验成功!",
            type: "success",
          });
        } else {
          this.$message({
            message: "校验失败，请检查参数或联系管理员！",
            type: "error",
          });
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    activeTabChanged(newVal) {
      // 当触发的tab变化时，更新图表
      for (let x = 0; x < this.stockData.length; x++) {
        if (this.stockData[x].name == newVal) {
          var temp = [];
          for (let y = 0; y < this.stockData[x].price_list.length; y++) {
            temp.push({
              时间: this.stockData[x].price_list[y]["update_time"],
              价格: this.stockData[x].price_list[y]["price"],
            });
          }
          this.chartData = {
            columns: ["时间", "价格"],
            rows: temp,
          };
          if (this.stockData[x].price_list.length != 0) {
            var listLen = this.stockData[x].price_list.length;
            this.latestRange = this.stockData[x].price_list[listLen - 1].range;
            this.latestUnitPrice = this.stockData[x].price_list[
              listLen - 1
            ].price;
          }
          return;
        }
      }
    },
    async get() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
        });
        this.stockData = res.data;
        this.chartData = {};

        // 初始化股票推送阈值和市场code
        for (let x = 0; x < this.stockData.length; x++) {
          this.stockData[x].market = String(this.stockData[x].market);
          this.stockData[x].push = this.stockData[x].push == 1 ? true : false;
          if (this.stockData[x] != null && this.stockData[x].length != 0) {
            this.stockData[x].threshold_min = this.stockData[
              x
            ].push_threshold[0];
            this.stockData[x].threshold_max = this.stockData[
              x
            ].push_threshold[1];
          }
        }

        // 初始化默认展示的股票
        this.activeName = res.data[0].name;
        var temp = [];
        for (let y = 0; y < res.data[0].price_list.length; y++) {
          temp.push({
            时间: res.data[0].price_list[y]["update_time"],
            价格: res.data[0].price_list[y]["price"],
          });
        }
        this.chartData = {
          columns: ["时间", "价格"],
          rows: temp,
        };

        var listLen = res.data[0].price_list.length;
        this.latestRange = res.data[0].price_list[listLen - 1].range;
        this.latestUnitPrice = res.data[0].price_list[listLen - 1].price;

        this.$nextTick((_) => {
          for (let x = 0; x < this.stockData.length; x++) {
            this.$refs[`chart`].echarts.resize();
          }
        });
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    autoSwitch() {
      window.clearInterval(this.switchTimerStock);
      for (let x = 0; x < this.stockData.length; x++) {
        if (this.stockData[x].name == this.activeName) {
          if (x + 1 == this.stockData.length) {
            x = -1;
          }
          this.activeName = this.stockData[x + 1].name;
          break;
        }
      }
      this.switchTimerStock = window.setTimeout(this.autoSwitch, 10000);
    },
  },
  mounted() {
    this.get();
    this.switchTimerStock = window.setTimeout(this.autoSwitch, 10000);
    this.timer = window.setInterval(this.get, this.flush);
  },
  beforeDestroy() {
    window.clearInterval(this.timer);
  },
};
</script>
</style>
