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
          <el-dropdown
            @command="handleCommand"
            size="small"
            v-show="activeNote==singleNotesData.name"
            show-timeout="50"
            placement="bottom"
          >
            <span class="el-dropdown-link">
              <i class="el-icon-more" style="margin-right: 4px;"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item style="color:#409EFF" command="edit" icon="el-icon-edit">编辑</el-dropdown-item>
              <el-dropdown-item style="color:#E6A23C" command="bell" icon="el-icon-bell">提醒</el-dropdown-item>
              <el-dropdown-item style="color:#F56C6C" command="delete" icon="el-icon-delete">删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          {{singleNotesData.name}}
        </span>
        <p class="notesText">{{singleNotesData.content}}</p>
      </el-tab-pane>
    </el-tabs>
    <el-row type="flex" justify="center" v-show="user_id!=0">
      <WidgetButton :user_id="user_id" :widget_id="widget_id" :buttons="buttons" @add="add()"></WidgetButton>
    </el-row>

    <el-dialog :title="edit.dialogTitle" :visible.sync="edit.visible">
      <div class="div-flex">
        <div class="notesEditFormLabel">标题：</div>
        <el-input
          size="small"
          style="width: 80%;"
          class="margin_bottom-medium"
          v-model="edit.title"
          placeholder="请输入便签标题"
        ></el-input>
      </div>
      <div class="div-flex">
        <div class="notesEditFormLabel">内容：</div>
        <el-input
          type="textarea"
          size="small"
          style="width: 80%; margin-left: 40px;"
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

    <el-dialog title="提醒" :visible.sync="notify.visible">
      <el-form ref="form" :model="notify.form" size="mini" class="padding_bottom-medium">
        <el-form-item label="标题">
          <p
            class="notesText"
            style="font-size: 14px; padding-top: 0px; margin-top: 0px; margin-bottom: 0px"
          >{{notify.form.title}}</p>
        </el-form-item>
        <el-form-item label="内容">
          <p
            class="notesText"
            style="font-size: 14px; padding-top: 0px; margin-top: 0px; margin-bottom: 0px"
          >{{notify.form.content}}</p>
        </el-form-item>
        <el-form-item label="推送方式">
          <div class="div-flex" style="width:324px">
            <el-select
              v-model="notify.form.notifyMethod.select"
              placeholder="请选择"
              size="small"
              class="main_select--medium"
            >
              <el-option
                v-for="item in notify.form.notifyMethod.options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </div>
        </el-form-item>
        <el-form-item label="推送时间">
          <div class="div-flex">
            <el-date-picker
              v-model="notify.form.triggerDate"
              type="date"
              placeholder="选择日期"
              value-format="yyyy-MM-dd"
              size="small"
              class="main_select--medium"
            ></el-date-picker>
            <el-time-select
              v-model="notify.form.triggerTime"
              :picker-options="{
              start: '00:00',
              step: '01:00',
              end: '24:00'
            }"
              placeholder="选择时间"
              size="small"
              class="main_select--medium"
            ></el-time-select>
          </div>
        </el-form-item>
        <p
          class="notesText"
          style="font-size: 13px; color: red; padding-top: 0px; margin-top: 0px; margin-bottom: 0px"
        >*提交后不能取消，但可以多次提交</p>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" @click="notify.visible=false">取消</el-button>
        <el-button type="primary" size="small" @click="notifyConfirm()">确定</el-button>
      </span>
    </el-dialog>
  </section>
</template>
<script>
import axios from "axios";
import WidgetButton from "./common/WidgetButton.vue";

const api = {
  get: "/notes/get",
  save: "/notes/save",
  notify: "/notes/notify",
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
      notify: {
        visible: false,
        form: {
          title: "",
          content: "",
          notifyMethod: {
            select: 1,
            options: [
              {
                value: 1,
                label: "微信",
              },
              {
                value: 2,
                label: "邮件",
              },
            ],
          },
          triggerDate: "",
          triggerTime: "",
        },
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
    handleCommand(command) {
      if (command == "edit") {
        this.editClicked(this.activeNote);
      }
      if (command == "bell") {
        this.notifyClicked(this.activeNote);
      }
      if (command == "delete") {
        this.del(this.activeNote);
      }
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
    async del(notesName) {
      this.$confirm("确认删除吗?", "提示", {}).then(async () => {
        let i = this.notesGetIndex(notesName);
        this.edit.noteIndex = i;
        this.notesData.splice(i, 1);
        await this.notesSave();
        await this.notesGet();
      });
    },
    async submit() {
      if (this.edit.dialogTitle == "编辑") {
        this.notesData[this.edit.noteIndex].title = this.edit.title;
        this.notesData[this.edit.noteIndex].content = this.edit.content;
      } else if (this.edit.dialogTitle == "新建") {
        this.notesData.push({
          name: this.edit.title,
          content: this.edit.content,
        });
      }
      await this.notesSave();
      await this.notesGet();
      this.edit.visible = false;
    },
    notifyClicked(notesName) {
      let i = this.notesGetIndex(notesName);
      this.notify.form.title = this.notesData[i].name;
      this.notify.form.content = this.notesData[i].content;
      this.notify.visible = true;
    },
    async notifyConfirm() {
      try {
        const { data: res } = await axios.post(api.notify, {
          user_id: this.user_id,
          title: this.notify.form.title,
          content: this.notify.form.content,
          method: this.notify.form.method,
          notify_trigger_time:
            this.notify.form.triggerDate + " " + this.notify.form.triggerTime,
        });
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
    this.notesGet();
  },
};
</script>
<style scoped>
.notesText {
  color: #606266;
  font-size: 15px;
  text-align: left;
  padding-top: 5px;
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
}
.notesEditFormLabel {
  color: #606266;
  font-size: 15px;
  text-align: left;
  padding-top: 5px;
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
}
</style>
