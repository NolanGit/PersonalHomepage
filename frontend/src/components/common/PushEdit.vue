// 编辑推送dialog
<template>
  <!--编辑提醒界面-->
  <div>
    <el-form ref="form" :model="notifyData.form" size="mini">
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
      <el-form-item label="推送方式" :v-show="notifyData.form.notify.select==1">
        <div class="div-flex" style="width:162px">
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
      <el-form-item label="提醒时间" :v-show="notifyData.form.notify.select==1">
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
      <el-form-item label="提醒间隔" :v-show="notifyData.form.notify.select==1">
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
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button type="primary" size="small" @click="edit()">确定</el-button>
    </span>
  </div>
</template>
<script>
import axios from "axios";
const api = {
  get: "/push/get",
  add: "/push/add",
  edit: "/push/edit",
  delete: "/push/delete"
};
export default {
  name: "PushEdit",
  props: {
    user_id: Number,
    widget_id: Number
  },
  data() {
    return {
      id: 0,
      notifyData: {
        form: {
          notify: {
            select: 0,
            options: [
              {
                value: 0,
                label: "否"
              },
              {
                value: 1,
                label: "是"
              }
            ]
          },
          notifyMethod: {
            select: 0,
            options: [
              {
                value: 0,
                label: "微信"
              },
              {
                value: 1,
                label: "邮件"
              }
            ]
          },
          triggerDate: "",
          triggerTime: "",
          interval: {
            value: "",
            unit: {
              select: 0,
              options: [
                {
                  value: 0,
                  label: "小时"
                },
                {
                  value: 1,
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
    async get() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
          widget_id: this.widget_id
        });
        if (res.data.length == 0) {
          return;
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async edit() {
      try {
        if (this.id != 0) {
          const { data: res } = await axios.post(api.edit, {
            user_id: this.user_id,
            widget_id: this.widget_id
          });
        } else if (this.id == 0) {
          const { data: res } = await axios.post(api.add, {
            user_id: this.user_id,
            widget_id: this.widget_id
          });
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
  mounted() {
    this.get();
  }
};
</script>
<style scoped>
</style>
