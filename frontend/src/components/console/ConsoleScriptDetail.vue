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
            :name="singleForm.title"
            :lazy="true"
          >
            <div class="div-flex">
              <div>
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
              </div>
              <ConsoleScriptButtons
                :user_id="user_id"
                :singleForm="singleForm"
                @replay="singleDataReplay"
                @output="singleDataLog"
                @deleted="singleDataDeleted"
                @edit="singleDataSetting"
              />
            </div>
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

    <!--运行界面-->
    <el-drawer
      title="输出"
      :v-if="output.visible"
      :visible.sync="output.visible"
      size="70%"
      direction="btt"
      :before-close="outputDialogClose"
    >
      <div class="margin_left-medium margin_right-medium">
        <el-card shadow="hover">
          <div class="output-div" ref="outputDialog">
            <div class="output-html" v-html="output.text"></div>
          </div>
        </el-card>
      </div>
      <div class="dialog-footer" v-show="output.canBeTerminate">
        <el-button size="small" plain type="danger" @click.native="terminate()">停止运行</el-button>
      </div>
    </el-drawer>

    <!--编辑界面-->
    <el-drawer
      :title="edit.dialogTitle"
      :visible.sync="edit.visible"
      :close-on-click-modal="false"
      size="60%"
      @closed="editFormClosed"
    >
      <ConsoleScriptEdit :edit="edit" />
    </el-drawer>
  </section>
</template>

<script>
import axios from "axios";
import { deepClone } from "../../js/common";
import ConsoleScriptButtons from "./ConsoleScriptButtons";
import ConsoleScriptEdit from "./ConsoleScriptEdit";
const api = {
  subSystemScript: "/script/subSystemScript",
  run: "/script/run",
  terminate: "/script/terminate",
  runOutput: "/script/runOutput",
  edit: "/script/edit",
  saveOutput: "/script/saveOutput",
  getLogs: "/script/getLogs",
  extraButtonScriptRun: "/script/extraButtonScriptRun"
};
export default {
  name: "ConsoleScriptDetail",
  components: {
    ConsoleScriptButtons,
    ConsoleScriptEdit
  },
  props: {
    user_id: Number,
    systemId: Number,
    activeScriptName: String
  },
  watch: {
    systemId(newVal, oldVal) {
      this.systemIdChanged(newVal);
    },
    activeTab(newVal, oldVal) {
      this.activeTabChanged(newVal);
    },
    activeScriptName(newVal, oldVal) {
      console.log(newVal);
      this.activeTab = newVal;
    }
  },
  data() {
    return {
      activeTab: "", //当前触发的tab名称
      activeTabIndex: 0, //当前触发的tab的index
      activeScriptId: 0, //当前触发的脚本的id
      formData: [],
      extra_button: {
        visible: false,
        output: "",
        buttonLoading: false,
        loading: false,
        output_temp: ""
      },
      output: {
        canBeTerminate: false,
        loading: false,
        log_id: 0,
        logs: [],
        visible: false,
        text: "",
        important_fields: [],
        isAlert: false,
        scrollInit: true
      },
      edit: {
        buttonLoading: false,
        dialogTitle: "编辑",
        id: 0,
        sub_system_id: 0,
        title: "",
        start_folder: "",
        start_script: "",
        type: 0,
        visible: false,
        typeOptions: [
          {
            label: "输入框",
            value: "input"
          },
          {
            label: "选择器",
            value: "select"
          },
          {
            label: "日期",
            value: "date"
          },
          {
            label: "日期范围",
            value: "dateRange"
          }
        ],
        boolOptions: [
          {
            label: "是",
            value: 1
          },
          {
            label: "否",
            value: 0
          }
        ],
        formData: []
      },
      submitButtonLoading: false
    };
  },
  methods: {
    singleDataReplay(singleForm) {
      this.formData[this.activeTabIndex] = singleForm;
    },
    singleDataLog(output) {
      this.output.visible = true;
      this.output.text = output;
      if (this.output.scrollInit) {
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
        this.output.scrollInit = false;
      }
    },
    singleDataDeleted() {
      this.systemIdChanged(this.systemId);
    },
    activeTabChanged(newVal) {
      for (let x = 0; x < this.formData.length; x++) {
        if (this.formData[x].title == newVal) {
          this.activeTabIndex = x;
          this.activeScriptId = this.formData[x].id;
          break;
        }
      }
    },
    async systemIdChanged(val) {
      if (val == "") {
        return;
      }
      await this.subSystemScript(val);
      this.activeTab = this.formData[0]["title"];
      this.$emit("formData", this.formData);
    },
    //展示栏目下的脚本
    async subSystemScript(systemId) {
      this.formDataLoading = true;
      try {
        const { data: res } = await axios.post(api.subSystemScript, {
          user_id: this.user_id,
          sub_system_id: systemId
        });
        this.formData = [];
        for (let d = 0; d < res.data.length; d++) {
          this.formData.push({
            title: res.data[d]["name"],
            id: res.data[d]["id"],
            start_folder: res.data[d]["start_folder"],
            start_script: res.data[d]["start_script"],
            runs: res.data[d]["runs"],
            user: res.data[d]["user"],
            update_time: res.data[d]["update_time"],
            version: res.data[d]["version"],
            update_time: res.data[d]["update_time"],
            type: res.data[d]["type"],
            sub_system_id: res.data[d]["sub_system_id"],
            formDataDetail: []
          });
          for (var t = 0; t < res.data[d]["detail"].length; t++) {
            this.formData[this.formData.length - 1]["formDataDetail"].push({
              type: res.data[d]["detail"][t]["type"],
              label: res.data[d]["detail"][t]["label"],
              value: res.data[d]["detail"][t]["value"],
              placeHolder: res.data[d]["detail"][t]["place_holder"],
              options: res.data[d]["detail"][t]["options"],
              createable: res.data[d]["detail"][t]["createable"],
              disabled: res.data[d]["detail"][t]["disabled"],
              remark: res.data[d]["detail"][t]["remark"],
              is_important: res.data[d]["detail"][t]["is_important"],
              visible: res.data[d]["detail"][t]["visible"],
              extra_button: res.data[d]["detail"][t]["extra_button"],
              extra_button_label:
                res.data[d]["detail"][t]["extra_button_label"],
              extra_button_script:
                res.data[d]["detail"][t]["extra_button_script"],
              version: res.data[d]["detail"][t]["version"]
            });
          }
        }
        this.formDataLoading = false;
        return this.formData;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //展示编辑脚本dialog
    singleDataSetting() {
      this.subSystemScript(this.systemId).then(data => {
        this.edit.dialogTitle = "编辑脚本";
        this.edit.title = data[this.activeTabIndex].title;
        this.edit.id = data[this.activeTabIndex].id;
        this.edit.start_folder = data[this.activeTabIndex].start_folder;
        this.edit.start_script = data[this.activeTabIndex].start_script;
        this.edit.type = String(data[this.activeTabIndex].type);
        this.edit.formData = data[this.activeTabIndex].formDataDetail;
        this.edit.sub_system_id = data[this.activeTabIndex].sub_system_id;
        this.edit.visible = true;
      });
    },
    //使用当前激活tab的detial，接收start_command和组装方式，组装好command和detail并返回，start_command在运行脚本时为打开文件夹的命令加上起始命令
    command_get(start_command, type) {
      var command = "";
      var detail = {};
      //console.log(this.activeTab)
      if (type == "1") {
        //顺序模式
        for (
          var x = 0;
          x < this.formData[this.activeTab].formDataDetail.length;
          x++
        ) {
          //console.log(this.formData[this.activeTab].formDataDetail[x].type)
          detail[
            this.formData[this.activeTab].formDataDetail[x].label
          ] = this.formData[this.activeTab].formDataDetail[x].value;
          if (
            this.formData[this.activeTab].formDataDetail[x].type == "dateRange"
          ) {
            if (this.formData[this.activeTab].formDataDetail[x].value == null) {
              //解决用户点击了组建上的清空按钮后导致前端报错的问题
              continue;
            }
            for (
              let d = 0;
              d < this.formData[this.activeTab].formDataDetail[x].value.length;
              d++
            ) {
              command =
                command +
                " " +
                this.formData[this.activeTab].formDataDetail[x].value[d];
            }
            continue;
          }
          command =
            command +
            " " +
            this.formData[this.activeTab].formDataDetail[x].value;
        }
        command = start_command + command;
        //console.log(command)
      } else if (type == "2") {
        //替换模式
        var tempCommand = start_command;
        for (
          var x = 0;
          x < this.formData[this.activeTab].formDataDetail.length;
          x++
        ) {
          detail[
            this.formData[this.activeTab].formDataDetail[x].label
          ] = this.formData[this.activeTab].formDataDetail[x].value;
          if (
            this.formData[this.activeTab].formDataDetail[x].type == "dateRange"
          ) {
            if (this.formData[this.activeTab].formDataDetail[x].value == null) {
              //解决用户点击了组建上的清空按钮后导致前端报错的问题
              continue;
            }
            var tempDateRange = "";
            for (
              let d = 0;
              d < this.formData[this.activeTab].formDataDetail[x].value.length;
              d++
            ) {
              tempDateRange =
                tempDateRange +
                " " +
                this.formData[this.activeTab].formDataDetail[x].value[d];
            }
            var reg = new RegExp(
              "%" + this.formData[this.activeTab].formDataDetail[x].label + "%",
              "g"
            );
            tempCommand = tempCommand.replace(reg, tempDateRange);
            continue;
          }
          var reg = new RegExp(
            "%" + this.formData[this.activeTab].formDataDetail[x].label + "%",
            "g"
          );
          tempCommand = tempCommand.replace(
            reg,
            this.formData[this.activeTab].formDataDetail[x].value
          );
        }
        command = tempCommand;
      }
      var temp = {
        command: command,
        detail: detail
      };
      return temp;
    },
    //关闭运行窗口
    outputDialogClose(done) {
      if (this.output.isAlert) {
        this.$confirm(
          "在运行中关闭运行窗口会导致运行日志保存不完整，仍然要关闭吗?",
          "提示",
          {}
        ).then(_ => {
          this.output.text = "";
          done();
        });
      } else {
        this.output.text = "";
        done();
      }
    }
  }
};
</script>

<style>
</style>
