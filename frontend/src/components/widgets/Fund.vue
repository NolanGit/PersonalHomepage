<template>
  <div class="fund-main">
    <el-main class="noPadding" style="height: 300px">
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane
          v-for="data in fundData"
          :key="data"
          :label="data.name"
          :name="data.name"
        ></el-tab-pane>
      </el-tabs>
      <a
        class="better_font_style"
        style="width: 98%; font-size: 15px"
        v-if="chartData.rows.length == 0"
      >
        暂无数据
      </a>
      <span class="better_font_style" style="width: 98%; font-size: 15px">
        涨跌幅:
      </span>
      <span class="better_font_style" style="width: 98%; font-size: 15px">
        {{ latestRange }}
      </span>
      <ve-line
        height="230px"
        :settings="chartSettings"
        :data="chartData"
        ref="chart"
        :legend-visible="false"
        v-if="chartData.rows.length != 0"
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
      title="编辑基金"
      :visible.sync="fundSortEdit.visible"
      width="40%"
    >
      <SlickSort
        v-if="fundSortEdit.visible"
        :list="fundSortEdit.list"
        :can_be_edit="true"
        @submit="fundSortEditSubmit"
        @edit="fundSortEditSetting"
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
  get: "/fund/get",
  add: "/fund/add",
  check: "/fund/check",
  edit: "/fund/edit",
};

export default {
  name: "fund",
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
      fundData: [],
      chartData: {
        rows: [],
      },
      latestRange: 0,
      activeName: "",
      notifyVisible: false,
      edit: {
        title: "",
        name: "",
        visible: false,
        index: Number,
        code: "",
        push: false,
        min: 0,
        max: 0,
      },
      fundSortEdit: {
        visible: false,
        list: [],
      },
    };
  },
  methods: {
    add() {
      this.edit.title = "增加基金";
      this.edit.visible = true;
    },
    notify() {
      this.notifyVisible = true;
    },
    sort() {
      this.fundSortEdit.visible = true;
      this.fundSortEdit.list = deepClone(this.fundData);
    },
    fundSortEditSetting(item, index) {
      console.log(item);
      this.edit.title = "编辑基金";
      this.edit.code = item.code;
      this.edit.name = item.name;
      this.edit.push = item.push;
      this.edit.min = item.min;
      this.edit.max = item.max;
      this.edit.index = index;
      this.edit.visible = true;
    },
    editFormClose() {
      this.edit = {
        title: "",
        name: "",
        visible: false,
        index: Number,
        code: "",
        push: false,
        min: 0,
        max: 0,
      };
    },
    async fundSortEditSubmit(list) {
      for (let x = 0; x < list.length; x++) {
        list[x].push = list[x].push ? 1 : 0;
      }
      try {
        const { data: res } = await axios.post(api.edit, {
          user_id: this.user_id,
          funds: list,
        });
        this.$message({
          message: res["msg"],
          type: "success",
        });
        this.get();
        this.fundSortEdit.visible = false;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async editSubmit() {
      if (this.edit.title == "增加基金") {
        try {
          const { data: res } = await axios.post(api.add, {
            user_id: this.user_id,
            code: this.edit.code,
            name: this.edit.name,
            push: this.edit.push ? 1 : 0,
            threshold_max: this.edit.max,
            threshold_min: this.edit.min,
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
      } else if (this.edit.title == "编辑基金") {
        let index = this.edit.index;
        this.fundSortEdit.list[index].code = this.edit.code;
        this.fundSortEdit.list[index].name = this.edit.name;
        this.fundSortEdit.list[index].push = this.edit.push;
        this.fundSortEdit.list[index].min = this.edit.min;
        this.fundSortEdit.list[index].max = this.edit.max;
        this.edit.visible = false;
      }
    },
    // 检查是否合法
    async check() {
      try {
        const { data: res } = await axios.post(api.check, {
          code: this.edit.code,
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
      var temp = [];
      for (let x = 0; x < this.fundData.length; x++) {
        if (this.fundData[x].name == newVal) {
          for (let y = 0; y < this.fundData[x].price_list.length; y++) {
            temp.push({
              时间: this.fundData[x].price_list[y]["update_time"],
              价格: this.fundData[x].price_list[y]["price"],
            });
          }
          this.chartData = {
            columns: ["时间", "价格"],
            rows: temp,
          };

          var listLength = this.fundData[x].price_list.length;
          this.latestRange = this.fundData[x].price_list[listLength - 1].range;
          return;
        }
      }
    },
    async get() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
        });
        this.fundData = res.data;
        this.chartData = {};

        // 初始化基金推送阈值和
        for (let x = 0; x < this.fundData.length; x++) {
          this.fundData[x].push = this.fundData[x].push == 1 ? true : false;
          if (this.fundData[x] != null && this.fundData[x].length != 0) {
            this.fundData[x].min = this.fundData[x].push_threshold[0];
            this.fundData[x].max = this.fundData[x].push_threshold[1];
          }
        }

        // 初始化默认展示的基金
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

        // 初始化默认展示的基金
        var listLength = res.data[0].price_list.length;
        this.latestRange = res.data[0].price_list[listLength - 1].range;

        this.$nextTick((_) => {
          for (let x = 0; x < this.fundData.length; x++) {
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
      for (let x = 0; x < this.fundData.length; x++) {
        if (this.fundData[x].name == this.activeName) {
          if (x + 1 == this.fundData.length) {
            x = -1;
          }
          this.activeName = this.fundData[x + 1].name;
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
