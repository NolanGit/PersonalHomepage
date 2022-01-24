<template>
  <section>
    <el-row>
      <el-col>
        <el-radio-group style="text-align: left" v-model="target" size="mini">
          <el-radio-button label="当前新闻"></el-radio-button>
          <el-radio-button label="新闻检索"></el-radio-button>
        </el-radio-group>
      </el-col>
      <el-col>
        <el-input v-if="target == '新闻检索'" size="medium" v-model="keyword">
          <el-date-picker
            slot="prepend"
            v-model="dateRange"
            type="daterange"
            align="right"
            unlink-panels
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :picker-options="pickerOptions"
          >
          </el-date-picker>
          <el-button
            class="search-button"
            slot="append"
            icon="el-icon-search"
            @click="search()"
          ></el-button>
        </el-input>
      </el-col>
    </el-row>
    <el-row v-if="target == '当前新闻'">
      <el-row
        :gutter="20"
        v-for="singleDataSuite in cookedData"
        :key="singleDataSuite"
      >
        <el-col :span="6" v-for="data in singleDataSuite" :key="data">
          <el-card shadow="hover" class="margin_bottom-medium">
            <newsModule :newsData="data" @done="done()" />
          </el-card>
        </el-col>
      </el-row>
    </el-row>
  </section>
</template>
<script>
import axios from "axios";
import newsModule from "./NewsModule.vue";
import { deepClone } from "../../js/common";

const api = {
  get: "/news/get",
};

export default {
  name: "news",
  props: {
    flush: Number,
  },
  components: {
    newsModule,
  },
  watch: {},
  data() {
    return {
      target: "当前新闻",
      dateRange: [],
      keyword: "",
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
            picker.$emit('pick', [start, end]);
          }
        }]
      },
      rawData: [],
      cookedData: {},
    };
  },
  methods: {
    done() {
      this.$emit("done");
    },
    async get() {
      try {
        const { data: res } = await axios.post(api.get, {
          token: this.$cookies.get("csrf_token"),
        });
        this.rawData = res.data;
        const STEP = 4; // 每行有几个
        let temp = [];
        let count = 0;
        temp.push([]);
        temp[temp.length - 1] = [];
        for (let x = 0; x < this.rawData.length; x++) {
          this.rawData[x].choose = this.rawData[x].data[0].title;
          this.rawData[x].show = deepClone(this.rawData[x].data[0]);
          this.rawData[x].chooseItems = [];
          for (let y = 0; y < this.rawData[x].data.length; y++) {
            this.rawData[x].chooseItems.push(this.rawData[x].data[y].title);
          }
          if (count < STEP) {
            count += 1;
          } else {
            count = 0;
            temp.push([]);
            temp[temp.length - 1] = [];
            count += 1;
          }
          temp[temp.length - 1].push(this.rawData[x]);
        }
        this.cookedData = temp;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    search() {
      console.log(this.dateRange)
      console.log(this.keyword)
    }
  },
  mounted() {
    this.get();
    this.timer = window.setInterval(this.get, this.flush);
  },
  beforeDestroy() {
    window.clearInterval(this.timer);
  },
};
</script>
</style>
