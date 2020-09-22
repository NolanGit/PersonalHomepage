<template>
  <section>
    <el-row class="margin_bottom-large">
      <div class="margin_left-medium margin_right-medium" style="text-align: center;">
        <el-upload
          class="upload-demo"
          ref="upload"
          style="text-align: center;"
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
            将图片拖到此处，或
            <em>点击上传</em>
          </div>
        </el-upload>
      </div>
    </el-row>
    <el-row>
      <div class="margin_left-medium margin_right-medium">
        <div
          class="scrollbar-div"
          style="max-height:calc(100vh - 435px); height: calc(100vh - 435px);"
        >
          <el-table :data="tableData" style="text-align: center;" size="small">
            <el-table-column label="名称">
              <template slot-scope="scope">
                <div style="display: inline-flex;">
                  <span
                    v-if="scope.row.editMode==false"
                    style="margin-right: 10px"
                  >{{ scope.row.file_name }}</span>
                  <i
                    v-if="scope.row.editMode==false"
                    class="el-icon-edit"
                    style="cursor: pointer; margin-top: 6px; font-size: 13px;"
                    @click="changeEditMode(scope.row.id,'enable')"
                  ></i>
                  <el-input
                    v-if="scope.row.editMode==true"
                    v-model="scope.row.file_name"
                    placeholder="请输入内容"
                    size="mini"
                  ></el-input>
                  <i
                    v-if="scope.row.editMode==true"
                    class="el-icon-check"
                    style="cursor: pointer; margin-top: 6px; font-size: 13px; color: #67C23A; padding-left: 5px"
                    @click="submitEditMode(scope.row.id,scope.row.file_name)"
                  ></i>
                  <i
                    v-if="scope.row.editMode==true"
                    class="el-icon-close"
                    style="cursor: pointer; margin-top: 6px; font-size: 13px; color: #F56C6C; padding-left: 5px"
                    @click="changeEditMode(scope.row.id,'disable')"
                  ></i>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="update_time" label="上传时间" width="170"></el-table-column>
            <el-table-column label="操作" width="280">
              <template slot-scope="scope">
                <el-popover placement="left" width="400" trigger="hover">
                  <div style="text-align: center; display: grid;">
                    <img
                      :src="scope.row.shorted_link"
                      @click="open(scope.row.shorted_link)"
                      class="image"
                      style="max-height: 300px; max-width: 300px; margin: 0 auto; cursor: pointer;"
                    />
                    <div style="margin: 0 auto; display: inline-flex;">
                      <i
                        class="el-icon-top"
                        style="color: #303133; padding-top: 0px; margin-top: 12px; margin-bottom: 10px"
                      ></i>
                      <p
                        class="notesText"
                        style="font-size: 12px; color: #303133; padding-top: 0px; margin-top: 10px; margin-bottom: 10px"
                      >点击图片以下载原图</p>
                    </div>
                  </div>
                  <el-button
                    slot="reference"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    icon="el-icon-download"
                    @click="download(scope.row.file_id)"
                  ></el-button>
                </el-popover>
                <el-tooltip content="复制链接" placement="top">
                  <el-button
                    class="margin_left-small"
                    size="mini"
                    plain
                    type="primary"
                    icon="el-icon-link"
                    v-clipboard:copy="scope.row.shorted_link"
                    v-clipboard:success="onCopy"
                    v-clipboard:error="onError"
                  ></el-button>
                </el-tooltip>
                <el-tooltip content="删除" placement="top">
                  <el-button
                    class="margin_left-small"
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
          style="text-align:center"
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
  get: "/imageHosting/get",
  save: "/imageHosting/save",
  delete: "/imageHosting/delete",
  changeName: "/imageHosting/changeName",
};

export default {
  name: "ImageHosting",
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
    open(url) {
      window.open(url);
    },
    async submitEditMode(rowId, rowFileName) {
      try {
        const { data: res } = await axios.post(api.changeName, {
          user_id: this.user_id,
          id: rowId,
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
    onCopy(e) {
      this.$message({
        message: "复制分享链接成功！现在就去粘贴吧！",
        type: "success",
      });
    },
    onError(e) {
      alert("复制失败");
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
