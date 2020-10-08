<template>
  <section>
    <el-card class="right-side-box-card" v-loading="formDataLoading">
      <el-row>
        <div class="info-text" v-show="formData.length==0">
          <i class="el-icon-back"></i>
          <div>请选择左侧系统</div>
        </div>
        <el-tabs v-model="activeTab" addable @tab-add="newScript" v-show="formData.length!=0">
          <el-tab-pane
            v-for="(singleForm,singleFormIndex) in formData"
            :key="singleForm.key"
            :label="singleForm.title"
            :name="singleForm.id"
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
              <ScriptButtons
                :user_id="user_id"
                :singleForm="singleForm"
                @replay="singleDataReplay"
                @output="singleDataLog"
                @deleted="flush"
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
      <ScriptEdit :user_id="user_id" :edit="edit" @done="flush" />
    </el-drawer>
  </section>
</template>

<script>
import axios from "axios";
import md5 from "js-md5";
import BScroll from "better-scroll";
import ScriptButtons from "./ScriptButtons";
import ScriptEdit from "./ScriptEdit";
const api = {
  subSystemScript: "/script/subSystemScript",
  run: "/script/run",
  terminate: "/script/terminate",
  runOutput: "/script/runOutput",
  edit: "/script/edit",
  saveOutput: "/script/saveOutput",
  extraButtonScriptRun: "/script/extraButtonScriptRun",
};
export default {
  name: "ConsoleScriptDetail",
  components: {
    ScriptButtons,
    ScriptEdit,
  },
  props: {
    user_id: Number,
    systemId: Number,
    newTabBool: Boolean,
    activeScriptName: String,
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
    },
    newTabBool(newVal, oldVal) {
      if (newVal && !oldVal) {
        this.newScript();
      }
    },
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
        output_temp: "",
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
        scrollInit: true,
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
            value: "input",
          },
          {
            label: "选择器",
            value: "select",
          },
          {
            label: "日期",
            value: "date",
          },
          {
            label: "日期范围",
            value: "dateRange",
          },
        ],
        boolOptions: [
          {
            label: "是",
            value: 1,
          },
          {
            label: "否",
            value: 0,
          },
        ],
        formData: [],
      },
      submitButtonLoading: false,
    };
  },
  methods: {
    //新增脚本
    newScript() {
      this.edit.dialogTitle = "新增脚本";
      this.edit.sub_system_id = this.systemId;
      this.edit.id = 0;
      this.edit.visible = true;
    },
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
                interactive: true,
              },
              momentumLimitDistance: 300,
              mouseWheel: true,
              preventDefault: false,
            });
            scroll.refresh();
          } catch (error) {
            console.log("滚动条设置失败" + error);
          }
        });
        this.output.scrollInit = false;
      }
    },
    flush() {
      this.systemIdChanged(this.systemId);
    },
    activeTabChanged(newVal) {
      for (let x = 0; x < this.formData.length; x++) {
        if (this.formData[x].id == newVal) {
          this.activeTabIndex = x;
          this.activeScriptId = Number(newVal);
          break;
        }
      }
    },
    async systemIdChanged(val) {
      if (val == "") {
        return;
      }
      await this.subSystemScript(val);
      if (this.formData.length != 0) {
        this.activeTab = this.formData[0].id;
      }
      this.$emit("formData", this.formData);
    },
    //展示栏目下的脚本
    async subSystemScript(systemId) {
      this.formDataLoading = true;
      try {
        const { data: res } = await axios.post(api.subSystemScript, {
          user_id: this.user_id,
          sub_system_id: systemId,
        });
        this.formData = [];
        //这里有一个坑，当以数字作为el-tab-panel的name时，tab下方标识当前被触发tab的横条不能被正确计算并显示，所以要将el-tab-panel的name转化为字符串
        for (let d = 0; d < res.data.length; d++) {
          this.formData.push({
            title: res.data[d]["name"],
            id: String(res.data[d]["id"]),
            start_folder: res.data[d]["start_folder"],
            start_script: res.data[d]["start_script"],
            runs: res.data[d]["runs"],
            user: res.data[d]["user"],
            update_time: res.data[d]["update_time"],
            version: res.data[d]["version"],
            update_time: res.data[d]["update_time"],
            type: res.data[d]["type"],
            sub_system_id: res.data[d]["sub_system_id"],
            formDataDetail: [],
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
              version: res.data[d]["detail"][t]["version"],
            });
          }
        }
        this.formDataLoading = false;
        return this.formData;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    //展示编辑脚本dialog
    singleDataSetting() {
      this.subSystemScript(this.systemId).then((data) => {
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
    //编辑窗口关闭
    editFormClosed() {
      this.edit.dialogTitle = "编辑";
      this.edit.id = 0;
      this.edit.title = "";
      this.edit.start_folder = "";
      this.edit.start_script = "";
      this.edit.type = 1;
      this.edit.formData = [];
    },
    //额外脚本提交
    extraButtonClicked(singleFormIndex, singleDataIndex, extra_button_command) {
      if (this.extra_button.visible) {
        this.extra_button.visible = false;
        return;
      }
      this.extra_button.output = "";
      this.extra_button.output_temp = "";
      this.extra_button.buttonLoading = true;
      var command_get_result = this.command_get(extra_button_command, 2);
      var command = command_get_result.command;
      this.extra_button.loading = true;
      try {
        axios
          .post(api.extraButtonScriptRun, {
            user_id: this.user_id,
            command: command,
          })
          .then((res) => {
            if (res.data.data["process_id"] == -1) {
              this.$message({
                message: "任务创建错误，请联系管理员！",
                type: "error",
              });
            } else {
              var process_id = res.data.data["process_id"];
            }
            this.extraButtonFlushOutput(
              singleFormIndex,
              singleDataIndex,
              process_id
            );
          });
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },

    //额外脚本输出
    extraButtonFlushOutput(singleFormIndex, singleDataIndex, process_id) {
      try {
        axios
          .post(api.runOutput, {
            process_id: process_id,
            user_id: this.user_id,
          })
          .then((res) => {
            if (res.data.data["status"] == -1) {
              this.$message({
                message: data["msg"],
                type: "error",
              });
              this.extra_button.loading = false;
              this.extra_button.buttonLoading = false;
              return;
            } else if (res.data.data["status"] == 0) {
              try {
                var dataTemp = JSON.parse(
                  this.extra_button.output_temp + res.data.data["output"]
                );
                this.extra_button.output = dataTemp.data.msg
                  .replace(/\n/g, "<br>")
                  .replace(/\s/g, "&nbsp;");
                if (dataTemp.data.value != undefined) {
                  this.formData[singleFormIndex].formDataDetail[
                    singleDataIndex
                  ].value = dataTemp.data.value;
                }
                if (dataTemp.data.options != undefined) {
                  this.formData[singleFormIndex].formDataDetail[
                    singleDataIndex
                  ].options = dataTemp.data.options;
                }
              } catch (err) {
                this.extra_button.output = (
                  this.extra_button.output_temp + res.data.data["output"]
                )
                  .replace(/\n/g, "<br>")
                  .replace(/\s/g, "&nbsp;");
              }
              this.extra_button.loading = false;
              this.extra_button.buttonLoading = false;
              return;
            } else if (res.data.data["status"] == 1) {
              this.extra_button.output_temp =
                this.extra_button.output_temp + res.data.data["output"];
              this.extraButtonFlushOutput(
                singleFormIndex,
                singleDataIndex,
                process_id
              );
            }
          });
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    //提交
    submit() {
      this.submitButtonLoading = true;
      var start_folder_with_start_script =
        "cd " +
        this.formData[this.activeTabIndex].start_folder +
        " && " +
        this.formData[this.activeTabIndex].start_script;
      var command_get_result = this.command_get(
        start_folder_with_start_script,
        this.formData[this.activeTabIndex].type
      );

      var command = command_get_result.command;
      var salt = Math.floor(Math.random() * 100000000000000);
      var sign = md5(
        this.formData[this.activeTabIndex].id +
          this.$cookies.get("user_id") +
          this.$cookies.get("user_key") +
          salt +
          command
      );

      try {
        axios
          .post(api.run, {
            id: this.formData[this.activeTabIndex].id,
            command: command,
            version: this.formData[this.activeTabIndex].version,
            detail: command_get_result.detail,
            user_id: this.user_id,
            salt: salt,
            sign: sign,
          })
          .then((res) => {
            if (res.data.data["process_id"] == -1) {
              this.$message({
                message: "任务创建错误，请联系管理员！",
                type: "error",
              });
            } else {
              this.output.log_id = res.data.data["log_id"];
              this.output.visible = true;
              this.output.text = command + "<br>";
              this.output.process_id = res.data.data["process_id"];
              this.output.canBeTerminate = true;
              this.flushOutput(res.data.data["process_id"]);
            }
          });
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    //运行中途停止运行
    async terminate() {
      this.$confirm("确定要停止运行吗?", "提示", {}).then(async () => {
        try {
          const { data: res } = await axios.post(api.terminate, {
            user_id: this.user_id,
            process_id: this.output.process_id,
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
      });
    },
    //更新输出
    flushOutput(process_id) {
      this.output.isAlert = true;
      try {
        axios
          .post(api.runOutput, {
            process_id: process_id,
            user_id: this.user_id,
          })
          .then((res) => {
            if (res.data.data["status"] == -1) {
              this.$message({
                message: data["msg"],
                type: "error",
              });
              this.submitButtonLoading = false;
              return;
            } else if (res.data.data["status"] == 0) {
              this.output.canBeTerminate = false;
              this.output.isAlert = false;
              this.output.text =
                "<div>" +
                this.output.text +
                "</div>" +
                res.data.data["output"]
                  .replace(/\n/g, "<br>")
                  .replace(/\s/g, "&nbsp;");
              this.output.text = this.output.text.replace(/#&nbsp;/g, " ");
              this.$message({
                message: "运行结束，请查看输出。",
                type: "success",
              });
              this.$nextTick(() => {
                let scroll = new BScroll(this.$refs.outputDialog, {
                  scrollY: true,
                  scrollbar: {
                    fade: true, // node_modules\better-scroll\dist\bscroll.esm.js:2345可以调时间，目前使用的是'var time = visible ? 500 : 5000;'
                    interactive: true,
                  },
                  momentumLimitDistance: 300,
                  mouseWheel: true,
                  preventDefault: false,
                });
                scroll.scrollTo(0, scroll.maxScrollY);
              });
              try {
                axios
                  .post(api.saveOutput, {
                    log_id: this.output.log_id,
                    output: this.output.text,
                  })
                  .then((res) => {
                    this.submitButtonLoading = false;
                  });
              } catch (e) {
                console.log(e);
                this.$message({
                  message:
                    "记录运行日志错误！请联系管理员" + e.response.data.msg,
                  type: "error",
                });
              }
              return;
            } else if (res.data.data["status"] == 1) {
              this.output.text =
                this.output.text +
                res.data.data["output"]
                  .replace(/\n/g, "<br>")
                  .replace(/\s/g, "&nbsp;");
              this.$nextTick(() => {
                try {
                  let scroll = new BScroll(this.$refs.outputDialog, {
                    scrollY: true,
                    scrollbar: {
                      fade: true, // node_modules\better-scroll\dist\bscroll.esm.js:2345可以调时间，目前使用的是'var time = visible ? 500 : 5000;'
                      interactive: true,
                    },
                    momentumLimitDistance: 300,
                    mouseWheel: true,
                    preventDefault: false,
                  });
                  scroll.scrollTo(0, scroll.maxScrollY);
                  scroll.destroy();
                } catch (error) {
                  console.log("滚动条设置失败" + error);
                }
              });
              this.flushOutput(process_id);
            }
          });
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    //使用当前激活tab的detial，接收start_command和组装方式，组装好command和detail并返回，start_command在运行脚本时为打开文件夹的命令加上起始命令
    command_get(start_command, type) {
      var command = "";
      var detail = [];
      if (type == "1") {
        //顺序模式
        for (
          var x = 0;
          x < this.formData[this.activeTabIndex].formDataDetail.length;
          x++
        ) {
          let _singleDetail = this.formData[this.activeTabIndex].formDataDetail[
            x
          ];
          detail.push({});
          detail[detail.length - 1].type = _singleDetail.type;
          detail[detail.length - 1].label = _singleDetail.label;
          detail[detail.length - 1].value = _singleDetail.value;
          if (detail[detail.length - 1].type == "select") {
            for (var l in _singleDetail.options) {
              if (
                _singleDetail.options[l].value ==
                detail[detail.length - 1].value
              ) {
                detail[detail.length - 1].optionLabel =
                  _singleDetail.options[l].label;
                break;
              }
            }
          }
          if (_singleDetail.type == "dateRange") {
            if (_singleDetail.value == null) {
              //解决用户点击了组建上的清空按钮后导致前端报错的问题
              continue;
            }
            for (let d = 0; d < _singleDetail.value.length; d++) {
              command = command + " " + _singleDetail.value[d];
            }
            continue;
          }
          command = command + " " + _singleDetail.value;
        }
        command = start_command + command;
        //console.log(command)
      } else if (type == "2") {
        //替换模式
        var tempCommand = start_command;
        for (
          var x = 0;
          x < this.formData[this.activeTabIndex].formDataDetail.length;
          x++
        ) {
          let _singleDetail = this.formData[this.activeTabIndex].formDataDetail[
            x
          ];
          detail.push({});
          detail[detail.length - 1].type = _singleDetail.type;
          detail[detail.length - 1].label = _singleDetail.label;
          detail[detail.length - 1].value = _singleDetail.value;
          if (detail[detail.length - 1].type == "select") {
            for (var l in _singleDetail.options) {
              if (
                _singleDetail.options[l].value ==
                detail[detail.length - 1].value
              ) {
                detail[detail.length - 1].optionLabel =
                  _singleDetail.options[l].label;
                break;
              }
            }
          }
          if (_singleDetail.type == "dateRange") {
            if (_singleDetail.value == null) {
              //解决用户点击了组建上的清空按钮后导致前端报错的问题
              continue;
            }
            var tempDateRange = "";
            for (let d = 0; d < _singleDetail.value.length; d++) {
              tempDateRange = tempDateRange + " " + _singleDetail.value[d];
            }
            var reg = new RegExp("%" + _singleDetail.label + "%", "g");
            tempCommand = tempCommand.replace(reg, tempDateRange);
            continue;
          }
          var reg = new RegExp("%" + _singleDetail.label + "%", "g");
          tempCommand = tempCommand.replace(reg, _singleDetail.value);
        }
        command = tempCommand;
      }
      var temp = {
        command: command,
        detail: detail,
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
        ).then((_) => {
          this.output.text = "";
          done();
        });
      } else {
        this.output.text = "";
        done();
      }
    },
  },
};
</script>

<style>
</style>
