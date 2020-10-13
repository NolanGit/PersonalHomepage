<template>
  <div class="stock-main">
    <el-main
      v-for="(data, index) in chartData"
      :key="data"
      class="noPadding"
      style="height: 300px"
    >
      <el-row type="flex" justify="center">
        <div class="widget-label">{{ stockData[index].name }}</div>
      </el-row>
      <ve-line
        height="228px"
        :settings="chartSettings"
        :data="data"
        :ref="stockData[index].name"
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
      :title="edit.chooseFormTitle"
      :visible.sync="edit.chooseFormVisible"
      width="40%"
    >
      <el-form ref="form" :model="edit.form" size="mini">
        <el-form-item label="App名称">
          <div class="div-flex">
            <el-input
              size="small"
              v-model="edit.form.name"
              placeholder="名称"
            ></el-input>
          </div>
        </el-form-item>
        <el-form-item label="AppURL">
          <div class="div-flex">
            <el-input
              size="small"
              v-model="edit.form.url"
              placeholder="App Store链接(如：'https://apps.apple.com/cn/app/id958955657')"
            ></el-input>
          </div>
        </el-form-item>
        <el-form-item label="期望价格">
          <div class="div-flex">
            <el-input
              size="small"
              v-model="edit.form.expect_price"
              placeholder="当小于期望价格时，如果设置了通知，会发送提醒"
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
  watch: {},
  data() {
    this.chartSettings = {
      min: ["dataMin"],
      max: ["dataMax"],
    };
    return {
      stockData: [],
      chartData: [],
      notifyVisible: false,
      settingForm: {
        visible: false,
      },
      edit: {
        searchFormTitle: "",
        searchFormVisible: false,
        searchLoading: false,
        searchContent: "",
        searchArea: "cn",
        searchResultList: [],
        chooseFormVisible: false,
        chooseFormTitle: "",
        form: {
          index: "",
          name: "",
          url: "",
          expect_price: 0,
        },
      },
      stockSortEdit: {
        visible: false,
        list: [],
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
    async get() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
        });
        this.stockData = res.data;

        this.chartData = [];
        for (let x = 0; x < res.data.length; x++) {
          var temp = [];
          for (let y = 0; y < res.data[x].price_list.length; y++) {
            temp.push({
              时间: res.data[x].price_list[y]["update_time"],
              价格: res.data[x].price_list[y]["price"],
            });
          }
          this.chartData.push({
            columns: ["时间", "价格"],
            rows: temp,
          });
        }
        this.$nextTick((_) => {
          for (let x = 0; x < this.stockData.length; x++) {
            this.$refs[this.stockData[x].name].echarts.resize();
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
  },
  mounted() {
    this.get();
    this.timer = window.setInterval(this.goldPriceGet, this.flush);
  },
  beforeDestroy() {
    window.clearInterval(this.timer);
  },
};
</script>
</style>
