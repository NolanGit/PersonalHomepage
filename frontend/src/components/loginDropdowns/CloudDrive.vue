<template>
  <section>
    <el-row class="margin_bottom-large">
      <div
        class="margin_left-medium margin_right-medium"
        style="text-align: center"
      >
        <el-upload
          class="upload-demo"
          ref="upload"
          style="text-align: center"
          drag
          action="/upload"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :on-progress="uploadProgress"
          :on-success="uploadSuccess"
          :before-remove="beforeRemove"
          :before-upload="beforeUpload"
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
        <div
          class="scrollbar-div"
          style="max-height: calc(100vh - 435px); height: calc(100vh - 435px)"
        >
          <el-table :data="tableData" style="text-align: center" size="small">
            <el-table-column label="名称">
              <template slot-scope="scope">
                <div style="display: inline-flex">
                  <span
                    v-if="scope.row.editMode == false"
                    style="margin-right: 10px"
                    >{{ scope.row.file_name }}</span
                  >
                  <i
                    v-if="scope.row.editMode == false"
                    class="el-icon-edit"
                    style="cursor: pointer; margin-top: 6px; font-size: 13px"
                    @click="changeEditMode(scope.row.id, 'enable')"
                  ></i>
                  <el-input
                    v-if="scope.row.editMode == true"
                    v-model="scope.row.file_name"
                    placeholder="请输入内容"
                    size="mini"
                  ></el-input>
                  <i
                    v-if="scope.row.editMode == true"
                    class="el-icon-check"
                    style="
                      cursor: pointer;
                      margin-top: 6px;
                      font-size: 13px;
                      color: #67c23a;
                      padding-left: 5px;
                    "
                    @click="
                      submitEditMode(
                        scope.row.id,
                        scope.row.file_id,
                        scope.row.file_name
                      )
                    "
                  ></i>
                  <i
                    v-if="scope.row.editMode == true"
                    class="el-icon-close"
                    style="
                      cursor: pointer;
                      margin-top: 6px;
                      font-size: 13px;
                      color: #f56c6c;
                      padding-left: 5px;
                    "
                    @click="changeEditMode(scope.row.id, 'disable')"
                  ></i>
                </div>
              </template>
            </el-table-column>
            <el-table-column
              prop="size"
              label="大小"
              width="100"
            ></el-table-column>
            <el-table-column
              prop="update_time"
              label="上传时间"
              width="170"
            ></el-table-column>
            <el-table-column label="操作" width="280">
              <template slot-scope="scope">
                <el-tooltip content="下载" placement="top">
                  <el-button
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    icon="el-icon-download"
                    @click="download(scope.row.file_id)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  v-if="scope.row.share == 0"
                  content="分享"
                  placement="top"
                >
                  <el-button
                    v-if="scope.row.share == 0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    icon="el-icon-share"
                    @click="share(scope.row.id)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  v-if="scope.row.share == 1"
                  content="复制分享链接"
                  placement="top"
                >
                  <el-button
                    v-if="scope.row.share == 1"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    icon="el-icon-link"
                    v-clipboard:copy="scope.row.share_link"
                    v-clipboard:success="onCopy"
                    v-clipboard:error="onError"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  v-if="scope.row.share == 1"
                  content="取消分享"
                  placement="top"
                >
                  <el-button
                    v-if="scope.row.share == 1"
                    class="noMargin"
                    size="mini"
                    plain
                    type="warning"
                    icon="el-icon-close"
                    @click="unShare(scope.row.id)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip content="删除" placement="top">
                  <el-button
                    class="noMargin"
                    size="mini"
                    plain
                    type="danger"
                    icon="el-icon-delete"
                    @click="del(scope.row.id)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <el-pagination
          small
          class="margin_top-medium"
          @size-change="paginationSizeChange"
          @current-change="paginationCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 20, 30]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next"
          :total="pagination.total"
          style="text-align: center"
        ></el-pagination>
      </div>
    </el-row>
  </section>
</template>
<script>
import axios from "axios";

const FLUSH_INTERVAL = 60000;
const api = {
  download: "/download",
  get: "/cloudDrive/get",
  save: "/cloudDrive/save",
  share: "/cloudDrive/share/set",
  unShare: "/cloudDrive/share/cancel",
  delete: "/cloudDrive/delete",
  changeName: "/cloudDrive/changeName",
};

export default {
  name: "CloudDrive",
  props: {
    user_id: Number,
  },
  components: {},
  watch: {},
  data() {
    return {
      tableData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0,
      },
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
      this.$emit("cloudStatusChanged", 0);
      this.$refs.upload.clearFiles();
    },
    uploadProgress() {
      this.$emit("cloudStatusChanged", 1);
    },
    async submitEditMode(rowId, file_id, rowFileName) {
      try {
        const { data: res } = await axios.post(api.changeName, {
          user_id: this.user_id,
          file_id: file_id,
          file_name: rowFileName,
        });
        await this.changeEditMode(rowId, "disable");
        this.get();
        this.$message({
          message: res.msg,
          type: "success",
        });
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    changeEditMode(rowId, action) {
      for (let x = 0; x < this.tableData.length; x++) {
        if (this.tableData[x].id == rowId) {
          if (action == "enable") {
            this.tableData[x].editMode = true;
          }
          if (action == "disable") {
            this.tableData[x].editMode = false;
          }
          this.$set(this.tableData, x, this.tableData[x]);
          break;
        }
      }
    },
    async get() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
          pagination_size: this.pagination.pageSize,
          current_page: this.pagination.currentPage,
        });
        this.tableData = res.data.list;
        for (let x = 0; x < this.tableData.length; x++) {
          this.tableData[x].editMode = false;
        }
        this.pagination.total = res.data.total;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async save(file_id) {
      try {
        const { data: res } = await axios.post(api.save, {
          user_id: this.user_id,
          file_id: file_id,
        });
        this.$message({
          message: res.msg,
          type: "success",
        });
        this.get();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
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
          type: "error",
        });
      }
    },
    async share(id) {
      try {
        const { data: res } = await axios.post(api.share, {
          user_id: this.user_id,
          id: id,
        });
        this.get();
        this.$message({
          message: "创建分享链接成功，点击[复制分享链接]按钮复制吧！",
          type: "success",
        });
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    onCopy(e) {
      this.$message({
        message: "复制分享链接成功！现在就去粘贴吧！",
        type: "success",
      });
    },
    onError(e) {
      alert("复制失败");
    },
    async unShare(id) {
      this.$confirm(
        "取消分享后，原来的分享链接将失效，确定取消分享吗？",
        "提示",
        {}
      ).then(async () => {
        try {
          const { data: res } = await axios.post(api.unShare, {
            user_id: this.user_id,
            id: id,
          });
          this.get();
          this.$message({
            message: res.msg,
            type: "success",
          });
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error",
          });
        }
      });
    },
    async del(row_id) {
      this.$confirm("确认删除吗？", "提示", {}).then(async () => {
        try {
          const { data: res } = await axios.post(api.delete, {
            user_id: this.user_id,
            id: row_id,
          });
          this.$message({
            message: res.msg,
            type: "success",
          });
          this.get();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error",
          });
        }
      });
    },
  },
  mounted() {
    this.get();
    this.timer = window.setInterval(this.get, FLUSH_INTERVAL);
  },
  beforeDestroy() {
    window.clearInterval(this.timer);
  },
};
</script>
</style>
