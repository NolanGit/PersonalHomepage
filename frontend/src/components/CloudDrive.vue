<template>
  <el-col>
    <el-row class="margin_bottom-large">
      <div class="margin_left-medium margin_right-medium" style="text-align: center;">
        <el-upload
          class="upload-demo"
          style="text-align: center;"
          drag
          action="/upload"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :on-progress="uploadProgress"
          :on-success="uploadSuccess"
          :before-remove="beforeRemove"
          :before-upload="beforeUpload"
          multiple
          :limit="3"
          :on-exceed="handleExceed"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">
            将文件拖到此处，或
            <em>点击上传</em>
          </div>
        </el-upload>
      </div>
    </el-row>
    <el-row>
      <div class="margin_left-medium margin_right-medium">
        <el-table :data="tableData" style="text-align: center;" size="small">
          <el-table-column prop="file_name" label="文件名称"></el-table-column>
          <el-table-column prop="update_time" label="上传时间"></el-table-column>
          <el-table-column :key="Math.random()" label="操作" width="150">
            <template slot-scope="scope">
              <el-button
                class="noMargin"
                size="mini"
                plain
                type="primary"
                @click="download(scope.row.file_id)"
              >下载</el-button>
              <el-button
                class="noMargin"
                size="mini"
                plain
                type="danger"
                @click="del(scope.row.id)"
              >删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          class="margin_top-medium"
          @size-change="paginationSizeChange"
          @current-change="paginationCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 20, 30]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          style="text-align:center"
        ></el-pagination>
      </div>
    </el-row>
  </el-col>
</template>
<script>
import axios from "axios";
import { Loading } from "element-ui";

const FLUSH_INTERVAL = 60000;
const api = {
  download: "/download",
  get: "/cloudDrive/get",
  save: "/cloudDrive/save",
  delete: "/cloudDrive/delete"
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
      tableData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      }
    };
  },
  methods: {
    paginationCurrentChange(currentPage) {
      this.pagination.currentPage = currentPage;
      this.get();
    },
    paginationSizeChange(pageSize) {
      this.pagination.pageSize = pageSize;
      this.get();
    },
    uploadSuccess(response, file, fileList) {
      this.save(response.data.id);
      let loadingInstance = Loading.service({ fullscreen: true });
      this.$nextTick(() => {
        // 以服务的方式调用的 Loading 需要异步关闭
        loadingInstance.close();
      });
    },
    uploadProgress() {
      let loadingInstance = Loading.service({ fullscreen: true });
    },
    async get() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
          pagination_size: this.pagination.pageSize,
          current_page: this.pagination.currentPage
        });
        this.tableData = res.data.list;
        this.pagination.total = res.data.total;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async save(file_id) {
      try {
        const { data: res } = await axios.post(api.save, {
          user_id: this.user_id,
          file_id: file_id
        });
        this.$message({
          message: res.msg,
          type: "success"
        });
        this.get();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async download(fileId) {
      try {
        var elemIF = document.createElement("iframe");
        elemIF.src = "/download?file_id=" + fileId;
        elemIF.style.display = "none";
        document.body.appendChild(elemIF);
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async del(row_id) {
      this.$confirm("确认删除吗？", "提示", {}).then(async () => {
        try {
          const { data: res } = await axios.post(api.delete, {
            user_id: this.user_id,
            id: row_id
          });
          this.$message({
            message: res.msg,
            type: "success"
          });
          this.get();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      });
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
