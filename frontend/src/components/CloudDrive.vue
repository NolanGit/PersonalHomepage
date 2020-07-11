<template>
  <el-row>
    <el-col>
      <el-upload
        class="upload-demo"
        drag
        action="https://jsonplaceholder.typicode.com/posts/"
        multiple
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
        <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
      </el-upload>
    </el-col>
    <el-col>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="date" label="日期" width="180"></el-table-column>
        <el-table-column prop="name" label="姓名" width="180"></el-table-column>
        <el-table-column prop="address" label="地址"></el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>
<script>
import axios from "axios";

const api = {
  get: "/cloudDrive/get",
  save: "/cloudDrive/save"
};

export default {
  name: "cloudDrive",
  props: {
    user_id: Number,
  },
  components: {},
  watch: {},
  data() {
    return {
      tableData: [
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄"
        }
      ]
    };
  },
  methods: {},
  mounted() {
    // this.goldPriceGet();
    // this.timer = window.setInterval(this.goldPriceGet, this.flush);
  },
  beforeDestroy() {
    // window.clearInterval(this.timer);
  }
};
</script>
</style>
