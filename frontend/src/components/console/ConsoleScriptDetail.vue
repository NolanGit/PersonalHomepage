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
                :scriptId="activeScriptId"
                :singleForm="singleForm"
              />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-row>
      <!--底部按钮-->
      <el-row style="margin-top:60px;margin-left:10;margin-right:10px;">
        <ConsoleScriptRun />
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
import ConsoleScriptButtons from "./ConsoleScriptButtons";
import ConsoleScriptRun from "./ConsoleScriptRun";
const api = {
  subSystemScript: "/script/subSystemScript",
  run: "/script/run",
  terminate: "/script/terminate",
  runOutput: "/script/runOutput",
  edit: "/script/edit",
  replay: "/script/replay",
  delete: "/script/delete",
  saveOutput: "/script/saveOutput",
  getLogs: "/script/getLogs",
  getNewestLog: "/script/getNewestLog",
  schedule: "/script/schedule",
  scheduleAdd: "/script/scheduleEdit",
  scheduleDelete: "/script/scheduleDelete",
  extraButtonScriptRun: "/script/extraButtonScriptRun"
};
export default {
  name: "ConsoleScriptDetail",
  components: {
    ConsoleScriptButtons,
    ConsoleScriptRun
  },
  props: {
    user_id: Number,
    systemId: Number
  },
  watch: {
    systemId(newVal, oldVal) {
      this.systemIdChanged(newVal);
    },
    activeTab(newVal, oldVal) {
      this.activeTabChanged(newVal);
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
      }
    };
  },
  methods: {
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
        console.log(this.formData);
        return this.formData;
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
