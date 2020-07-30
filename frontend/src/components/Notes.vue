<template>
  <section>
    <el-row type="flex" justify="center">
      <div>
        <div class="widget-label">便签</div>
      </div>
    </el-row>
    <el-tabs
      tab-position="left"
      class="scrollbar-div"
      style="max-height: 210px; min-height: 210px;"
      v-model="activeNote"
    >
      <el-tab-pane
        v-for="singleNotesData in notesData"
        :key="singleNotesData"
        :label="singleNotesData.name"
        :name="singleNotesData.name"
        style="padding-left:0px;"
      >
        <span slot="label">
          <el-dropdown @command="handleCommand" size="small">
            {{singleNotesData.name}}
            <i
              class="el-icon-more"
              v-show="activeNote==singleNotesData.name"
            ></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item style="color:#409EFF" icon="el-icon-edit">编辑</el-dropdown-item>
              <el-dropdown-item style="color:#E6A23C" icon="el-icon-bell">提醒</el-dropdown-item>
              <el-dropdown-item style="color:#F56C6C" icon="el-icon-delete">删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </span>
        <p
          style="color: #606266;
          font-size: 15px;
          text-align: left;
          line-height: 35px;
          margin-left: 10px;
          margin-right: 20px;
          margin-top: 0px;
          font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;"
        >{{singleNotesData.content}}</p>
      </el-tab-pane>
    </el-tabs>
    <el-row type="flex" justify="center" v-show="user_id!=0">
      <WidgetButton :user_id="user_id" :widget_id="widget_id" :buttons="buttons" @add="add()"></WidgetButton>
    </el-row>
    <el-dialog :title="edit.dialogTitle" :visible.sync="edit.visible">
      <div class="div-flex">
        <div
          style="color: #606266;
          font-size: 15px;
          text-align: left;
          padding-top: 5px;
          font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;"
        >标题：</div>
        <el-input
          size="small"
          style="width: 80%;"
          class="margin_bottom-medium"
          v-model="edit.title"
          placeholder="请输入便签标题"
        ></el-input>
      </div>
      <div class="div-flex">
        <div
          style="color: #606266;
          font-size: 15px;
          text-align: left;
          padding-top: 5px;
          font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;"
        >内容：</div>
        <el-input
          type="textarea"
          size="small"
          style="width: 80%;"
          autosize
          class="margin_bottom-large"
          v-model="edit.content"
          placeholder="请输入便签内容"
        ></el-input>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="edit.visible = false">取消</el-button>
        <el-button size="small" type="primary" @click="submit()">确定</el-button>
      </div>
    </el-dialog>
  </section>
</template>
<script>
import axios from "axios";
import WidgetButton from "./common/WidgetButton.vue";

const api = {
  get: "/notes/get",
  save: "/notes/save",
};
export default {
  name: "notes",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
  },
  components: {
    WidgetButton,
  },
  data() {
    return {
      notesData: [],
      activeNote: "",
      edit: {
        noteIndex: Number,
        visible: false,
        dialogTitle: "",
        title: "",
        content: "",
      },
    };
  },
  methods: {
    async notesGet() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
        });
        this.notesData = res.data;
        this.activeNote = this.notesData[0].name;
        for (let x = 0; x < this.notesData.length; x++) {
          this.notesData[x].content
            .replace(/\n/g, "<br>")
            .replace(/\s/g, "&nbsp;");
        }
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async notesSave() {
      try {
        const { data: res } = await axios.post(api.save, {
          user_id: this.user_id,
          notes: this.notesData,
        });
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
    notesGetIndex(notesName) {
      for (let x = 0; x < this.notesData.length; x++) {
        if (this.notesData[x].name == notesName) {
          return x;
        }
      }
      return null;
    },
    add() {
      this.edit.dialogTitle = "新建";
      let d = new Date();
      this.edit.title = d.getMonth() + 1 + "." + d.getDate();
      this.edit.content = "";
      this.edit.visible = true;
    },
    editClicked(notesName) {
      let i = this.notesGetIndex(notesName);
      this.edit.noteIndex = i;
      this.edit.dialogTitle = "编辑";
      this.edit.title = this.notesData[i].name;
      this.edit.content = this.notesData[i].content;
      this.edit.visible = true;
    },
    submit() {
      if (this.edit.dialogTitle == "编辑") {
        this.notesData[this.edit.noteIndex].title = this.edit.title;
        this.notesData[this.edit.noteIndex].content = this.edit.content;
      } else if (this.edit.dialogTitle == "新建") {
        this.notesData.push();
      }
      this.notesSave();
      this.notesGet();
      this.edit.visible = false;
    },
  },
  mounted() {
    this.notesGet();
  },
};
</script>
<style scoped>
</style>
