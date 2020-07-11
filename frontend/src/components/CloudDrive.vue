<template>
  <el-col>
    <el-row class="margin_bottom-large">
      <el-upload class="upload" style="text-align: center;" drag action="/upload" multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
      </el-upload>
    </el-row>
    <el-row>
      <el-table :data="tableData" style="text-align: center;">
        <el-table-column prop="file_name" label="文件名称" width="180"></el-table-column>
        <el-table-column prop="update_time" label="上传时间" width="180"></el-table-column>
        <el-table-column :key="Math.random()" label="操作">
          <template slot-scope="scope">
            <el-button
              v-show="scope.row.is_valid==1"
              class="noMargin"
              size="mini"
              plain
              @click="roleDisable(scope.row.id)"
            >下载</el-button>
            <el-button
              v-show="scope.row.is_valid==1"
              class="noMargin"
              size="mini"
              plain
              type="danger"
              @click="roleDisable(scope.row.id)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </el-col>
</template>
<script>
import axios from "axios";

const FLUSH_INTERVAL = 60000;
const api = {
  get: "/cloudDrive/get",
  save: "/cloudDrive/save"
};

export default {
  name: "CloudDrive",
  props: {
    user_id: Number
  },
  components: {},
  watch: {},
  data() {
    return {
      tableData: []
    };
  },
  methods: {
    async get() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id
        });
        this.tableData = res.data;
        this.$message({
          message: res["msg"],
          type: "success"
        });
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
    this.get();
    this.timer = window.setInterval(this.get, FLUSH_INTERVAL);
  },
  beforeDestroy() {
    window.clearInterval(this.timer);
  }
};
</script>
</style>
