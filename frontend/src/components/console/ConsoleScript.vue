<template>
  <section>
    <el-row class="main-row margin_bottom-medium" :gutter="20">
      <el-col :span="5" class="lift-side-bar">
        <el-card class="left-side-box-card">
          <el-collapse v-model="activeSystem" @change="handleChange" accordion>
            <el-collapse-item
              v-for="singleSystem in subSystem"
              :key="singleSystem.key"
              :title="singleSystem.title"
              :name="singleSystem.title"
            >
              <div
                class="collapse-div"
                v-show="singleSystem.scriptText!=''"
              >包括：{{singleSystem.scriptText}}</div>
              <div class="collapse-div" v-show="formData.length==0">本系统暂无脚本</div>
              <el-button type="text" v-show="formData.length==0" size="small" @click="newTab">需要新增？</el-button>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-col>
      <el-col :span="19" class="right-side-bar">
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
                  <el-tooltip
                    class="noMargin"
                    effect="dark"
                    content="查看最近一次由我运行的日志"
                    placement="top"
                  >
                    <el-button
                      class="noMargin"
                      type="primary"
                      plain
                      icon="el-icon-tickets"
                      circle
                      @click="singleDataLog()"
                    ></el-button>
                  </el-tooltip>
                  <el-tooltip
                    class="question-mark"
                    effect="dark"
                    content="查看最近50次运行记录"
                    placement="top"
                  >
                    <el-popover placement="left" width="1010" trigger="click">
                      <div class="scrollbar-div max-height-medium" ref="scrollbarDiv">
                        <el-table
                          size="small"
                          :data="output.logs"
                          stripe
                          v-loading="output.loading"
                        >
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
                        <el-table-column width="80" property="user" label="创建人"></el-table-column>
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
                      <div
                        class="add"
                        style="width: 99.87%;"
                        @click="schedule.dialogVisible = true"
                      >
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
      </el-col>
    </el-row>

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
      <div class="edit-form-card margin_left-medium margin_right-medium">
        <div class="scrollbar-div max-height-large padding-right-19" ref="scrollbarDiv">
          <el-card shadow="never">
            <div class="margin_bottom-medium">
              <el-card>
                <div>
                  <td type="flex" class="td--label">
                    <p class="td__p--label">脚本名称：</p>
                  </td>
                  <td>
                    <el-tooltip
                      open-delay="1000"
                      effect="dark"
                      :content="edit.title"
                      placement="top"
                    >
                      <el-input
                        size="small"
                        v-model="edit.title"
                        placeholder="请输入名称"
                        class="main_input--large"
                      ></el-input>
                    </el-tooltip>
                  </td>
                </div>
                <div>
                  <td type="flex" class="td--label">
                    <p class="td__p--label">起始文件夹：</p>
                  </td>
                  <td>
                    <el-tooltip
                      open-delay="1000"
                      effect="dark"
                      :content="edit.start_folder"
                      placement="top"
                    >
                      <el-input
                        size="small"
                        v-model="edit.start_folder"
                        placeholder="请输入起始文件夹"
                        class="main_input--large"
                      ></el-input>
                    </el-tooltip>
                  </td>
                </div>
                <div>
                  <td type="flex" class="td--label">
                    <p class="td__p--label">起始脚本：</p>
                  </td>
                  <td>
                    <el-tooltip
                      open-delay="1000"
                      effect="dark"
                      :content="edit.start_script"
                      placement="top"
                    >
                      <el-input
                        size="small"
                        v-model="edit.start_script"
                        placeholder="请输入起始脚本"
                        class="main_input--large"
                      ></el-input>
                    </el-tooltip>
                  </td>
                </div>
                <div>
                  <td type="flex" class="td--label">
                    <p class="td__p--label">组合方式：</p>
                  </td>
                  <td>
                    <div>
                      <td class="dialog-type-order">
                        <el-radio v-model="edit.type" label="1">顺序</el-radio>
                      </td>
                      <td class="dialog-type-tooltip">
                        <el-tooltip
                          class="question-mark"
                          effect="dark"
                          content="顺序组合组件值来生成脚本"
                          placement="top"
                        >
                          <i class="fa fa-question-circle-o"></i>
                        </el-tooltip>
                      </td>
                      <td class="dialog-type-replace">
                        <el-radio v-model="edit.type" label="2">替换</el-radio>
                      </td>
                      <td class="dialog-type-tooltip">
                        <el-tooltip
                          class="question-mark"
                          effect="dark"
                          content="使用组件值替换起始脚本中格式为'%组件名称%'的字段来生成脚本"
                          placement="top"
                        >
                          <i class="fa fa-question-circle-o"></i>
                        </el-tooltip>
                      </td>
                    </div>
                  </td>
                </div>
              </el-card>
            </div>
            <div v-for="singleData in edit.formData" :key="singleData.key">
              <div class="margin_bottom-medium">
                <el-card class="edit-form-card">
                  <el-col :span="21">
                    <div>
                      <td type="flex" class="td--label">
                        <p class="td__p--label">组件名称：</p>
                      </td>
                      <td>
                        <el-input
                          size="small"
                          v-model="singleData.label"
                          placeholder="请输入组件名称"
                          class="main_input--large"
                        ></el-input>
                      </td>
                    </div>
                    <div>
                      <td type="flex" class="td--label">
                        <p class="td__p--label">组件类型：</p>
                      </td>
                      <td>
                        <el-select
                          size="small"
                          v-model="singleData.type"
                          placeholder="请选择组件类型"
                          filterable
                          default-first-option
                          class="main_select--large"
                        >
                          <el-option
                            v-for="item in edit.typeOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          ></el-option>
                        </el-select>
                      </td>
                    </div>
                    <div v-if="singleData.type=='select'">
                      <td type="flex" class="td--label">
                        <p class="td__p--label">选项：</p>
                      </td>
                      <td>
                        <el-button
                          size="small"
                          @click.native="singleDataOptionDialogClicked(edit.formData.indexOf(singleData),singleData.options)"
                        >编辑选项</el-button>
                      </td>
                    </div>
                    <div v-if="singleData.type=='select'">
                      <td type="flex" class="td--label">
                        <p class="td__p--label">是否可创建选项：</p>
                      </td>
                      <td>
                        <el-select
                          size="small"
                          v-model="singleData.createable"
                          placeholder="不选择时为否"
                          filterable
                          default-first-option
                          class="main_select--large"
                        >
                          <el-option
                            v-for="item in edit.boolOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          ></el-option>
                        </el-select>
                      </td>
                    </div>
                    <div v-if="singleData.type!='date'&&singleData.type!='dateRange'">
                      <td type="flex" class="td--label">
                        <p class="td__p--label">默认值：</p>
                      </td>
                      <td v-if="singleData.type!='select'">
                        <el-tooltip
                          open-delay="1000"
                          effect="dark"
                          :content="singleData.value"
                          placement="top"
                        >
                          <el-input
                            size="small"
                            v-model="singleData.value"
                            placeholder="如无默认值可以留空"
                            class="main_input--large"
                          ></el-input>
                        </el-tooltip>
                      </td>
                      <td v-if="singleData.type=='select'">
                        <el-tooltip
                          open-delay="1000"
                          effect="dark"
                          :content="singleData.value"
                          placement="top"
                        >
                          <el-input
                            size="small"
                            v-model="singleData.value"
                            placeholder="请输入选项中的'值'作为默认值，如无默认值可留空"
                            class="main_input--large"
                          ></el-input>
                        </el-tooltip>
                      </td>
                      <td v-if="singleData.type=='select'">
                        <el-tooltip
                          class="edit-form-question-mark question-mark"
                          effect="dark"
                          content="注意：如选择器有默认值，需要填写的是选项中的'值'，而非'标签'"
                          placement="top"
                        >
                          <i class="fa fa-question-circle-o"></i>
                        </el-tooltip>
                      </td>
                    </div>
                    <div>
                      <td type="flex" class="td--label">
                        <p class="td__p--label">是否只读：</p>
                      </td>
                      <td>
                        <el-select
                          size="small"
                          v-model="singleData.disabled"
                          placeholder="不选择时为否"
                          filterable
                          default-first-option
                          class="main_select--large"
                        >
                          <el-option
                            v-for="item in edit.boolOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          ></el-option>
                        </el-select>
                      </td>
                    </div>
                    <div v-if="singleData.type!='dateRange'">
                      <td type="flex" class="td--label">
                        <p class="td__p--label">占位文字：</p>
                      </td>
                      <td>
                        <el-tooltip
                          open-delay="1000"
                          effect="dark"
                          :content="singleData.placeHolder"
                          placement="top"
                        >
                          <el-input
                            size="small"
                            v-model="singleData.placeHolder"
                            placeholder="如无占位文字可以留空"
                            class="main_input--large"
                          ></el-input>
                        </el-tooltip>
                      </td>
                    </div>
                    <div>
                      <td type="flex" class="td--label">
                        <p class="td__p--label">备注：</p>
                      </td>
                      <td>
                        <el-tooltip
                          open-delay="1000"
                          effect="dark"
                          :content="singleData.remark"
                          placement="top"
                        >
                          <el-input
                            size="small"
                            v-model="singleData.remark"
                            placeholder="如无备注可以留空"
                            class="main_input--large"
                          ></el-input>
                        </el-tooltip>
                      </td>
                    </div>
                    <div>
                      <td type="flex" class="td--label">
                        <p class="td__p--label">是否有额外按钮：</p>
                      </td>
                      <td>
                        <el-select
                          size="small"
                          v-model="singleData.extra_button"
                          placeholder="不选择时为否"
                          filterable
                          default-first-option
                          class="main_select--large"
                        >
                          <el-option
                            v-for="item in edit.boolOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          ></el-option>
                        </el-select>
                      </td>
                      <td>
                        <el-tooltip
                          class="edit-form-question-mark question-mark"
                          effect="dark"
                          content="额外按钮配置为'是'时，组件右侧会出现一个按钮，点击按钮可以运行'额外按钮运行脚本'的脚本"
                          placement="top"
                        >
                          <i class="fa fa-question-circle-o"></i>
                        </el-tooltip>
                      </td>
                    </div>
                    <div v-if="singleData.extra_button==1">
                      <td type="flex" class="td--label">
                        <p class="td__p--label">额外按钮名称：</p>
                      </td>
                      <td>
                        <el-tooltip
                          open-delay="1000"
                          effect="dark"
                          :content="singleData.extra_button_label"
                          placement="top"
                        >
                          <el-input
                            size="small"
                            v-model="singleData.extra_button_label"
                            placeholder="请输入额外按钮名称"
                            class="main_input--large"
                          ></el-input>
                        </el-tooltip>
                      </td>
                    </div>
                    <div v-if="singleData.extra_button==1">
                      <td type="flex" class="td--label">
                        <p class="td__p--label">额外按钮运行脚本：</p>
                      </td>
                      <td>
                        <el-tooltip
                          open-delay="1000"
                          effect="dark"
                          :content="singleData.extra_button_script"
                          placement="top"
                        >
                          <el-input
                            size="small"
                            v-model="singleData.extra_button_script"
                            placeholder="请输入额外按钮运行脚本"
                            class="main_input--large"
                          ></el-input>
                        </el-tooltip>
                      </td>
                      <td>
                        <el-tooltip
                          class="edit-form-question-mark question-mark"
                          effect="dark"
                          content="点击'额外按钮'可以运行此处填写的脚本，并将此处脚本的运行输出返回至页面"
                          placement="top"
                        >
                          <i class="fa fa-question-circle-o"></i>
                        </el-tooltip>
                      </td>
                    </div>
                    <div>
                      <td type="flex" class="td--label">
                        <p class="td__p--label">是否在列表展示：</p>
                      </td>
                      <td>
                        <el-select
                          size="small"
                          v-model="singleData.is_important"
                          placeholder="不选择时为否"
                          filterable
                          default-first-option
                          class="main_select--large"
                        >
                          <el-option
                            v-for="item in edit.boolOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          ></el-option>
                        </el-select>
                      </td>
                      <td>
                        <el-tooltip
                          class="edit-form-question-mark question-mark"
                          effect="dark"
                          content="选为是会将此组件使用单独的一列在运行记录中展示，建议不要设置太多列，否则会拖慢页面速度"
                          placement="top"
                        >
                          <i class="fa fa-question-circle-o"></i>
                        </el-tooltip>
                      </td>
                    </div>
                    <div>
                      <td type="flex" class="td--label">
                        <p class="td__p--label">是否显示：</p>
                      </td>
                      <td>
                        <el-select
                          size="small"
                          v-model="singleData.visible"
                          placeholder="不选择时为是"
                          filterable
                          default-first-option
                          class="main_select--large"
                        >
                          <el-option
                            v-for="item in edit.boolOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          ></el-option>
                        </el-select>
                      </td>
                      <td>
                        <el-tooltip
                          class="edit-form-question-mark question-mark"
                          effect="dark"
                          content="当选为'否'时，组件在页面上将不可见"
                          placement="top"
                        >
                          <i class="fa fa-question-circle-o"></i>
                        </el-tooltip>
                      </td>
                    </div>
                  </el-col>
                  <el-col :span="3">
                    <div class="editFormRightButtons">
                      <td>
                        <i
                          class="editFormRightButton editFormMoveUp el-icon-top"
                          @click="editFormMoveUp(edit.formData.indexOf(singleData))"
                        ></i>
                      </td>
                      <td>
                        <i
                          class="editFormRightButton editFormMoveDown el-icon-bottom"
                          @click="editFormMoveDown(edit.formData.indexOf(singleData))"
                        ></i>
                      </td>
                      <td>
                        <i
                          class="editFormRightButton editFormDeleted el-icon-close"
                          @click="editFormDeleted(edit.formData.indexOf(singleData))"
                        ></i>
                      </td>
                    </div>
                  </el-col>
                </el-card>
              </div>
            </div>
            <div class="add" style="width: 99.87%;" @click="editFormAddSingleData()">
              <span>+ 添加参数</span>
            </div>
          </el-card>
        </div>
        <div class="dialog-footer">
          <el-button size="small" @click.native="edit.visible=false">关闭</el-button>
          <el-button
            type="primary"
            size="small"
            :loading="edit.buttonLoading"
            @click.native="editFormSubmited()"
          >提交</el-button>
        </div>
      </div>
    </el-drawer>

    <!--选择器编辑选项界面-->
    <el-drawer
      title="编辑"
      :visible.sync="singleDataOptionDialog.visible"
      :close-on-click-modal="false"
      size="40%"
      @closed="singleDataOptionDialogClosed"
    >
      <div class="margin_left-medium margin_right-medium">
        <div v-for="singleDataOption in singleDataOptionDialog.data" :key="singleDataOption.key">
          <div>
            <td type="flex" class="td--label--short">
              <p class="td__p--label">标签：</p>
            </td>
            <td>
              <el-tooltip
                open-delay="1000"
                effect="dark"
                :content="singleDataOption.label"
                placement="top"
              >
                <el-input size="small" v-model="singleDataOption.label" placeholder="请输入选项展示文字"></el-input>
              </el-tooltip>
            </td>
            <td type="flex" class="td--label--short">
              <p class="singleDataOptionDialogValue">值：</p>
            </td>
            <td>
              <el-tooltip
                open-delay="1000"
                effect="dark"
                :content="singleDataOption.value"
                placement="top"
              >
                <el-input size="small" v-model="singleDataOption.value" placeholder="请输入选项实际的值"></el-input>
              </el-tooltip>
            </td>
            <td>
              <i
                class="singleDataOptionDialogDeleted el-icon-delete"
                @click="singleDataOptionDialogDeleted(singleDataOptionDialog.data.indexOf(singleDataOption))"
              ></i>
            </td>
          </div>
        </div>
        <div class="add" style="width: 99.87%;" @click="singleDataOptionDialogAddSingleData()">
          <span>+ 添加选项</span>
        </div>
        <div class="dialog-footer">
          <el-button size="small" @click="singleDataOptionDialog.visible = false">关闭</el-button>
          <el-button type="primary" size="small" @click="singleDataOptionDialogSubmited()">保存</el-button>
        </div>
      </div>
    </el-drawer>

    <!--编辑定时任务界面-->
    <el-drawer
      :title="schedule.label"
      :visible.sync="schedule.dialogVisible"
      :close-on-click-modal="false"
      size="40%"
      @closed="schedulenDialogClosed"
    >
      <div class="margin_left-medium margin_right-medium">
        <div>
          <td type="flex" class="td--label">
            <p class="td__p--label">定时运行时间：</p>
          </td>
          <td>
            <el-date-picker
              v-model="schedule.scheduleData.triggerDate"
              type="date"
              placeholder="选择日期时间"
              value-format="yyyy-MM-dd"
              size="small"
              class="main_select--medium"
            ></el-date-picker>
          </td>
          <td>
            <el-time-select
              v-model="schedule.scheduleData.triggerTime"
              :picker-options="{
              start: '00:00',
              step: '00:15',
              end: '24:00'
            }"
              placeholder="选择时间"
              size="small"
              class="main_select--medium"
            ></el-time-select>
          </td>
        </div>
        <div>
          <td type="flex" class="td--label">
            <p class="td__p--label">重复：</p>
          </td>
          <td>
            <el-switch
              v-model="schedule.scheduleData.is_automatic"
              false
              active-color="#3383BA"
              inactive-color="#80868C"
            ></el-switch>
          </td>
          <td v-show="schedule.scheduleData.is_automatic==true">
            <p class="inline_margin--medium">每</p>
          </td>
          <td v-show="schedule.scheduleData.is_automatic==true">
            <el-input
              v-model="schedule.scheduleData.interval.value"
              placeholder="请输入"
              size="small"
              class="main_input--tiny inline_margin--small"
            ></el-input>
          </td>
          <td v-show="schedule.scheduleData.is_automatic==true">
            <el-select
              v-model="schedule.scheduleData.interval.unit.select"
              placeholder="请选择"
              size="small"
              class="main_select--medium"
            >
              <el-option
                v-for="item in schedule.scheduleData.interval.unit.options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </td>
        </div>
        <div class="dialog-footer">
          <el-button size="small" @click="schedule.dialogVisible = false">关闭</el-button>
          <el-button type="primary" size="small" @click="scheduleAdd()">提交</el-button>
        </div>
      </div>
    </el-drawer>
  </section>
</template>

<script>
import axios from "axios";
import BScroll from "better-scroll";
import {
  consoleScriptRunOutput,
  consoleScriptSaveOutput,
  consoleScriptExtraButtonScriptRun
} from "../../api/console";
const api = {
  subSystem: "/script/subSystem",
  subSystemScript: "/script/subSystemScript",
  run: "/script/consoleScriptRun",
  terminate: "/script/consoleScriptTerminate",
  runOutput: "/script/consoleScriptRunOutput",
  edit: "/script/consoleScriptEdit",
  replay: "/script/consoleScriptReplay",
  delete: "/script/consoleScriptDelete",
  saveOutput: "/script/consoleScriptSaveOutput",
  getLogs: "/script/consoleScriptGetLogs",
  getNewestLog: "/script/consoleScriptGetNewestLog",
  schedule: "/script/consoleScriptSchedule",
  scheduleAdd: "/script/consoleScriptScheduleEdit",
  scheduleDelete: "/script/consoleScriptScheduleDelete",
  extraButtonScriptRun: "/script/consoleScriptExtraButtonScriptRun"
};
export default {
  name: "ConsoleScript",
  data() {
    return {
      pickerOptions: {
        shortcuts: [
          {
            text: "最近一周",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "最近一个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "最近三个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            }
          }
        ]
      },
      bool: {
        singleDataLog: true
      },
      activeTab: "0",
      activedSystem: 0,
      activeSystem: [],
      subSystem: [],
      formData: [],
      formDataLoading: false,
      submitButtonLoading: false,
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
      extra_button: {
        visible: false,
        output: "",
        buttonLoading: false,
        loading: false,
        output_temp: ""
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
      singleDataOptionDialog: {
        visible: false,
        index: 0,
        data: []
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
  methods: {
    deepClone(obj) {
      var _obj = JSON.stringify(obj),
        objClone = JSON.parse(_obj);
      return objClone;
    },
    swapItem(arr, index1, index2) {
      arr[index1] = arr.splice(index2, 1, arr[index1])[0];
      return arr;
    },
    handleChange(val) {
      if (val == "") {
        return;
      }
      for (var s = 0; s < this.subSystem.length; s++) {
        if (val == this.subSystem[s].title) {
          break;
        }
      }
      this.activedSystem = this.subSystem[s].id;
      this.activeTab = "0";
      this.subSystemScript(this.subSystem[s].id);
    },
    //获取系统信息
    async getSubSystem() {
      try {
        const { data: res } = await axios.get(api.subSystem, {
          user: sessionStorage.getItem("user").replace(/\"/g, "")
        });
        for (let x = 0; x < res.data.length; x++) {
          this.subSystem.push({
            id: res.data[x]["id"],
            title: res.data[x]["name"]
          });
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //展示子系统下的脚本
    async subSystemScript(sub_system_id) {
      this.formDataLoading = true;
      for (
        var subSystemIndex = 0;
        subSystemIndex < this.subSystem.length;
        subSystemIndex++
      ) {
        if (Number(sub_system_id) == this.subSystem[subSystemIndex].id) {
          break;
        }
      }
      try {
        const { data: res } = await axios.post(api.subSystemScript, {
          user: sessionStorage.getItem("user").replace(/\"/g, ""),
          sub_system_id: this.subSystem[subSystemIndex].id
        });
        this.formData = [];
        this.subSystem[subSystemIndex].script = [];
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
          this.subSystem[subSystemIndex].script.push(res.data[d]["name"]);
        }
        this.subSystem[subSystemIndex].scriptText = this.subSystem[
          subSystemIndex
        ].script.join("、");
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
    //提交
    submit() {
      this.submitButtonLoading = true;
      var start_folder_with_start_script =
        "cd " +
        this.formData[this.activeTab].start_folder +
        " && " +
        this.formData[this.activeTab].start_script;
      var command_get_result = this.command_get(
        start_folder_with_start_script,
        this.formData[this.activeTab].type
      );
      var command = command_get_result.command;
      try {
        const { data: res } = axios.post(api.run, {
          id: this.formData[this.activeTab].id,
          command: command,
          version: this.formData[this.activeTab].version,
          detail: command_get_result.detail,
          user: sessionStorage.getItem("user").replace(/\"/g, "")
        });
        if (res.data["process_id"] == -1) {
          this.$message({
            message: "任务创建错误，请联系管理员！",
            type: "error"
          });
        } else {
          this.output.log_id = res.data["log_id"];
          this.output.visible = true;
          this.output.text = command + "<br>";
          this.output.process_id = res.data["process_id"];
          this.output.canBeTerminate = true;
          this.flushOutput(res.data["process_id"]);
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //运行中途停止运行
    async terminate() {
      this.$confirm("确定要停止运行吗?", "提示", {}).then(async () => {
        try {
          const { data: res } = await axios.post(api.terminate, {
            user: sessionStorage.getItem("user").replace(/\"/g, ""),
            process_id: this.output.process_id
          });
          this.$message({
            message: res.msg,
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
    //编辑脚本提交
    async editFormSubmited() {
      this.edit.buttonLoading = true;
      try {
        const { data: res } = await axios.post(api.edit, {
          sub_system_id: this.edit.sub_system_id,
          script_id: this.edit.id,
          name: this.edit.title,
          start_folder: this.edit.start_folder,
          start_script: this.edit.start_script,
          type: Number(this.edit.type),
          detail: this.edit.formData,
          user: sessionStorage.getItem("user").replace(/\"/g, "")
        });
        this.$message({
          message: res.msg,
          type: "success"
        });
        this.edit.visible = false;
        this.subSystemScript(this.edit.sub_system_id);
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
      this.edit.buttonLoading = false;
    },
    //回放上一次由我运行的脚本参数
    async singleDataReplay() {
      try {
        const { data: res } = await axios.get(api.replay, {
          script_id: this.formData[this.activeTab].id,
          user: sessionStorage.getItem("user").replace(/\"/g, "")
        });
        if (this.formData[this.activeTab].version != res.data.version) {
          this.$message({
            message:
              "检测到脚本配置发生过修改(" +
              "V" +
              res.data.version +
              "→" +
              "V" +
              this.formData[this.activeTab].version +
              ")，可能无法完美恢复上一次参数",
            type: "info"
          });
        }
        for (
          var f = 0;
          f < this.formData[this.activeTab].formDataDetail.length;
          f++
        ) {
          try {
            this.formData[this.activeTab].formDataDetail[f].value =
              res.data.detail[
                this.formData[this.activeTab].formDataDetail[f].label
              ];
          } catch (err) {
            console.log(
              "[" +
                this.formData[this.activeTab].formDataDetail[f].label +
                "]" +
                "恢复失败：" +
                err
            );
          }
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //删除脚本
    async singleDataDelete() {
      this.$confirm("确认删除吗?", "提示", {})
        .then(async () => {
          try {
            const { data: res } = await axios.post(api.delete, {
              script_id: this.formData[this.activeTab].id,
              user: sessionStorage.getItem("user").replace(/\"/g, "")
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
    },
    //展示脚本的运行日志
    async singleDataShowLogs() {
      this.output.loading = true;
      this.output.logs = [];
      try {
        const { data: res } = await axios.post(api.getLogs, {
          script_id: this.formData[this.activeTab].id,
          user: sessionStorage.getItem("user").replace(/\"/g, "")
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
    //展示最近一次由我运行的脚本日志
    async singleDataLog() {
      try {
        const { data: res } = await axios.post(api.getNewestLog, {
          script_id: this.formData[this.activeTab].id,
          user: sessionStorage.getItem("user").replace(/\"/g, "")
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
    },
    //展示定时任务列表
    async scheduleShow() {
      this.schedule.loading = true;
      this.schedule.schedules = [];
      try {
        const { data: res } = await axios.post(api.schedule, {
          script_id: this.formData[this.activeTab].id,
          user: sessionStorage.getItem("user").replace(/\"/g, "")
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
        this.formData[this.activeTab].start_folder +
        " && " +
        this.formData[this.activeTab].start_script;
      var command_get_result = this.command_get(
        start_folder_with_start_script,
        this.formData[this.activeTab].type
      );
      var command = command_get_result.command;
      var detail = command_get_result.detail;
      try {
        const { data: res } = await axios.post(api.scheduleAdd, {
          user: sessionStorage.getItem("user").replace(/\"/g, ""),
          script_id: this.formData[this.activeTab].id,
          command: command,
          detail: detail,
          version: this.formData[this.activeTab].version,
          trigger_time:
            this.schedule.scheduleData.triggerDate +
            " " +
            this.schedule.scheduleData.triggerTime,
          is_automatic: this.schedule.scheduleData.is_automatic == true ? 1 : 0,
          interval_raw: Number(this.schedule.scheduleData.interval.value),
          interval_unit: this.schedule.scheduleData.interval.unit.select,
          schedule_id: this.schedule.scheduleData.schedule_id
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
    //删除定时任务
    async scheduleDelete(schedule_id) {
      this.$confirm("确认停止并删除定时任务吗?", "提示", {}).then(async () => {
        try {
          const { data: res } = await axios.post(api.scheduleDelete, {
            user: sessionStorage.getItem("user").replace(/\"/g, ""),
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

    // 以下为无接口交互函数
    //增加组件
    editFormAddSingleData() {
      this.edit.formData.push({
        type: "",
        label: "",
        value: "",
        placeHolder: "",
        options: "",
        createable: "",
        disabled: "",
        is_important: "",
        remark: ""
      });
    },
    //删除组件
    editFormDeleted(index) {
      this.edit.formData.splice(index, 1);
    },
    //上移
    editFormMoveUp(index) {
      if (index > 0) {
        this.swapItem(this.edit.formData, index, index - 1);
      } else {
        this.$message({
          message: "已经是第一位，不能再上移了哦",
          type: "info"
        });
      }
    },
    //下移
    editFormMoveDown(index) {
      if (index < this.edit.formData.length - 1) {
        this.swapItem(this.edit.formData, index, index + 1);
      } else {
        this.$message({
          message: "已经是最后一位，不能再下移了哦",
          type: "info"
        });
      }
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
    //选择器组件点击
    singleDataOptionDialogClicked(index, singleDataOptions) {
      this.singleDataOptionDialog.index = index;
      this.singleDataOptionDialog.visible = true;
      this.singleDataOptionDialog.data =
        singleDataOptions == "" ? [] : this.deepClone(singleDataOptions);
    },
    //选择器组件关闭
    singleDataOptionDialogClosed() {
      this.singleDataOptionDialog.data = [];
    },
    //选择器组件删除
    singleDataOptionDialogDeleted(index) {
      this.singleDataOptionDialog.data.splice(index, 1);
    },
    //选择器组件增加
    singleDataOptionDialogAddSingleData() {
      this.singleDataOptionDialog.data.push({
        label: "",
        value: ""
      });
    },
    //选择器组件提交
    singleDataOptionDialogSubmited() {
      this.edit.formData[
        this.singleDataOptionDialog.index
      ].options = this.singleDataOptionDialog.data;
      this.singleDataOptionDialog.visible = false;
    },
    //新增脚本
    newTab() {
      this.edit.dialogTitle = "新增脚本";
      this.edit.sub_system_id = this.subSystem[this.activedSystem - 1].id;
      this.edit.id = 0;
      this.edit.visible = true;
    },
    //展示编辑脚本dialog
    singleDataSetting() {
      this.subSystemScript(this.activedSystem).then(data => {
        this.edit.dialogTitle = "编辑脚本";
        this.edit.title = data[this.activeTab].title;
        this.edit.id = data[this.activeTab].id;
        this.edit.start_folder = data[this.activeTab].start_folder;
        this.edit.start_script = data[this.activeTab].start_script;
        this.edit.type = String(data[this.activeTab].type);
        this.edit.formData = data[this.activeTab].formDataDetail;
        this.edit.sub_system_id = data[this.activeTab].sub_system_id;
        this.edit.visible = true;
      });
    },
    //定时任务dialog关闭
    schedulenDialogClosed() {
      this.schedule.dialogVisible = false;
      this.schedule.scheduleData.triggerDate = "";
      this.schedule.scheduleData.triggerTime = "";
      this.schedule.scheduleData.is_automatic = false;
      this.schedule.scheduleData.schedule_id = 0;
      this.schedule.scheduleData.interval.value = 1;
      this.schedule.scheduleData.interval.unit.select = 2;
      this.schedule.label = "新建定时任务";
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
    //更新输出
    flushOutput(process_id) {
      this.output.isAlert = true;
      var para = {
        process_id: process_id,
        user: sessionStorage.getItem("user").replace(/\"/g, "")
      };
      consoleScriptRunOutput(para).then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          if (data["data"]["status"] == -1) {
            this.$message({
              message: data["msg"],
              type: "error"
            });
            this.submitButtonLoading = false;
            return;
          } else if (data["data"]["status"] == 0) {
            this.output.canBeTerminate = false;
            this.output.isAlert = false;
            this.output.text =
              "<div>" +
              this.output.text +
              "</div>" +
              data["data"]["output"]
                .replace(/\n/g, "<br>")
                .replace(/\s/g, "&nbsp;");
            this.output.text = this.output.text.replace(/#&nbsp;/g, " ");
            this.$message({
              message: "运行结束，请查看输出。",
              type: "success"
            });
            this.$nextTick(() => {
              let scroll = new BScroll(this.$refs.outputDialog, {
                scrollY: true,
                scrollbar: {
                  fade: true, // node_modules\better-scroll\dist\bscroll.esm.js:2345可以调时间，目前使用的是'var time = visible ? 500 : 5000;'
                  interactive: true
                },
                momentumLimitDistance: 300,
                mouseWheel: true,
                preventDefault: false
              });
              scroll.scrollTo(0, scroll.maxScrollY);
            });
            var para2 = {
              log_id: this.output.log_id,
              output: this.output.text
            };
            consoleScriptSaveOutput(para2).then(data => {
              if (data["data"]["status"] == -1) {
                this.$message({
                  message: "记录运行日志错误！请联系管理员" + data["msg"],
                  type: "error"
                });
              } else {
                this.submitButtonLoading = false;
              }
            });
            return;
          } else if (data["data"]["status"] == 1) {
            this.output.text =
              this.output.text +
              data["data"]["output"]
                .replace(/\n/g, "<br>")
                .replace(/\s/g, "&nbsp;");
            this.$nextTick(() => {
              try {
                let scroll = new BScroll(this.$refs.outputDialog, {
                  scrollY: true,
                  scrollbar: {
                    fade: true, // node_modules\better-scroll\dist\bscroll.esm.js:2345可以调时间，目前使用的是'var time = visible ? 500 : 5000;'
                    interactive: true
                  },
                  momentumLimitDistance: 300,
                  mouseWheel: true,
                  preventDefault: false
                });
                scroll.scrollTo(0, scroll.maxScrollY);
                scroll.destroy();
              } catch (error) {
                console.log("滚动条设置失败" + error);
              }
            });
            this.flushOutput(process_id);
          }
        }
      });
    },
    //展示日志中的输出
    log_output(output) {
      this.output.visible = true;
      this.output.text = output;
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
    },
    //回放日志中的参数
    log_replay(version, detail) {
      for (
        var f = 0;
        f < this.formData[this.activeTab].formDataDetail.length;
        f++
      ) {
        try {
          this.formData[this.activeTab].formDataDetail[f].value =
            detail[this.formData[this.activeTab].formDataDetail[f].label];
        } catch (err) {
          console.log(
            "[" +
              this.formData[this.activeTab].formDataDetail[f].label +
              "]" +
              "恢复失败：" +
              err
          );
        }
      }
      if (this.formData[this.activeTab].version != version) {
        this.$message({
          message:
            "参数填充成功，但是检测到脚本配置发生过修改(" +
            "V" +
            version +
            "→" +
            "V" +
            this.formData[this.activeTab].version +
            ")，可能无法完美恢复上一次参数，请关闭列表弹出框后查看",
          type: "info",
          duration: 4000
        });
      } else {
        this.$message({
          message: "参数填充成功，请关闭列表弹出框后点击提交按钮以运行",
          type: "success"
        });
      }
    },
    extraButtonFlushOutput(singleFormIndex, singleDataIndex, process_id) {
      var para = {
        process_id: process_id,
        user: sessionStorage.getItem("user").replace(/\"/g, "")
      };
      consoleScriptRunOutput(para).then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          if (data["data"]["status"] == -1) {
            this.$message({
              message: data["msg"],
              type: "error"
            });
            this.extra_button.loading = false;
            this.extra_button.buttonLoading = false;
            return;
          } else if (data["data"]["status"] == 0) {
            try {
              var dataTemp = JSON.parse(
                this.extra_button.output_temp + data["data"]["output"]
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
                this.extra_button.output_temp + data["data"]["output"]
              )
                .replace(/\n/g, "<br>")
                .replace(/\s/g, "&nbsp;");
            }
            this.extra_button.loading = false;
            this.extra_button.buttonLoading = false;
            return;
          } else if (data["data"]["status"] == 1) {
            this.extra_button.output_temp =
              this.extra_button.output_temp + data["data"]["output"];
            this.extraButtonFlushOutput(
              singleFormIndex,
              singleDataIndex,
              process_id
            );
          }
        }
      });
    },
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
      var para = {
        user: sessionStorage.getItem("user").replace(/\"/g, ""),
        command: command
      };
      this.extra_button.loading = true;
      consoleScriptExtraButtonScriptRun(para).then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          if (data["data"]["process_id"] == -1) {
            this.$message({
              message: "任务创建错误，请联系管理员！",
              type: "error"
            });
          } else {
            var process_id = data["data"]["process_id"];
          }
          this.extraButtonFlushOutput(
            singleFormIndex,
            singleDataIndex,
            process_id
          );
        }
      });
    },
    //使用当前激活tab的detial，接收start_command和组装方式，组装好command和detail并返回，start_command在运行脚本时为打开文件夹的命令加上起始命令
    command_get(start_command, type) {
      var command = "";
      var detail = {};
      if (type == "1") {
        //顺序模式
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
  },
  mounted() {
    this.getSubSystem();
  }
};
</script>

<style scoped>
.noMargin {
  margin: 0;
}
</style>