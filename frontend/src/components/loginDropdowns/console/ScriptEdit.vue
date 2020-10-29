<template>
  <section>
    <div class="edit-form-card margin_left-medium margin_right-medium">
      <div
        class="scrollbar-div max_height-large padding-right-19"
        ref="scrollbarDiv"
      >
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
                  <div v-if="singleData.type == 'select'">
                    <td type="flex" class="td--label">
                      <p class="td__p--label">选项：</p>
                    </td>
                    <td>
                      <el-button
                        size="small"
                        @click.native="
                          singleDataOptionDialogClicked(
                            edit.formData.indexOf(singleData),
                            singleData.options
                          )
                        "
                        >编辑选项</el-button
                      >
                    </td>
                  </div>
                  <div v-if="singleData.type == 'select'">
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
                  <div
                    v-if="
                      singleData.type != 'date' &&
                      singleData.type != 'dateRange'
                    "
                  >
                    <td type="flex" class="td--label">
                      <p class="td__p--label">默认值：</p>
                    </td>
                    <td v-if="singleData.type != 'select'">
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
                    <td v-if="singleData.type == 'select'">
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
                    <td v-if="singleData.type == 'select'">
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
                  <div v-if="singleData.type != 'dateRange'">
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
                  <div v-if="singleData.extra_button == 1">
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
                  <div v-if="singleData.extra_button == 1">
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
                  <div class="div-flex">
                    <div>
                      <i
                        class="editFormRightButton editFormMoveUp el-icon-top"
                        @click="
                          editFormMoveUp(edit.formData.indexOf(singleData))
                        "
                      ></i>
                    </div>
                    <div>
                      <i
                        class="editFormRightButton editFormMoveDown el-icon-bottom"
                        @click="
                          editFormMoveDown(edit.formData.indexOf(singleData))
                        "
                      ></i>
                    </div>
                    <div>
                      <i
                        class="editFormRightButton editFormDeleted el-icon-close"
                        @click="
                          editFormDeleted(edit.formData.indexOf(singleData))
                        "
                      ></i>
                    </div>
                  </div>
                </el-col>
              </el-card>
            </div>
          </div>
          <div
            class="add"
            style="width: 99.87%"
            @click="editFormAddSingleData()"
          >
            <span>+ 添加参数</span>
          </div>
        </el-card>
      </div>
      <div class="dialog-footer">
        <el-button
          slot="reference"
          size="small"
          @click.native="editFormCloneButtonActive()"
          >复制现有脚本的组件配置</el-button
        >
        <el-button size="small" @click.native="edit.visible = false"
          >关闭</el-button
        >
        <el-button
          type="primary"
          size="small"
          :loading="edit.buttonLoading"
          @click.native="editFormSubmited()"
          >提交</el-button
        >
      </div>
    </div>

    <!--复制现有脚本的组件配置界面-->
    <el-drawer
      title="选择想要复制的配置"
      :visible.sync="cloneSettings.visible"
      :close-on-click-modal="false"
      size="25%"
    >
      <div class="margin_left-medium margin_right-medium">
        <div class="min_height-medium scrollbar-div max_height-large">
          <div class="margin_right-small">
            <el-table :data="cloneSettings.script.data" size="mini">
              <el-table-column
                label="名称"
                width="250"
                prop="name"
              ></el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    @click="editFormClone(scope.$index, scope.row)"
                    >选择</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
          </div>
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
        <div
          class="scrollbar-div max_height-large padding-right-19 padding_bottom-medium"
          ref="scrollbarDiv"
        >
          <div
            v-for="singleDataOption in singleDataOptionDialog.data"
            :key="singleDataOption.key"
          >
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
                  <el-input
                    style="width: 12vw"
                    size="small"
                    v-model="singleDataOption.label"
                    placeholder="请输入选项展示文字"
                  ></el-input>
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
                  <el-input
                    style="width: 16vw"
                    size="small"
                    v-model="singleDataOption.value"
                    placeholder="请输入选项实际的值"
                  ></el-input>
                </el-tooltip>
              </td>
              <td>
                <i
                  class="singleDataOptionDialogDeleted el-icon-delete"
                  @click="
                    singleDataOptionDialogDeleted(
                      singleDataOptionDialog.data.indexOf(singleDataOption)
                    )
                  "
                ></i>
              </td>
            </div>
          </div>
          <div
            class="add"
            style="width: 99.87%"
            @click="singleDataOptionDialogAddSingleData()"
          >
            <span>+ 添加选项</span>
          </div>
        </div>
        <div class="dialog-footer">
          <el-button
            size="small"
            @click="singleDataOptionDialog.visible = false"
            >关闭</el-button
          >
          <el-button
            type="primary"
            size="small"
            @click="singleDataOptionDialogSubmited()"
            >保存</el-button
          >
        </div>
      </div>
    </el-drawer>
  </section>
</template>

<script>
import axios from "axios";
import { deepClone } from "../../../js/common";

const api = {
  edit: "/script/edit",
  scriptAll: "/script/scriptAll",
  subSystemScript: "/script/subSystemScript",
};
export default {
  name: "ScriptEdit",
  props: {
    user_id: Number,
    edit: Array,
  },
  data() {
    return {
      edit: {
        title: "",
        start_folder: "",
        start_script: "",
        type: 1,
        formData: [],
      },
      singleDataOptionDialog: {
        visible: false,
        index: 0,
        data: [],
      },
      cloneSettings: {
        visible: false,
        script: {
          value: "",
          data: [],
        },
      },
    };
  },
  watch: {},
  methods: {
    swapItem(arr, index1, index2) {
      arr[index1] = arr.splice(index2, 1, arr[index1])[0];
      return arr;
    },
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
        remark: "",
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
          type: "info",
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
          type: "info",
        });
      }
    },
    //选择器组件点击
    singleDataOptionDialogClicked(index, singleDataOptions) {
      this.singleDataOptionDialog.index = index;
      this.singleDataOptionDialog.visible = true;
      this.singleDataOptionDialog.data =
        singleDataOptions.length == 0 ? [] : deepClone(singleDataOptions);
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
        value: "",
      });
    },
    //选择器组件提交
    singleDataOptionDialogSubmited() {
      this.edit.formData[
        this.singleDataOptionDialog.index
      ].options = this.singleDataOptionDialog.data;
      this.singleDataOptionDialog.visible = false;
    },
    //编辑脚本复制
    async editFormCloneButtonActive() {
      try {
        const { data: res } = await axios.post(api.subSystemScript, {
          sub_system_id: 0,
        });
        if (res["code"] !== 200) {
          this.$message({
            message: res["msg"],
            type: "error",
          });
        } else {
          this.cloneSettings.script.data = res.data;
          this.cloneSettings.visible = true;
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    editFormClone(index, row) {
      this.edit.formData = row.detail;
      this.$message({
        message: "成功",
        type: "success",
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
          user_id: this.user_id,
        });
        this.$message({
          message: res.msg,
          type: "success",
        });
        this.edit.visible = false;
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
      this.edit.buttonLoading = false;
    },
  },
};
</script>

<style>
</style>
