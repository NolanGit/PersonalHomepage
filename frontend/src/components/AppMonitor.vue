<template>
  <section>
    <el-main style="height: 315px; padding-bottom: 0px;">
      <el-row type="flex" justify="center">
        <div class="widget-label">APP</div>
      </el-row>
      <el-carousel height="180px" trigger="click" interval="5000" indicator-position="outside">
        <el-carousel-item v-for="appData in appSuite" :key="appData">
          <el-table :data="appData" style="width: 100%" size="mini">
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="price" label="当前价格" width="80"></el-table-column>
            <el-table-column prop="update_time" label="更新时间" width="180"></el-table-column>
          </el-table>
        </el-carousel-item>
      </el-carousel>
    </el-main>

    <el-footer style="justify-content: center; display: flex;" v-show="user_id != 0">
      <WidgetButton
        :user_id="user_id"
        :widget_id="widget_id"
        :buttons="buttons"
        @add="add()"
        @sort="sort()"
        @notify="notify()"
      ></WidgetButton>
    </el-footer>

    <!--编辑界面-->
    <el-dialog :title="edit.title" :visible.sync="edit.visible" width="40%">
      <el-form ref="form" :model="edit.form" size="mini">
        <el-form-item label="App名称">
          <div class="div-flex">
            <el-input size="small" v-model="edit.form.name" placeholder="名称"></el-input>
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
        <el-button type="primary" size="small" @click="editSubmit()">确定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="提醒" :visible.sync="notifyVisible" width="40%">
      <PushEdit :user_id="user_id" :widget_id="widget_id" v-if="notifyVisible" @done="notify()"></PushEdit>
    </el-dialog>

    <!--编辑顺序界面-->
    <el-dialog title="编辑App" :visible.sync="appSortEdit.visible" width="40%">
      <SlickSort
        v-if="appSortEdit.visible"
        :list="appSortEdit.list"
        :can_be_edit="true"
        @submit="appSortEditSubmit"
        @edit="appSortEditSetting"
      ></SlickSort>
    </el-dialog>
  </section>
</template>

<script>
import axios from "axios";
import SlickSort from "./common/SlickSort.vue";
import WidgetButton from "./common/WidgetButton.vue";
import PushEdit from "./common/PushEdit.vue";
import { deepClone } from "../js/common";
const api = {
  get: "/app/get",
  add: "/app/add",
  edit: "/app/edit",
};

export default {
  name: "AppMonitor",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
    flush: Boolean,
  },
  components: {
    SlickSort,
    WidgetButton,
    PushEdit,
  },
  watch: {
    flush(newVal, oldVal) {
      if (newVal) {
        this.appGet();
      }
    },
  },
  data() {
    return {
      appSortEdit: {
        visible: false,
        list: [],
      },
      notifyVisible: false,
      appRawData: [],
      appSuite: [],
      edit: {
        visible: false,
        title: "",
        form: {
          index: "",
          name: "",
          url: "",
          expect_price: 0,
        },
      },
    };
  },
  methods: {
    add() {
      this.edit.title = "新增App";
      this.edit.visible = true;
    },
    notify() {
      this.notifyVisible = !this.notifyVisible;
    },
    sort() {
      this.appSortEdit.visible = true;
      this.appSortEdit.list = deepClone(this.appRawData);
    },
    appSortEditSetting(item, index) {
      this.edit.title = "编辑App";
      this.edit.form.name = item.name;
      this.edit.form.url = item.url;
      this.edit.form.expect_price = item.expect_price;
      this.edit.form.index = index;
      this.edit.visible = true;
    },
    async appGet() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
        });
        this.appRawData = res.data;
        const STEP = 4; // 每页几行
        let temp = [];
        for (let x = 0; x < res.data.length; x += STEP) {
          temp.push([]);
          for (let y = 0; y < STEP; y++) {
            if (res.data[x + y] != undefined) {
              temp[temp.length - 1].push(res.data[x + y]);
            }
          }
        }
        this.appSuite = temp;
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async editSubmit() {
      if (this.edit.title == "新增App") {
        try {
          const { data: res } = await axios.post(api.add, {
            user_id: this.user_id,
            name: this.edit.form.name,
            url: this.edit.form.url,
            expect_price: this.edit.form.expect_price,
          });
          this.appGet();
          this.edit.visible = false;
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error",
          });
        }
      } else if ((this.edit.title = "编辑App")) {
        let index = this.edit.form.index;
        this.appSortEdit.list[index].name = this.edit.form.name;
        this.appSortEdit.list[index].url = this.edit.form.url;
        this.appSortEdit.list[index].expect_price = this.edit.form.expect_price;
        this.edit.visible = false;
      }
    },
    async appSortEditSubmit(list) {
      for (let x = 0; x < list.length; x++) {
        list[x].order = x + 1;
      }
      try {
        const { data: res } = await axios.post(api.edit, {
          apps: list,
          user_id: this.user_id,
        });
        this.$message({
          message: res["msg"],
          type: "success",
        });
        this.appSortEdit.visible = false;
        this.appGet();
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
    this.appGet();
    this.timer = window.setInterval(this.appGet, this.flush);
  },
  beforeDestroy() {
    window.clearInterval(this.timer);
  },
};
</script>

<style scoped>
.noMargin {
  margin: 0;
}
</style>