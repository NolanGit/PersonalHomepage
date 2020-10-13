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
      <ve-line
        height="230px"
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
    <el-dialog :title="edit.title" :visible.sync="edit.visible" width="40%">
      <el-form ref="form" :model="edit.form" size="mini">
        <el-form-item label="市场">
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
        <el-form-item label="当价格不在此范围内时提醒我">
          <div class="div-flex">
            <el-input
              size="mini"
              v-model="edit.min"
              placeholder="最小值"
            ></el-input
            >~
            <el-input
              size="mini"
              v-model="edit.max"
              placeholder="最大值"
            ></el-input>
          </div>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" @click="editSubmit()"
          >确定</el-button
        >
      </span>
    </el-dialog>

    <!--编辑顺序界面-->
    <el-dialog
      title="编辑App"
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
      chartData: {},
      activeName: "",
      notifyVisible: false,
      edit: {
        title: "",
        visible: false,
        index: Number,
        market: "1",
        code: "000001",
        min: 0,
        max: 1,
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
      this.notifyVisible = true;
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
      this.edit.min = item.min;
      this.edit.max = item.max;
      this.edit.index = index;
      this.edit.visible = true;
    },
    editSubmit() {
      if (this.edit.title == "增加股票") {
      } else if (this.edit.title == "编辑股票") {
        let index = this.edit.index;
        this.stockSortEdit.list[index].market = this.edit.market;
        this.stockSortEdit.list[index].code = this.edit.code;
        this.stockSortEdit.list[index].min = this.edit.min;
        this.stockSortEdit.list[index].max = this.edit.max;
        this.$message({
          message: res["msg"],
          type: "success",
        });
        this.edit.visible = false;
      }
    },
    check() {},
    activeTabChanged(newVal) {
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
        this.chartData = [];

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
      window.clearInterval(this.switchTimer);
      for (let x = 0; x < this.stockData.length; x++) {
        if (this.stockData[x].name == this.activeName) {
          if (x + 1 == this.stockData.length) {
            x = -1;
          }
          this.activeName = this.stockData[x + 1].name;
          break;
        }
      }
      this.switchTimer = window.setTimeout(this.autoSwitch, 10000);
    },
  },
  mounted() {
    this.get();
    this.switchTimer = window.setTimeout(this.autoSwitch, 10000);
    this.timer = window.setInterval(this.get, this.flush);
  },
  beforeDestroy() {
    window.clearInterval(this.timer);
  },
};
</script>
</style>
