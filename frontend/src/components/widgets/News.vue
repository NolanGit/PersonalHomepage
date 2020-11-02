<template>
  <section>
    <el-row v-for="singleDataSuite in cookedData" :key="singleDataSuite">
      <el-col :span="6" v-for="data in singleDataSuite" :key="data">
        <el-card>
          <!-- title area -->
          <el-row>
            <div>data</div>
            <el-radio-group v-model="radio1">
              <el-radio-button label="上海"></el-radio-button>
              <el-radio-button label="北京"></el-radio-button>
            </el-radio-group>
          </el-row>
          <!-- content area -->
          <el-row> </el-row>
        </el-card>
      </el-col>
    </el-row>
  </section>
</template>
<script>
import axios from "axios";

const api = {
  get: "/news/get",
};

export default {
  name: "news",
  watch: {},
  data() {
    return {
      rawData: [],
      cookedData: [],
    };
  },
  methods: {
    async get() {
      try {
        const { data: res } = await axios.post(api.get);
        this.rawData = res.data;
        const STEP1 = 4; // 每行有几个
        let temp1 = [];
        let count = 0;
        for (let k in this.rawData) {
          if (!count < 4) {
            temp1[temp1.length - 1][k] = this.rawData[k];
            count += 1;
          } else {
            count = 0;
            temp1.push([]);
            temp1[temp1.length - 1][k] = this.rawData[k];
          }
        }
        console.log(temp1);
      } catch (e) {
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
    this.$emit("done");
  },
};
</script>
</style>
