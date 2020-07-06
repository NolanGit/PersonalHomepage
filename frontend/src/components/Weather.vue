<template>
  <div class="weather">
    <el-carousel height="250px" trigger="click" interval="5000" indicator-position="outside">
      <el-carousel-item v-for="weather in weathers" :key="weather">
        <el-row type="flex" justify="center" ref="weatherForm" :model="weather.weatherForm">
          <div>
            <div class="location">{{ weather.location }}</div>
          </div>
        </el-row>
        <el-row type="flex" justify="center" ref="weatherForm" :model="weather.weatherForm">
          <td>
            <el-row type="flex" justify="left">
              <td class="todayWeatherIcon">
                <i :class="weather.iconfontWeatherClass" style="font-size:100px;"></i>
              </td>
              <td class="todayWeatherText">
                <div class="todayWeatherTextDiv">{{ weather.weatherForm.tmp }}°C</div>
              </td>
            </el-row>

            <el-row type="flex" justify="left">
              <td class="todayAqiIcon">
                <i :class="weather.iconfontAqiClass" style="font-size:50px;"></i>
              </td>
              <td class="todayAqiText">
                <div class="todayAqiTextDiv">AQI:{{ weather.weatherForm.aqi }}</div>
              </td>
            </el-row>

            <el-row type="flex" justify="left">
              <td class="tomorrowWeatherIcon">
                <i :class="weather.iconfontTomorrowWeatherClass" style="font-size:50px;"></i>
              </td>
              <td class="tomorrowWeatherText">
                <div class="tomorrowWeatherTextDiv">
                  明日:{{ weather.weatherForm.tomorrow_tmp_min }}°C-{{
                  weather.weatherForm.tomorrow_tmp_max
                  }}°C
                </div>
              </td>
            </el-row>
          </td>
          <div
            style="float:left;margin-top: 30px;width:1px;height: 175px; background: darkgray;margin-left: 25px;margin-right: 25px;"
          ></div>
          <div class="weatherSideText">
            <td>
              <div class="weatherSideTextDetail">
                今日: {{ weather.weatherForm.tmp_min }}°C-{{
                weather.weatherForm.tmp_max
                }}°C
              </div>
              <div class="weatherSideTextDetail">风力: {{ weather.weatherForm.wind }}</div>
              <div class="weatherSideTextDetail">体感: {{ weather.weatherForm.fl }}°C</div>
            </td>
          </div>
        </el-row>
      </el-carousel-item>
    </el-carousel>

    <el-row type="flex" justify="center" v-show="user_id != 0">
      <WidgetButton
        :user_id="user_id"
        :widget_id="widget_id"
        :buttons="buttons"
        @add="add()"
        @sort="sort()"
      ></WidgetButton>
    </el-row>

    <!--编辑顺序界面-->
    <el-dialog title="编辑地区" :visible.sync="locationEdit.visible" width="40%">
      <SlickSort
        v-if="locationEdit.visible"
        :list="locationEdit.list"
        :can_be_edit="false"
        @submit="locationEditSubmit"
      ></SlickSort>
    </el-dialog>

    <!--编辑界面-->
    <el-dialog title="添加城市" :visible.sync="edit.visible" width="40%">
      <el-form ref="form" :model="edit" size="mini">
        <el-form-item label="城市名称">
          <div class="div-flex">
            <el-input size="mini" v-model="edit.location" placeholder="城市名称，如：北京"></el-input>
          </div>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" @click="locationAdd()">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import axios from "axios";
import SlickSort from "./common/SlickSort.vue";
import WidgetButton from "./common/WidgetButton.vue";
const api = {
  weatherData: "/weather/get",
  locationAdd: "/weather/weatherLocationCreate",
  locationListEdit: "/weather/weatherLocationListEdit"
};

export default {
  name: "weather",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
    flush: Boolean
  },
  components: {
    SlickSort,
    WidgetButton
  },
  watch: {
    flush(newVal, oldVal) {
      if (newVal) {
        this.weatherData();
      }
    }
  },
  data() {
    return {
      locationEdit: {
        list: [],
        visible: false
      },
      weathers: [
        {
          location: "",
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
          iconfontWeatherClass: "el-icon-more",
          iconfontAqiClass: "el-icon-more",
          iconfontTomorrowWeatherClass: "el-icon-more"
        }
      ],
      loading: true,
      edit: {
        visible: false,
        location: ""
      }
    };
  },
  methods: {
    add() {
      this.edit.visible = true;
    },
    sort() {
      this.locationEdit.list = [];
      for (let x = 1; x < this.weathers.length; x++) {
        this.locationEdit.list.push({
          name: this.weathers[x].location
        });
      }
      this.locationEdit.visible = true;
    },
    async locationEditSubmit(list) {
      try {
        let tempList = [];
        for (let x = 0; x < list.length; x++) {
          tempList.push(list[x].name);
        }
        const { data: res } = await axios.post(api.locationListEdit, {
          user_id: this.user_id,
          locations: tempList
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.locationEdit.visible = false;
        this.weatherData();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async locationAdd() {
      this.edit.visible = false;
      try {
        const { data: res } = await axios.post(api.locationAdd, {
          user_id: this.user_id,
          location: this.edit.location
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.weatherData();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async weatherData(locations) {
      try {
        const { data: res } = await axios.post(api.weatherData, {
          user_id: this.user_id
        });
        this.weathers = [];
        for (
          let single_result = 0;
          single_result < res.data.length;
          single_result++
        ) {
          let {
            id,
            location,
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
          } = res.data[single_result];
          this.weathers.push({ weatherForm: {} });
          this.weathers[single_result].weatherForm.tmp = tmp;
          this.weathers[single_result].weatherForm.tmp_min = tmp_min;
          this.weathers[single_result].weatherForm.tmp_max = tmp_max;
          this.weathers[single_result].weatherForm.fl = fl;
          this.weathers[single_result].weatherForm.wind = wind;
          this.weathers[single_result].weatherForm.aqi = aqi;
          this.weathers[
            single_result
          ].weatherForm.tomorrow_tmp_min = tomorrow_tmp_min;
          this.weathers[
            single_result
          ].weatherForm.tomorrow_tmp_max = tomorrow_tmp_max;
          this.weathers[single_result].location = location;
          this.weathers[single_result].id = id;
          this.loading = false;
          if (cond_code_d == 100) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-qing";
          }
          if (
            (cond_code_d >= 101 && cond_code_d <= 102) ||
            cond_code_d == 104 ||
            (cond_code_d >= 202 && cond_code_d <= 208)
          ) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-duoyun";
          }
          if (cond_code_d == 103) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-duoyunzhuanyin";
          }
          if (cond_code_d == 200) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-feng";
          }
          if (cond_code_d == 201) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-qing";
          }
          if (cond_code_d >= 209 && cond_code_d <= 213) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-taifeng";
          }
          if (cond_code_d >= 301 && cond_code_d <= 303) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-baoyu";
          }
          if (cond_code_d == 304 || cond_code_d == 313) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-bingbao";
          }
          if (
            cond_code_d == 300 ||
            cond_code_d == 305 ||
            cond_code_d == 309 ||
            cond_code_d == 314
          ) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-xiaoyu";
          }
          if (cond_code_d == 306 || cond_code_d == 315 || cond_code_d == 399) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-zhongyu";
          }
          if (
            (cond_code_d >= 307 && cond_code_d <= 308) ||
            (cond_code_d >= 310 && cond_code_d <= 312) ||
            (cond_code_d >= 316 && cond_code_d <= 318)
          ) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-dayu";
          }
          if (cond_code_d == 400 || cond_code_d == 407 || cond_code_d == 408) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-xiaoxue";
          }
          if (cond_code_d == 401 || cond_code_d == 409 || cond_code_d == 499) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-zhongxue";
          }
          if (cond_code_d == 402 || cond_code_d == 410) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-daxue";
          }
          if (cond_code_d == 403) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-baoxue";
          }
          if (cond_code_d >= 404 && cond_code_d <= 406) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-yujiaxue";
          }
          if (
            (cond_code_d >= 500 && cond_code_d <= 501) ||
            (cond_code_d >= 509 && cond_code_d <= 510) ||
            (cond_code_d >= 514 && cond_code_d <= 515)
          ) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-wu";
          }
          if (cond_code_d == 502) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-mai";
          }
          if (cond_code_d >= 503 && cond_code_d <= 504) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-shachen1";
          }
          if (cond_code_d >= 507 && cond_code_d <= 508) {
            this.weathers[single_result].iconfontWeatherClass =
              "iconfont icon-shachenbao";
          }
          //aqi图标
          if (aqi >= 100) {
            this.weathers[single_result].iconfontAqiClass = "iconfont icon-PM";
          }
          if (aqi < 100) {
            this.weathers[single_result].iconfontAqiClass =
              "iconfont icon-app_icons--";
          }
          //明日天气图标
          if (tomorrow_cond_code_d == 100) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-qing";
          }
          if (
            (tomorrow_cond_code_d >= 101 && tomorrow_cond_code_d <= 102) ||
            tomorrow_cond_code_d == 104 ||
            (tomorrow_cond_code_d >= 202 && tomorrow_cond_code_d <= 208)
          ) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-duoyun";
          }
          if (tomorrow_cond_code_d == 103) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-duoyunzhuanyin";
          }
          if (tomorrow_cond_code_d == 200) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-feng";
          }
          if (tomorrow_cond_code_d == 201) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-qing";
          }
          if (tomorrow_cond_code_d >= 209 && tomorrow_cond_code_d <= 213) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-taifeng";
          }
          if (tomorrow_cond_code_d >= 301 && tomorrow_cond_code_d <= 303) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-baoyu";
          }
          if (tomorrow_cond_code_d == 304 || tomorrow_cond_code_d == 313) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-bingbao";
          }
          if (
            tomorrow_cond_code_d == 300 ||
            tomorrow_cond_code_d == 305 ||
            tomorrow_cond_code_d == 309 ||
            tomorrow_cond_code_d == 314
          ) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-xiaoyu";
          }
          if (
            tomorrow_cond_code_d == 306 ||
            tomorrow_cond_code_d == 315 ||
            tomorrow_cond_code_d == 399
          ) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-zhongyu";
          }
          if (
            (tomorrow_cond_code_d >= 307 && tomorrow_cond_code_d <= 308) ||
            (tomorrow_cond_code_d >= 310 && tomorrow_cond_code_d <= 312) ||
            (tomorrow_cond_code_d >= 316 && tomorrow_cond_code_d <= 318)
          ) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-dayu";
          }
          if (
            tomorrow_cond_code_d == 400 ||
            tomorrow_cond_code_d == 407 ||
            tomorrow_cond_code_d == 408
          ) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-xiaoxue";
          }
          if (
            tomorrow_cond_code_d == 401 ||
            tomorrow_cond_code_d == 409 ||
            tomorrow_cond_code_d == 499
          ) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-zhongxue";
          }
          if (tomorrow_cond_code_d == 402 || tomorrow_cond_code_d == 410) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-daxue";
          }
          if (tomorrow_cond_code_d == 403) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-baoxue";
          }
          if (tomorrow_cond_code_d >= 404 && tomorrow_cond_code_d <= 406) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-yujiaxue";
          }
          if (
            (tomorrow_cond_code_d >= 500 && tomorrow_cond_code_d <= 501) ||
            (tomorrow_cond_code_d >= 509 && tomorrow_cond_code_d <= 510) ||
            (tomorrow_cond_code_d >= 514 && tomorrow_cond_code_d <= 515)
          ) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-wu";
          }
          if (tomorrow_cond_code_d == 502) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-mai";
          }
          if (tomorrow_cond_code_d >= 503 && tomorrow_cond_code_d <= 504) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-shachen1";
          }
          if (tomorrow_cond_code_d >= 507 && tomorrow_cond_code_d <= 508) {
            this.weathers[single_result].iconfontTomorrowWeatherClass =
              "iconfont icon-shachenbao";
          }
        }
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    }
  },
  created() {},
  mounted() {
    this.weatherData();
  }
};
</script>
<style scoped>
.weather {
  min-height: 280px;
}
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
  font-size: 18px;
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
  font-size: 18px;
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
.location {
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
  font-weight: 600;
  font-size: 20px;
  color: #303133;
}
.weatherDelete {
  margin-left: 10px;
}
</style>
