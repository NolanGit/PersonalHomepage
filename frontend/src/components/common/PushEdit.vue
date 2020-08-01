// 编辑推送dialog
<template>
  <!--编辑提醒界面-->
  <div>
    <el-form ref="form" :model="notifyData.form" size="mini" class="padding_bottom-medium">
      <el-form-item label="是否推送">
        <div class="div-flex">
          <el-select
            v-model="notifyData.form.notify.select"
            placeholder="请选择"
            size="small"
            class="main_select--medium"
          >
            <el-option
              v-for="item in notifyData.form.notify.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </div>
      </el-form-item>
      <el-form-item label="推送方式" v-show="notifyData.form.notify.select == 1">
        <div class="div-flex" style="width:324px">
          <el-select
            v-model="notifyData.form.notifyMethod.select"
            placeholder="请选择"
            size="small"
            class="main_select--medium"
          >
            <el-option
              v-for="item in notifyData.form.notifyMethod.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </div>
      </el-form-item>
      <el-form-item label="提醒间隔" v-show="notifyData.form.notify.select == 1">
        <div class="div-flex">
          <div>每</div>
          <el-input
            v-model="notifyData.form.interval.value"
            placeholder="请输入"
            size="small"
            class="main_input--tiny inline_margin--small"
          ></el-input>
          <el-select
            v-model="notifyData.form.interval.unit.select"
            placeholder="请选择"
            size="small"
            class="main_select--medium"
          >
            <el-option
              v-for="item in notifyData.form.interval.unit.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </div>
      </el-form-item>
      <el-form-item label="在此时间后开始推送" v-show="notifyData.form.notify.select == 1">
        <div class="div-flex">
          <el-date-picker
            v-model="notifyData.form.triggerDate"
            type="date"
            placeholder="选择日期"
            value-format="yyyy-MM-dd"
            size="small"
            class="main_select--medium"
          ></el-date-picker>
          <el-time-select
            v-model="notifyData.form.triggerTime"
            :picker-options="{
              start: '00:00',
              step: '00:15',
              end: '24:00'
            }"
            placeholder="选择时间"
            size="small"
            class="main_select--medium"
          ></el-time-select>
        </div>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button :loading="buttonLoading" type="primary" size="small" @click="edit()">确定</el-button>
    </span>
  </div>
</template>
<script>
import axios from "axios";
import { formatDate } from "../../js/common";
const api = {
  get: "/push/get",
  add: "/push/add",
  edit: "/push/edit",
  delete: "/push/delete",
};
export default {
  name: "PushEdit",
  props: {
    user_id: Number,
    widget_id: Number,
  },
  data() {
    return {
      id: 0,
      buttonLoading: false,
      notifyData: {
        form: {
          notify: {
            select: 0,
            options: [
              {
                value: 0,
                label: "否",
              },
              {
                value: 1,
                label: "是",
              },
            ],
          },
          notifyMethod: {
            select: 1,
            options: [
              {
                value: 1,
                label: "微信",
              },
              {
                value: 2,
                label: "邮件",
              },
            ],
          },
          triggerDate: "",
          triggerTime: "",
          interval: {
            value: "",
            unit: {
              select: 1,
              options: [
                {
                  value: 0,
                  label: "分钟",
                },
                {
                  value: 1,
                  label: "小时",
                },
                {
                  value: 2,
                  label: "天",
                },
              ],
            },
          },
        },
      },
    };
  },
  methods: {
    async get() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
          widget_id: this.widget_id,
        });
        if (res.data.length == 0) {
          var today = new Date();
          this.notifyData.form.triggerDate = formatDate(
            new Date(today.getTime() + 24 * 60 * 60 * 1000)
          );
          this.notifyData.form.triggerTime = "08:00";
          return;
        } else {
          this.id = res.data.id;
          this.notifyData.form.notify.select = res.data.notify;
          this.notifyData.form.notifyMethod.select = res.data.notify_method;
          this.notifyData.form.triggerDate = res.data.notify_trigger_time.split(
            " "
          )[0];
          this.notifyData.form.triggerTime = res.data.notify_trigger_time
            .split(" ")[1]
            .substr(0, 5);
          this.notifyData.form.interval.value = res.data.notify_interval_raw;
          this.notifyData.form.interval.unit.select =
            res.data.notify_interval_unit;
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async edit() {
      try {
        this.buttonLoading = true;
        if (this.id != 0) {
          const { data: res } = await axios.post(api.edit, {
            id: this.id,
            user_id: this.user_id,
            widget_id: this.widget_id,
            notify: this.notifyData.form.notify.select,
            notify_method: this.notifyData.form.notifyMethod.select,
            notify_interval_raw: Number(this.notifyData.form.interval.value),
            notify_interval_unit: this.notifyData.form.interval.unit.select,
            notify_trigger_time:
              this.notifyData.form.triggerDate +
              " " +
              this.notifyData.form.triggerTime,
          });
          this.$message({
            message: res.msg,
            type: "success",
          });
          this.buttonLoading = false;
          this.$emit("done");
        } else if (this.id == 0) {
          const { data: res } = await axios.post(api.add, {
            id: this.id,
            user_id: this.user_id,
            widget_id: this.widget_id,
            notify: this.notifyData.form.notify.select,
            notify_method: this.notifyData.form.notifyMethod.select,
            notify_interval_raw: Number(this.notifyData.form.interval.value),
            notify_interval_unit: this.notifyData.form.interval.unit.select,
            notify_trigger_time:
              this.notifyData.form.triggerDate +
              " " +
              this.notifyData.form.triggerTime,
          });
          this.$message({
            message: res.msg,
            type: "success",
          });
          this.buttonLoading = false;
          this.$emit("done");
        }
      } catch (e) {
        this.buttonLoading = false;
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
  },
  mounted() {
    this.get();
  },
};
</script>
<style scoped>
</style>
