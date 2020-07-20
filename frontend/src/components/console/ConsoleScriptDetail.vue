<template>
  <section>
    <el-card class="right-side-box-card" v-loading="formDataLoading">
      <el-row>
        <div class="info-text" v-show="formData.length==0">
          <i class="el-icon-back"></i>
          <div>请选择左侧系统</div>
        </div>
        <el-tabs v-model="activeTab" addable @tab-add="newTab" v-show="formData.length!=0">
          <el-tab-pane
            v-for="(singleForm,singleFormIndex) in formData"
            :key="singleForm.key"
            :label="singleForm.title"
            :lazy="true"
          >
            <td>
              <div
                v-for="(singleData,singleDataIndex) in singleForm.formDataDetail"
                :key="singleData.key"
                v-show="singleData.visible==1"
              >
                <el-row class="singleData">
                  <td type="flex" class="td--label">
                    <p class="td__p--label">{{singleData.label}}：</p>
                  </td>
                  <td type="flex" class="singleDataCol">
                    <el-tooltip
                      open-delay="500"
                      class="item"
                      :content="singleData.value"
                      placement="top"
                    >
                      <el-input
                        size="small"
                        v-if="singleData.type=='input'"
                        v-model="singleData.value"
                        :placeholder="singleData.placeHolder"
                        :disabled="singleData.disabled!=0"
                        class="main_input--large"
                      ></el-input>
                    </el-tooltip>
                    <el-select
                      size="small"
                      v-if="singleData.type=='select'"
                      v-model="singleData.value"
                      :placeholder="singleData.placeHolder"
                      :disabled="singleData.disabled!=0"
                      filterable
                      :allow-create="singleData.createable!=0"
                      default-first-option
                      class="main_select--large"
                    >
                      <el-option
                        v-for="item in singleData.options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                      ></el-option>
                    </el-select>
                    <el-date-picker
                      size="small"
                      v-if="singleData.type=='date'"
                      v-model="singleData.value"
                      type="date"
                      value-format="yyyy-MM-dd"
                      :placeholder="singleData.placeHolder"
                      :disabled="singleData.disabled!=0"
                      class="main_select--large"
                    ></el-date-picker>
                    <el-date-picker
                      size="small"
                      v-if="singleData.type=='dateRange'"
                      v-model="singleData.value"
                      type="daterange"
                      value-format="yyyy-MM-dd"
                      range-separator="至"
                      start-placeholder="开始日期"
                      end-placeholder="结束日期"
                      :placeholder="singleData.placeHolder"
                      :disabled="singleData.disabled!=0"
                      :picker-options="pickerOptions"
                      class="main_select--large"
                    ></el-date-picker>
                  </td>
                  <td class="padding_left-small padding_right-small min_width-small">
                    <el-tooltip
                      v-show="singleData.remark!=''"
                      class="question-mark"
                      effect="dark"
                      :content="singleData.remark"
                      placement="top"
                    >
                      <i class="fa fa-question-circle-o"></i>
                    </el-tooltip>
                  </td>
                  <td v-if="singleData.extra_button!=0">
                    <el-popover
                      placement="right"
                      width="300"
                      trigger="click"
                      v-model="extra_button.visible"
                      @after-leave="extra_button.output='';extra_button.output_temp=''"
                    >
                      <div
                        class="min_height-medium"
                        v-loading="extra_button.loading"
                        v-html="extra_button.output"
                      ></div>
                      <el-button
                        size="small"
                        slot="reference"
                        :disabled="extra_button.buttonLoading"
                        @click="extraButtonClicked(singleFormIndex,singleDataIndex,singleData.extra_button_script)"
                      >{{singleData.extra_button_label}}</el-button>
                    </el-popover>
                  </td>
                </el-row>
              </div>
            </td>
            <td class="single-data-setting">
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
                <el-popover
                  placement="left"
                  width="900"
                  trigger="click"
                  :v-model="schedule.popoverVisible"
                >
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
                <el-button
                  type="danger"
                  plain
                  icon="el-icon-delete"
                  circle
                  @click="singleDataDelete()"
                ></el-button>
              </el-tooltip>
            </td>
          </el-tab-pane>
        </el-tabs>
      </el-row>
      <!--底部按钮-->
      <el-row style="margin-top:60px;margin-left:10;margin-right:10px;">
        <el-button
          :loading="submitButtonLoading"
          type="primary"
          style="margin:20px 20px 20px 20px;position:absolute;bottom:0;right:0;z-index:99"
          @click="submit()"
          v-show="formData.length!=0"
        >提交</el-button>
      </el-row>
    </el-card>
  </section>
</template>

<script>
import axios from "axios";
import { deepClone } from "../../js/common";
const api = {
  subSystem: "/script/subSystem",
  subSystemAdd: "/script/subSystemAdd",
  subSystemDelete: "/script/subSystemDelete"
};
export default {
  name: "ConsoleScriptDetail",
  props: {
    user_id: Number,
    system_id: Number,
  },
  data() {
    return {
      activeSystem: [],
      subSystem: [],
      subSystemName: ""
    };
  },
  watch: {
    activeSystem(newVal, oldVal) {
      if (newVal == "") {
        return;
      }
      for (var s = 0; s < this.subSystem.length; s++) {
        if (newVal == this.subSystem[s].title) {
          break;
        }
      }
      this.$emit("subSystemClicked", this.subSystem[s].id);
    }
  },
  methods: {
    scriptLabelClicked(scriptName) {
      this.$emit("scriptNameClicked", scriptName);
    },
    //删除栏目
    async subSystemDelete() {
      this.$confirm("确认删除吗?", "提示", {}).then(async () => {
        try {
          for (var s = 0; s < this.subSystem.length; s++) {
            if (this.activeSystem == this.subSystem[s].title) {
              break;
            }
          }
          const { data: res } = await axios.post(api.subSystemDelete, {
            sub_system_id: this.subSystem[s].id,
            user_id: this.user_id
          });
          this.$message({
            message: "成功！",
            type: "success"
          });
          this.getSubSystem();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      });
    },
    //添加栏目
    async subSystemAdd() {
      try {
        const { data: res } = await axios.post(api.subSystemAdd, {
          sub_system_name: this.subSystemName,
          user_id: this.user_id
        });
        this.subSystem = [];
        this.subSystemScript();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    }
  }
};
</script>

<style>
</style>