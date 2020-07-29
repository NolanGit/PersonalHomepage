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
          {{singleNotesData.name}}
          <el-popover placement="right" width="50" trigger="hover" v-model="visible">
            <div>
              <div>
                <el-button
                  @click="edit(singleNotesData.name)"
                  type="text"
                  style="color:#409EFF"
                  icon="el-icon-edit"
                >编辑</el-button>
              </div>
              <div>
                <el-button
                  @click="notify(singleNotesData.name)"
                  type="text"
                  style="color:#E6A23C"
                  icon="el-icon-bell"
                >提醒</el-button>
              </div>
              <div>
                <el-button
                  @click="del(singleNotesData.name)"
                  type="text"
                  style="color:#F56C6C"
                  icon="el-icon-delete"
                >删除</el-button>
              </div>
            </div>
            <i class="el-icon-more" slot="reference" v-show="activeNote==singleNotesData.name"></i>
          </el-popover>
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
    <el-dialog :title="edit.title" :visible.sync="edit.visible">
      <el-input v-model="edit.title"></el-input>
      <el-input v-model="edit.content"></el-input>
      <div slot="footer" class="dialog-footer">
        <el-button @click="edit.visible = false">取消</el-button>
        <el-button type="primary" @click="submit()">确定</el-button>
      </div>
    </el-dialog>
  </section>
</template>
<script>
import axios from "axios";
import WidgetButton from "./common/WidgetButton.vue";

const api = {
  get: "/notes/get",
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
        visible: false,
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
    notesGetIndex(notesName) {
      for (let x = 0; x < this.notesData.length; x++) {
        if (this.notesData[x].name == notesName) {
          return x;
        }
      }
      return null;
    },
    add() {
      this.edit.title = "";
      this.edit.content = "";
      this.edit.visible = true;
    },
    edit(notesName) {
      let i = this.notesGetIndex(notesName);
      this.edit.title = this.notesData[i].name;
      this.edit.content = this.notesData[i].content;
      this.edit.visible = true;
    },
    submit() {
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
