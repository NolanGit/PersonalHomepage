<template>
  <section>
    <div class="single-data-setting">
      <el-tooltip effect="dark" content="回放最近一次由我运行的参数" placement="top">
        <el-button
          type="primary"
          plain
          icon="el-icon-refresh-left"
          circle
          @click="singleDataReplay()"
          class="noMargin"
        ></el-button>
      </el-tooltip>
      <el-tooltip effect="dark" content="查看最近一次由我运行的日志" placement="top">
        <el-button
          type="primary"
          plain
          icon="el-icon-tickets"
          circle
          @click="singleDataLog()"
          class="noMargin"
        ></el-button>
      </el-tooltip>
      <el-tooltip class="question-mark" effect="dark" content="查看最近50次运行记录" placement="top">
        <el-popover placement="left" width="1010" trigger="click">
          <div class="scrollbar-div max-height-medium" ref="scrollbarDiv">
            <el-table size="small" :data="output.logs" stripe v-loading="output.loading">
              <el-table-column width="110" property="user" label="运行人"></el-table-column>
              <el-table-column
                v-for="important_field in output.important_fields"
                :key="important_field"
                min-width="110"
                :property="important_field"
                :label="important_field"
              ></el-table-column>
              <el-table-column min-width="235" property="options" label="操作">
                <template slot-scope="scope">
                  <el-popover placement="left" width="350" trigger="hover">
                    <tr v-for="(key,index) in scope.row.detail" :key="key">
                      <td class="td--label">
                        <b>{{index+":"}}</b>
                      </td>
                      <td>{{key}}</td>
                    </tr>
                    <el-button
                      plain
                      size="mini"
                      type="primary"
                      icon="el-icon-set-up"
                      slot="reference"
                    >参数</el-button>
                  </el-popover>
                  <el-button
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    icon="el-icon-tickets"
                    @click="log_output(scope.row.output)"
                  >日志</el-button>
                  <el-button
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    icon="el-icon-refresh-left"
                    @click="log_replay(scope.row.version,scope.row.detail)"
                  >回放</el-button>
                </template>
              </el-table-column>
              <el-table-column width="150" property="update_time" label="运行开始时间"></el-table-column>
              <el-table-column width="80" property="duration" label="耗时"></el-table-column>
              <el-table-column width="80" property="log_id" label="运行ID"></el-table-column>
            </el-table>
          </div>
          <el-button
            type="primary"
            plain
            icon="el-icon-files"
            circle
            slot="reference"
            :loading="output.loading"
            @click="singleDataShowLogs()"
          ></el-button>
        </el-popover>
      </el-tooltip>
      <el-tooltip class="question-mark" effect="dark" content="定时运行" placement="top">
        <el-popover placement="left" width="900" trigger="click" :v-model="schedule.popoverVisible">
          <el-table :data="schedule.schedules" stripe v-loading="schedule.loading">
            <el-table-column width="100" property="schedule_id" label="定时任务ID"></el-table-column>
            <el-table-column width="80" property="user_name" label="创建人"></el-table-column>
            <el-table-column width="50" property="is_automatic_text" label="重复"></el-table-column>
            <el-table-column width="180" property="trigger_time" label="下次运行时间"></el-table-column>
            <el-table-column width="180" property="update_time" label="创建时间"></el-table-column>
            <el-table-column min-width="250" property="options" label="操作">
              <template slot-scope="scope">
                <el-popover placement="left" width="350" trigger="hover">
                  <tr v-for="(key,index) in scope.row.detail" :key="key">
                    <td class="td--label">
                      <b>{{index+":"}}</b>
                    </td>
                    <td>{{key}}</td>
                  </tr>
                  <el-button
                    plain
                    size="mini"
                    type="primary"
                    icon="el-icon-set-up"
                    slot="reference"
                  >参数</el-button>
                </el-popover>
                <el-button
                  class="noMargin"
                  size="mini"
                  plain
                  type="primary"
                  icon="el-icon-edit"
                  @click="scheduleEdit(scope.row)"
                >编辑</el-button>
                <el-button
                  class="noMargin"
                  size="mini"
                  plain
                  type="danger"
                  icon="el-icon-delete"
                  @click="scheduleDelete(scope.row.schedule_id)"
                >停止</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="add" style="width: 99.87%;" @click="schedule.dialogVisible = true">
            <span>
              + 使用
              <b>当前表单填写的参数</b> 创建定时任务
            </span>
          </div>
          <el-button
            type="primary"
            plain
            icon="el-icon-alarm-clock"
            circle
            slot="reference"
            @click="scheduleShow()"
          ></el-button>
        </el-popover>
      </el-tooltip>
      <el-tooltip effect="dark" content="编辑脚本" placement="top">
        <el-popover placement="bottom-end" width="250" trigger="hover">
          <tr>
            <td class="td--label--medium">
              <b>{{"最后修改人:"}}</b>
            </td>
            <td>{{singleForm.user}}</td>
          </tr>
          <tr>
            <td class="td--label--medium">
              <b>{{"版本:"}}</b>
            </td>
            <td>{{"V"+singleForm.version}}</td>
          </tr>
          <tr>
            <td class="td--label--medium">
              <b>{{"运行次数:"}}</b>
            </td>
            <td>{{singleForm.runs+"次"}}</td>
          </tr>
          <tr>
            <td class="td--label--medium">
              <b>{{"更新时间:"}}</b>
            </td>
            <td>{{singleForm.update_time}}</td>
          </tr>
          <el-button
            type="primary"
            plain
            icon="el-icon-setting"
            circle
            slot="reference"
            @click="singleDataSetting()"
          ></el-button>
        </el-popover>
      </el-tooltip>
      <el-tooltip effect="dark" content="删除脚本" placement="top">
        <el-button type="danger" plain icon="el-icon-delete" circle @click="singleDataDelete()"></el-button>
      </el-tooltip>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import { deepClone } from "../../js/common";
const api = {
  replay: "/script/replay",
  getLogs: "/script/getLogs",
  getNewestLog: "/script/getNewestLog",
  schedule: "/script/schedule",
  scheduleAdd: "/script/scheduleEdit",
  scheduleDelete: "/script/scheduleDelete"
};
export default {
  name: "ConsoleScriptButtons",
  components: {},
  props: {
    user_id: Number,
    singleForm: Array
  },
  watch: {},
  data() {
    return {
      schedule: {
        label: "新建定时任务",
        popoverVisible: false,
        dialogVisible: false,
        loading: false,
        schedules: [],
        scheduleData: {
          schedule_id: 0,
          triggerDate: "",
          triggerTime: "",
          is_automatic: false,
          interval: {
            value: 1,
            unit: {
              select: 2,
              options: [
                {
                  value: 1,
                  label: "小时"
                },
                {
                  value: 2,
                  label: "天"
                }
              ]
            }
          }
        }
      },
      output: {
        canBeTerminate: false,
        loading: false,
        log_id: 0,
        logs: [],
        visible: false,
        text: "",
        important_fields: [],
        isAlert: false
      }
    };
  },
  watch: {},
  methods: {
    //回放上一次由我运行的脚本参数
    async singleDataReplay() {
      try {
        const { data: res } = await axios.post(api.replay, {
          script_id: this.singleForm.id,
          user_id: this.user_id
        });
        if (res.code != 200) {
          this.$message({
            message: res.msg,
            type: "error"
          });
        } else if (this.singleForm.version != res.data.version) {
          this.$message({
            message:
              "检测到脚本配置发生过修改(" +
              "V" +
              res.data.version +
              "→" +
              "V" +
              this.singleForm.version +
              ")，可能无法完美恢复上一次参数",
            type: "info"
          });
        }
        for (var f = 0; f < this.singleForm.formDataDetail.length; f++) {
          try {
            this.singleForm.formDataDetail[f].value =
              res.data.detail[this.singleForm.formDataDetail[f].label];
          } catch (err) {
            console.log(
              "[" +
                this.singleForm.formDataDetail[f].label +
                "]" +
                "恢复失败：" +
                err
            );
          }
        }
        this.$message({
          message: "参数填充成功",
          type: "success"
        });
        this.$emit("replay", this.singleForm);
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //展示最近一次由我运行的脚本日志
    async singleDataLog() {
      try {
        const { data: res } = await axios.post(api.getNewestLog, {
          script_id: this.singleForm.id,
          user_id: this.user_id
        });
        this.$emit("output", res.data[0].output);
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //展示脚本的运行日志
    async singleDataShowLogs() {
      this.output.loading = true;
      this.output.logs = [];
      try {
        const { data: res } = await axios.post(api.getLogs, {
          script_id: this.singleForm.id,
          user_id: this.user_id
        });
        this.output.logs = res.data.logs;
        this.output.important_fields = res.data.important_fields;
        for (let o = 0; o < this.output.logs.length; o++) {
          for (let i = 0; i < this.output.important_fields.length; i++) {
            this.output.logs[o][
              this.output.important_fields[i]
            ] = this.output.logs[o].detail[this.output.important_fields[i]];
          }
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
      this.output.loading = false;
    },
    //展示日志中的输出
    log_output(output) {
      this.$emit("output", output);
    },
    //回放日志中的参数
    log_replay(version, detail) {
      for (var f = 0; f < this.singleForm.formDataDetail.length; f++) {
        try {
          this.singleForm.formDataDetail[f].value =
            detail[this.singleForm.formDataDetail[f].label];
        } catch (err) {
          console.log(
            "[" +
              this.singleForm.formDataDetail[f].label +
              "]" +
              "恢复失败：" +
              err
          );
        }
      }
      if (this.singleForm.version != version) {
        this.$message({
          message:
            "参数填充成功，但是检测到脚本配置发生过修改(" +
            "V" +
            version +
            "→" +
            "V" +
            this.singleForm.version +
            ")，可能无法完美恢复上一次参数，请关闭列表弹出框后查看",
          type: "info",
          duration: 4000
        });
      } else {
        this.$message({
          message: "参数填充成功，请关闭列表弹出框后点击提交按钮以运行",
          type: "success"
        });
        this.$emit("replay", this.singleForm);
      }
    },
    //展示定时任务列表
    async scheduleShow() {
      this.schedule.loading = true;
      this.schedule.schedules = [];
      try {
        const { data: res } = await axios.post(api.schedule, {
          script_id: this.singleForm.id,
          user_id: this.user_id
        });
        this.schedule.loading = false;
        this.schedule.schedules = res.data;
        this.schedule.popoverVisible = true;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //点击提交定时任务按钮
    async scheduleAdd() {
      var start_folder_with_start_script =
        "cd " +
        this.singleForm.start_folder +
        " && " +
        this.singleForm.start_script;
      var command_get_result = this.command_get(
        start_folder_with_start_script,
        this.singleForm.type
      );
      var command = command_get_result.command;
      var detail = command_get_result.detail;
      try {
        const { data: res } = await axios.post(api.scheduleAdd, {
          user_id: this.user_id,
          script_id: this.singleForm.id,
          command: command,
          detail: detail,
          version: this.singleForm.version,
          trigger_time:
            this.schedule.scheduleData.triggerDate +
            " " +
            this.schedule.scheduleData.triggerTime,
          is_automatic: this.schedule.scheduleData.is_automatic == true ? 1 : 0,
          interval_raw: Number(this.schedule.scheduleData.interval.value),
          interval_unit: this.schedule.scheduleData.interval.unit.select,
          schedule_id: this.schedule.scheduleData.schedule_id
        });
        this.$message({
          message: "成功！",
          type: "success"
        });
        this.schedule.dialogVisible = false;
        this.schedule.scheduleData.triggerDate = "";
        this.schedule.scheduleData.triggerTime = "";
        this.schedule.scheduleData.is_automatic = false;
        this.schedule.scheduleData.schedule_id = 0;
        this.schedule.scheduleData.interval.value = "";
        this.schedule.scheduleData.interval.unit.select = 2;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //编辑定时任务
    scheduleEdit(schedule) {
      console.log(schedule);
      this.schedule.label = "编辑定时任务";
      this.schedule.scheduleData.schedule_id = schedule.schedule_id;
      this.schedule.scheduleData.is_automatic = schedule.is_automatic
        ? true
        : false;
      this.schedule.scheduleData.triggerDate = schedule.trigger_time.split(
        " "
      )[0];
      this.schedule.scheduleData.triggerTime = schedule.trigger_time
        .split(" ")[1]
        .substr(0, 5);
      this.schedule.scheduleData.interval.unit.select = schedule.is_automatic
        ? schedule.interval_unit
        : 2;
      this.schedule.scheduleData.interval.value = schedule.is_automatic
        ? schedule.interval_raw
        : 1;
      this.schedule.dialogVisible = true;
    },
    //删除定时任务
    async scheduleDelete(schedule_id) {
      this.$confirm("确认停止并删除定时任务吗?", "提示", {}).then(async () => {
        try {
          const { data: res } = await axios.post(api.scheduleDelete, {
            user_id: this.user_id,
            schedule_id: schedule_id
          });
          this.$message({
            message: data["msg"],
            type: "success"
          });
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      });
    },
    //删除脚本
    async singleDataDelete() {
      this.$confirm("确认删除吗?", "提示", {})
        .then(async () => {
          try {
            const { data: res } = await axios.post(api.delete, {
              script_id: this.singleForm.id,
              user_id: this.user_id
            });
            this.$message({
              message: res.msg,
              type: "success"
            });
            this.subSystemScript(this.activedSystem);
          } catch (e) {
            console.log(e);
            this.$message({
              message: e.response.data.msg,
              type: "error"
            });
          }
        })
        .catch(() => {});
    }
  },
  mounted() {}
};
</script>

<style>
</style>
