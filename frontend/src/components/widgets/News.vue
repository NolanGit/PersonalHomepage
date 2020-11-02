<template>
  <section>
    <el-row v-for="singleDataSuite in cookedData" :key="singleDataSuite">
      <el-col :span="6" v-for="data in singleDataSuite" :key="data">
        <el-card>
          <!-- title area -->
          <el-row>
            <div>{{ data.title }}</div>
            <el-radio-group v-model="value.choose" v-if="data.data.length > 1">
              <el-radio-button
                :label="singleValue.title"
                v-for="singleValue in data.data"
                :key="singleValue"
              ></el-radio-button>
            </el-radio-group>
          </el-row>
          <!-- content area -->
          <el-row>
            <div v-for="link in value[0].url" :key="link"></div>
            {{ link }}</el-row
          >
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
      cookedData: {},
    };
  },
  methods: {
    async get() {
      try {
        const { data: res } = await axios.post(api.get);
        this.rawData = res.data;
        const STEP = 4; // 每行有几个
        let temp = [];
        let count = 0;
        temp.push({});
        for (let x = 0; x < this.rawData.length; x++) {
          if (count < STEP) {
            count += 1;
          } else {
            count = 0;
            temp.push([]);
            count += 1;
          }
          temp[temp.length - 1].push(this.rawData[x]);
        }
        this.cookedData = temp;
        console.log(temp);
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
