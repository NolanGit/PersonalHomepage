<template>
  <div class="weather">
    <el-row type="flex" justify="center" ref="weatherForm" :model="weatherForm" v-show="todayShow">
      <td>
        <el-row type="flex" justify="left">
          <td class="todayWeatherIcon">
            <i :class="iconfontWeatherClass" style="font-size:100px;"></i>
          </td>
          <td class="todayWeatherText">
            <div class="todayWeatherTextDiv">{{weatherForm.tmp}}°C</div>
          </td>
        </el-row>

        <el-row type="flex" justify="left">
          <td class="todayAqiIcon">
            <i :class="iconfontAqiClass" style="font-size:50px;"></i>
          </td>
          <td class="todayAqiText">
            <div class="todayAqiTextDiv">AQI:{{weatherForm.aqi}}</div>
          </td>
        </el-row>

        <el-row type="flex" justify="left">
          <td class="tomorrowWeatherIcon">
            <i :class="iconfontTomorrowWeatherClass" style="font-size:50px;"></i>
          </td>
          <td class="tomorrowWeatherText">
            <div
              class="tomorrowWeatherTextDiv"
            >明日:{{weatherForm.tomorrow_tmp_min}}°C-{{weatherForm.tomorrow_tmp_max}}°C</div>
          </td>
        </el-row>
      </td>
      <div
        style="float:left;margin-top: 30px;width:1px;height: 200px; background: darkgray;margin-left: 25px;margin-right: 25px;"
      ></div>
      <div class="weatherSideText">
        <td>
          <div
            class="weatherSideTextDetail"
          >今日气温: {{weatherForm.tmp_min}}°C-{{weatherForm.tmp_max}}°C</div>
          <div class="weatherSideTextDetail">风力: {{weatherForm.wind}}</div>
          <div class="weatherSideTextDetail">体感温度: {{weatherForm.fl}}°C</div>
        </td>
      </div>
    </el-row>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import { getWeatherData } from "../api/weather";

export default {
  name: "weather",
  props: {
    city: String
  },
  data() {
    return {
      weatherForm: {
        tmp: "-",
        tmp_min: "-",
        tmp_max: "-",
        fl: "-",
        wind: "-",
        aqi: "-",
        tomorrow_tmp_min: "-",
        tomorrow_tmp_max: "-"
      },
      loading: true,
      value: "",
      iconfontWeatherClass: "el-icon-more",
      iconfontAqiClass: "el-icon-more",
      iconfontTomorrowWeatherClass: "el-icon-more",
      todayShow: true
    };
  },
  methods: {
    getWeatherDatafront(loc) {
      this.todayShow = false;
      this.value = loc;
      try {
        var user = sessionStorage.getItem("user").replace(/\"/g, "");
      } catch (error) {
        var user = undefined;
      }
      let para = {
        location: this.value,
        user: user
      };
      getWeatherData(para)
        .then(data => {
          let {
            fl,
            tmp,
            wind,
            cond_code_d,
            cond_txt_d,
            cond_code_n,
            cond_txt_n,
            tmp_max,
            tmp_min,
            tomorrow_cond_code_d,
            tomorrow_cond_txt_d,
            tomorrow_tmp_max,
            tomorrow_tmp_min,
            aqi
          } = data;
          this.weatherForm.tmp = tmp;
          this.weatherForm.tmp_min = tmp_min;
          this.weatherForm.tmp_max = tmp_max;
          this.weatherForm.fl = fl;
          this.weatherForm.wind = wind;
          this.weatherForm.aqi = aqi;
          this.weatherForm.tomorrow_tmp_min = tomorrow_tmp_min;
          this.weatherForm.tomorrow_tmp_max = tomorrow_tmp_max;
          this.loading = false;
          if (cond_code_d == 100) {
            this.iconfontWeatherClass = "iconfont icon-qing";
          }
          if (
            (cond_code_d >= 101 && cond_code_d <= 102) ||
            cond_code_d == 104 ||
            (cond_code_d >= 202 && cond_code_d <= 208)
          ) {
            this.iconfontWeatherClass = "iconfont icon-duoyun";
          }
          if (cond_code_d == 103) {
            this.iconfontWeatherClass = "iconfont icon-duoyunzhuanyin";
          }
          if (cond_code_d == 200) {
            this.iconfontWeatherClass = "iconfont icon-feng";
          }
          if (cond_code_d == 201) {
            this.iconfontWeatherClass = "iconfont icon-qing";
          }
          if (cond_code_d >= 209 && cond_code_d <= 213) {
            this.iconfontWeatherClass = "iconfont icon-taifeng";
          }
          if (cond_code_d >= 301 && cond_code_d <= 303) {
            this.iconfontWeatherClass = "iconfont icon-baoyu";
          }
          if (cond_code_d == 304 || cond_code_d == 313) {
            this.iconfontWeatherClass = "iconfont icon-bingbao";
          }
          if (
            cond_code_d == 300 ||
            cond_code_d == 305 ||
            cond_code_d == 309 ||
            cond_code_d == 314
          ) {
            this.iconfontWeatherClass = "iconfont icon-xiaoyu";
          }
          if (cond_code_d == 306 || cond_code_d == 315 || cond_code_d == 399) {
            this.iconfontWeatherClass = "iconfont icon-zhongyu";
          }
          if (
            (cond_code_d >= 307 && cond_code_d <= 308) ||
            (cond_code_d >= 310 && cond_code_d <= 312) ||
            (cond_code_d >= 316 && cond_code_d <= 318)
          ) {
            this.iconfontWeatherClass = "iconfont icon-dayu";
          }
          if (cond_code_d == 400 || cond_code_d == 407 || cond_code_d == 408) {
            this.iconfontWeatherClass = "iconfont icon-xiaoxue";
          }
          if (cond_code_d == 401 || cond_code_d == 409 || cond_code_d == 499) {
            this.iconfontWeatherClass = "iconfont icon-zhongxue";
          }
          if (cond_code_d == 402 || cond_code_d == 410) {
            this.iconfontWeatherClass = "iconfont icon-daxue";
          }
          if (cond_code_d == 403) {
            this.iconfontWeatherClass = "iconfont icon-baoxue";
          }
          if (cond_code_d >= 404 && cond_code_d <= 406) {
            this.iconfontWeatherClass = "iconfont icon-yujiaxue";
          }
          if (
            (cond_code_d >= 500 && cond_code_d <= 501) ||
            (cond_code_d >= 509 && cond_code_d <= 510) ||
            (cond_code_d >= 514 && cond_code_d <= 515)
          ) {
            this.iconfontWeatherClass = "iconfont icon-wu";
          }
          if (cond_code_d == 502) {
            this.iconfontWeatherClass = "iconfont icon-mai";
          }
          if (cond_code_d >= 503 && cond_code_d <= 504) {
            this.iconfontWeatherClass = "iconfont icon-shachen1";
          }
          if (cond_code_d >= 507 && cond_code_d <= 508) {
            this.iconfontWeatherClass = "iconfont icon-shachenbao";
          }
          //aqi图标
          if (aqi >= 100) {
            this.iconfontAqiClass = "iconfont icon-PM";
          }
          if (aqi < 100) {
            this.iconfontAqiClass = "iconfont icon-app_icons--";
          }
          //明日天气图标
          if (tomorrow_cond_code_d == 100) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-qing";
          }
          if (
            (tomorrow_cond_code_d >= 101 && tomorrow_cond_code_d <= 102) ||
            tomorrow_cond_code_d == 104 ||
            (tomorrow_cond_code_d >= 202 && tomorrow_cond_code_d <= 208)
          ) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-duoyun";
          }
          if (tomorrow_cond_code_d == 103) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-duoyunzhuanyin";
          }
          if (tomorrow_cond_code_d == 200) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-feng";
          }
          if (tomorrow_cond_code_d == 201) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-qing";
          }
          if (tomorrow_cond_code_d >= 209 && tomorrow_cond_code_d <= 213) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-taifeng";
          }
          if (tomorrow_cond_code_d >= 301 && tomorrow_cond_code_d <= 303) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-baoyu";
          }
          if (tomorrow_cond_code_d == 304 || tomorrow_cond_code_d == 313) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-bingbao";
          }
          if (
            tomorrow_cond_code_d == 300 ||
            tomorrow_cond_code_d == 305 ||
            tomorrow_cond_code_d == 309 ||
            tomorrow_cond_code_d == 314
          ) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-xiaoyu";
          }
          if (
            tomorrow_cond_code_d == 306 ||
            tomorrow_cond_code_d == 315 ||
            tomorrow_cond_code_d == 399
          ) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-zhongyu";
          }
          if (
            (tomorrow_cond_code_d >= 307 && tomorrow_cond_code_d <= 308) ||
            (tomorrow_cond_code_d >= 310 && tomorrow_cond_code_d <= 312) ||
            (tomorrow_cond_code_d >= 316 && tomorrow_cond_code_d <= 318)
          ) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-dayu";
          }
          if (
            tomorrow_cond_code_d == 400 ||
            tomorrow_cond_code_d == 407 ||
            tomorrow_cond_code_d == 408
          ) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-xiaoxue";
          }
          if (
            tomorrow_cond_code_d == 401 ||
            tomorrow_cond_code_d == 409 ||
            tomorrow_cond_code_d == 499
          ) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-zhongxue";
          }
          if (tomorrow_cond_code_d == 402 || tomorrow_cond_code_d == 410) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-daxue";
          }
          if (tomorrow_cond_code_d == 403) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-baoxue";
          }
          if (tomorrow_cond_code_d >= 404 && tomorrow_cond_code_d <= 406) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-yujiaxue";
          }
          if (
            (tomorrow_cond_code_d >= 500 && tomorrow_cond_code_d <= 501) ||
            (tomorrow_cond_code_d >= 509 && tomorrow_cond_code_d <= 510) ||
            (tomorrow_cond_code_d >= 514 && tomorrow_cond_code_d <= 515)
          ) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-wu";
          }
          if (tomorrow_cond_code_d == 502) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-mai";
          }
          if (tomorrow_cond_code_d >= 503 && tomorrow_cond_code_d <= 504) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-shachen1";
          }
          if (tomorrow_cond_code_d >= 507 && tomorrow_cond_code_d <= 508) {
            this.iconfontTomorrowWeatherClass = "iconfont icon-shachenbao";
          }
          this.todayShow = true;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {},
  mounted() {
    this.getWeatherDatafront(this.city);
  }
};
</script>
<style scoped>
.todayWeatherText {
  display: flex;
}
.todayWeatherTextDiv {
  text-align: center;
  color: #303133;
  font-family: Arial;
  font-weight: bold;
  font-size: 38px;
  align-self: center;
}
.todayAqiText {
  display: flex;
}
.todayAqiTextDiv {
  text-align: center;
  color: #303133;
  font-family: Arial;
  font-weight: bold;
  font-size: 20px;
  align-self: center;
  margin-left: 4px;
}
.tomorrowWeatherText {
  display: flex;
}
.tomorrowWeatherTextDiv {
  text-align: center;
  color: #303133;
  font-family: Arial;
  font-weight: bold;
  font-size: 20px;
  align-self: center;
  margin-left: 4px;
}
.weatherSideText {
  text-align: left;
  color: #303133;
  font-family: Arial;
  font-weight: bold;
  font-size: 20px;
  margin-bottom: 20px;
  margin-top: 20px;
}
.weatherSideTextDetail {
  margin-top: 30px;
  margin-bottom: 30px;
}
</style>
