<template>
  <section>
    <el-row type="flex" justify="center">
      <div>
        <div class="widget-label">APP价格监控</div>
      </div>
    </el-row>
    <el-table :data="tableData" style="width: 100%" size="mini">
      <el-table-column prop="date" label="日期" width="180"></el-table-column>
      <el-table-column prop="name" label="姓名" width="180"></el-table-column>
      <el-table-column prop="address" label="地址"></el-table-column>
    </el-table>
    <el-pagination layout="prev, pager, next" :total="50"></el-pagination>
    <el-button
      class="bookmarks-option-button-add"
      size="small"
      @click="bookmarksOptionButtonAddClicked()"
      icon="el-icon-plus"
      circle
    ></el-button>
    <el-button
      class="bookmarks-option-button-edit-form"
      size="small"
      @click="bookmarksOptionButtonSettingClicked()"
      icon="el-icon-setting"
      circle
    ></el-button>
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
          date: "2016-05-03",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1516 弄"
        }
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