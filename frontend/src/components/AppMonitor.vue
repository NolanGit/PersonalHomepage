<template>
  <section>
    <el-row type="flex" justify="center">
      <div>
        <div class="widget-label">APP</div>
      </div>
    </el-row>
    <el-carousel height="180px" trigger="click" interval="5000" indicator-position="outside">
      <el-carousel-item v-for="weather in tableData" :key="weather">
        <el-table :data="tableData" style="width: 100%" size="mini">
          <el-table-column prop="date" label="日期" width="180"></el-table-column>
          <el-table-column prop="name" label="姓名" width="180"></el-table-column>
          <el-table-column prop="address" label="地址"></el-table-column>
        </el-table>
      </el-carousel-item>
    </el-carousel>
    <el-row type="flex" justify="center" class="margin-top-medium">
      <el-button
        class="margin_left-mini margin_right-mini"
        size="small"
        @click="bookmarksOptionButtonAddClicked()"
        icon="el-icon-plus"
        circle
      ></el-button>
      <el-button
        class="bmargin_left-mini margin_right-mini"
        size="small"
        @click="bookmarksOptionButtonSettingClicked()"
        icon="el-icon-setting"
        circle
      ></el-button>
    </el-row>
  </section>
</template>

<script>
import axios from "axios";
const api = {
  get: "/app/get",
  add: "/app/add",
  edit: "/app/edit"
};
export default {
  name: "AppMonitor",
  components: {},
  data() {
    return {
      tableData: [
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄"
        },
        {
          date: "2016-05-04",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1517 弄"
        },
        {
          date: "2016-05-01",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1519 弄"
        },
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄"
        },
      ]
    };
  },
  methods: {},
  mounted() {}
};
</script>

<style scoped>
.noMargin {
  margin: 0;
}
</style>