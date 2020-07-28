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
          <i
            class="el-icon-edit"
            style="color:#409EFF; cursor: pointer;"
            v-show="!singleNotesData.editMode&activeNote==singleNotesData.name"
            @click="edit(singleNotesData.name)"
          ></i>
          <i
            class="el-icon-check"
            style="color:#67C23A; cursor: pointer;"
            v-show="singleNotesData.editMode&activeNote==singleNotesData.name"
            @click="submit(singleNotesData.name)"
          ></i>
          <el-popover placement="right" width="160" trigger="hover" v-model="visible">
            <el-button type="text" style="color:#E6A23C" icon="el-icon-bell">提醒</el-button>
            <el-button type="text" style="color:#F56C6C" icon="el-icon-delete">删除</el-button>
            <i class="el-icon-more" slot="reference" v-show="activeNote==singleNotesData.name"></i>
          </el-popover>
        </span>
        <el-input
          v-show="singleNotesData.editMode"
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 4}"
          placeholder="请输入内容"
          v-model="singleNotesData.content"
        ></el-input>
        <p
          style="color: #606266;
          font-size: 15px;
          text-align: left;
          line-height: 35px;
          margin-left: 10px;
          margin-right: 20px;
          margin-top: 0px;
          font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;"
          v-show="!singleNotesData.editMode"
        >{{singleNotesData.content}}</p>
      </el-tab-pane>
    </el-tabs>
    <el-row type="flex" justify="center" v-show="user_id!=0">
      <WidgetButton
        :user_id="user_id"
        :widget_id="widget_id"
        :buttons="buttons"
        @add="add()"
        @sort="sort()"
        @notify="notify()"
        @setting="setting()"
      ></WidgetButton>
    </el-row>
  </section>
</template>
<script>
import axios from "axios";
import WidgetButton from "./common/WidgetButton.vue";

const api = {
  get: "/notes/get"
};
export default {
  name: "notes",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array
  },
  components: {
    WidgetButton
  },
  data() {
    return {
      notesData: [],
      activeNote: ""
    };
  },
  methods: {
    async notesGet() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id
        });
        this.notesData = res.data;
        this.activeNote = this.notesData[0].name;
        for (let x = 0; x < this.notesData.length; x++) {
          this.notesData[x].editMode = false;
          this.notesData[x].content
            .replace(/\n/g, "<br>")
            .replace(/\s/g, "&nbsp;");
        }
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
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
    edit(notesName) {
      let i = this.notesGetIndex(notesName);
      this.notesData[i].editMode = true;
    },
    submit(notesName) {
      let i = this.notesGetIndex(notesName);
      this.notesData[i].editMode = false;
    }
  },
  mounted() {
    this.notesGet();
  }
};
</script>
<style scoped>
</style>
