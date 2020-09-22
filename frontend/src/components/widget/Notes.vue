<template>
  <section>
    <el-main class="noPadding" style="height: 300px;">
      <el-row type="flex" justify="center">
          <div class="widget-label">便签</div>
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
          :name="singleNotesData.token"
          style="padding-left:0px;"
        >
          <span slot="label">
            <el-dropdown
              @command="actionClicked"
              size="small"
              v-show="activeNote==singleNotesData.token"
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
    </el-main>
    <el-footer height="31px" style="justify-content: center; display: flex;" v-if="user_id != 0">
      <WidgetButton
        :user_id="user_id"
        :widget_id="widget_id"
        :buttons="buttons"
        @add="add()"
        @revert="revertClicked()"
      ></WidgetButton>
    </el-footer>

    <!-- 编辑dialog -->
    <el-dialog :title="edit.dialogTitle" :visible.sync="edit.visible" :close-on-click-modal="false">
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
          style="width: 80%;"
          autosize
          class="margin_bottom-large"
          v-model="edit.content"
          placeholder="请输入便签内容"
        ></el-input>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="edit.visible = false">取消</el-button>
        <el-button size="small" type="primary" @click="editSubmit()">确定</el-button>
      </div>
    </el-dialog>

    <!-- 推送dialog -->
    <el-dialog title="提醒" :visible.sync="notify.visible">
      <el-form ref="form" :model="notify.form" size="mini" class="padding_bottom-medium">
        <el-form-item label="标题">
          <p
            class="notesText"
            style="font-size: 14px; padding-top: 0px; margin-top: 0px; line-height: 28px; margin-bottom: 0px"
          >{{notify.form.title}}</p>
        </el-form-item>
        <el-form-item label="内容">
          <p
            class="notesText"
            style="font-size: 14px; margin-left: 40px; line-height: 28px; padding-top: 0px; margin-top: 0px; margin-bottom: 0px"
          >{{notify.form.content}}</p>
        </el-form-item>
        <el-form-item label="提醒方式">
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
        <el-form-item label="提醒时间">
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
          style="font-size: 12px; color: #F56C6C; padding-top: 0px; margin-top: 0px; margin-bottom: 0px"
        >*提交后不能取消，但可以多次提交。</p>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" @click="notify.visible=false">取消</el-button>
        <el-button type="primary" size="small" @click="notifySubmit()">确定</el-button>
      </span>
    </el-dialog>

    <!-- 时间机器dialog -->
    <el-dialog title="时间机器" :visible.sync="revert.visible">
      <p
        class="notesText"
        style="font-size: 12px; color: #F56C6C; padding-top: 0px; margin-top: 0px; margin-bottom: 0px"
      >*可以恢复到最近的五个版本中的任意一个，此操作不会对过去的版本产生影响，而是会使用以前版本的内容生成一个新版本。</p>
      <el-table :data="revert.data" style="text-align: center; margin-bottom: 20px;" size="small">
        <el-table-column prop="update_time" label="版本"></el-table-column>
        <el-table-column prop="user" label="创建人" width="100"></el-table-column>
        <el-table-column :key="Math.random()" label="操作" width="150">
          <template slot-scope="scope">
            <el-popover placement="right" width="350" trigger="hover">
              <el-table :data="scope.row.detail" style="text-align: center;" size="small">
                <el-table-column prop="name" width="100" label="标题"></el-table-column>
                <el-table-column label="内容">
                  <template slot-scope="innerScope">
                    <span v-if="innerScope.row.content.length<25">{{ innerScope.row.content }}</span>
                    <el-popover
                      placement="top"
                      width="200"
                      trigger="hover"
                      :content="innerScope.row.content"
                    >
                      <span
                        slot="reference"
                        v-if="innerScope.row.content.length>=25"
                      >{{ innerScope.row.content.substring(0,25)+'...' }}</span>
                    </el-popover>
                  </template>
                </el-table-column>
              </el-table>
              <el-button
                class="noMargin"
                size="mini"
                plain
                type="primary"
                slot="reference"
                @click="revertConfirm(scope.row.update_time, scope.row.detail)"
              >恢复至此版本</el-button>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="revert.visible = false">取消</el-button>
      </div>
    </el-dialog>
  </section>
</template>
<script>
import axios from "axios";
import WidgetButton from "../common/WidgetButton.vue";

const api = {
  get: "/notes/get",
  save: "/notes/save",
  notify: "/notes/notify",
  revert: "/notes/revert",
};
export default {
  name: "notes",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
    flush: Number,
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
      revert: {
        visible: false,
        data: [],
      },
    };
  },
  methods: {
    actionClicked(command) {
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
    notesGetIndex(notesName) {
      for (let x = 0; x < this.notesData.length; x++) {
        if (this.notesData[x].token == notesName) {
          return x;
        }
      }
      return null;
    },
    async notesGet() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
        });
        this.notesData = res.data;
        if (this.notesData.length != 0) {
          this.activeNote = this.notesData[0].token;
          for (let x = 0; x < this.notesData.length; x++) {
            this.notesData[x].content
              .replace(/\n/g, "<br>")
              .replace(/\s/g, "&nbsp;");
          }
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
    add() {
      this.edit.dialogTitle = "新建";
      let d = new Date();
      this.edit.title = d.getMonth() + 1 + "." + d.getDate();
      this.edit.content = "";
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
    editClicked(notesName) {
      let i = this.notesGetIndex(notesName);
      this.edit.noteIndex = i;
      this.edit.dialogTitle = "编辑";
      this.edit.title = this.notesData[i].name;
      this.edit.content = this.notesData[i].content;
      this.edit.visible = true;
    },
    async editSubmit() {
      if (this.edit.dialogTitle == "编辑") {
        this.notesData[this.edit.noteIndex].title = this.edit.title;
        this.notesData[this.edit.noteIndex].content = this.edit.content;
      } else if (this.edit.dialogTitle == "新建") {
        let timestamp = new Date().getTime();
        let salt = Math.floor(Math.random() * 100000000000000);
        this.notesData.push({
          name: this.edit.title,
          content: this.edit.content,
          token: String(timestamp) + String(salt),
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
    async notifySubmit() {
      try {
        const { data: res } = await axios.post(api.notify, {
          user_id: this.user_id,
          title: this.notify.form.title,
          content: this.notify.form.content,
          method: this.notify.form.notifyMethod.select,
          notify_trigger_time:
            this.notify.form.triggerDate + " " + this.notify.form.triggerTime,
        });
        this.$message({
          message: res.msg,
          type: "success",
        });
        this.notify.visible = false;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async revertClicked() {
      try {
        const { data: res } = await axios.post(api.revert, {
          user_id: this.user_id,
        });
        this.revert.data = res.data;
        this.revert.visible = true;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async revertConfirm(update_time, detail) {
      this.$confirm(
        "确认使用时间机器恢复至[" + update_time + "]的版本吗?",
        "提示",
        {}
      ).then(async () => {
        this.notesData = detail;
        await this.notesSave();
        await this.notesGet();
        this.revert.visible = false;
      });
    },
  },
  mounted() {
    this.notesGet();
    this.timer = window.setInterval(this.notesGet, this.flush);
  },
  beforeDestroy() {
    window.clearInterval(this.timer);
  },
};
</script>
<style scoped>
.notesText {
  color: #606266;
  font-size: 15px;
  text-align: left;
  line-height: 35px;
  margin-left: 10px;
  margin-right: 20px;
  margin-top: 0px;
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
