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
        ></el-button>
      </el-tooltip>
      <el-tooltip class="noMargin" effect="dark" content="查看最近一次由我运行的日志" placement="top">
        <el-button
          class="noMargin"
          type="primary"
          plain
          icon="el-icon-tickets"
          circle
          @click="singleDataLog()"
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
import ConsoleScriptRun from "./ConsoleScriptRun";
const api = {
  subSystem: "/script/subSystem",
  subSystemAdd: "/script/subSystemAdd",
  subSystemDelete: "/script/subSystemDelete"
};
export default {
  name: "ConsoleScriptButtons",
  components: {
    ConsoleScriptRun
  },
  props: {
    user_id: Number,
    singleForm: Array,
    scriptId: Number
  },
  watch: {},
  data() {
    return {
      output: {
        canBeTerminate: false,
        loading: false,
        log_id: 0,
        logs: [],
        visible: false,
        text: "",
        important_fields: [],
        isAlert: false
      },
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
      }
    };
  },
  watch: {},
  methods: {
    //回放上一次由我运行的脚本参数
    async singleDataReplay() {
      try {
        const { data: res } = await axios.post(api.replay, {
          script_id: singleForm.id,
          user_id: this.user_id
        });
        if (res.code != 200) {
          this.$message({
            message: res.msg,
            type: "error"
          });
        } else if (singleForm.version != res.data.version) {
          this.$message({
            message:
              "检测到脚本配置发生过修改(" +
              "V" +
              res.data.version +
              "→" +
              "V" +
              singleForm.version +
              ")，可能无法完美恢复上一次参数",
            type: "info"
          });
        }
        for (var f = 0; f < singleForm.formDataDetail.length; f++) {
          try {
            singleForm.formDataDetail[f].value =
              res.data.detail[singleForm.formDataDetail[f].label];
          } catch (err) {
            console.log(
              "[" +
                singleForm.formDataDetail[f].label +
                "]" +
                "恢复失败：" +
                err
            );
          }
        }
        this.$emit('replay',singleForm)
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    singleDataLog() {
      this.$emit("singleLog");
    },
    //展示最近一次由我运行的脚本日志
    async singleDataLog() {
      try {
        const { data: res } = await axios.post(api.getNewestLog, {
          script_id: singleForm.id,
          user_id: this.user_id
        });
        this.output.visible = true;
        this.output.text = res.data[0].output;
        if (this.bool.singleDataLog) {
          this.$nextTick(() => {
            try {
              var scroll = new BScroll(this.$refs.outputDialog, {
                scrollY: true,
                scrollbar: {
                  fade: true, // node_modules\better-scroll\dist\bscroll.esm.js:2345可以调时间，目前使用的是'var time = visible ? 500 : 5000;'
                  interactive: true
                },
                momentumLimitDistance: 300,
                mouseWheel: true,
                preventDefault: false
              });
              scroll.refresh();
            } catch (error) {
              console.log("滚动条设置失败" + error);
            }
          });
          this.bool.singleDataLog = false;
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    }
  },
  mounted() {}
};
</script>

<style>
</style>
