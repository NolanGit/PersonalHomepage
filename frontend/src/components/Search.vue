<template>
  <div class="search">
    <div>
      <i :class="searchIcon"></i>
    </div>
    <div>
      <el-autocomplete
        placeholder="请输入内容"
        v-model="word"
        @keyup.enter.native="search()"
        class="search-input"
        :fetch-suggestions="autoComplete"
        ref="input"
        @select="search()"
      >
        <el-select
          class="search-engine-select"
          v-model="searchEngines.select"
          slot="prepend"
          placeholder="请选择"
        >
          <el-option
            v-for="item in searchEngines.options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
        <el-button class="search-button" slot="append" icon="el-icon-search" @click="search()"></el-button>
      </el-autocomplete>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
const api = {
  searchEnginesData: "/search/searchEnginesData",
  searchEnginesAutoComplete: "/search/searchEnginesAutoComplete",
  searchLog: "/search/searchLog"
};

export default {
  name: "search",
  data() {
    return {
      word: "",
      searchIcon: "search-icon el-icon-search",
      searchEngines: {
        select: "",
        select_engine_id: 0,
        main_url: "",
        auto_complete_url: "",
        options: []
      }
    };
  },
  methods: {
    async searchEnginesDataFront() {
      try {
        const { data: res } = await axios.get(api.searchEnginesData);
        for (let s = 0; s < res.data.length; s++) {
          this.searchEngines.options.push({
            id: res.data[s].id,
            main_url: res.data[s].main_url,
            auto_complete_url: res.data[s].auto_complete_url,
            icon: res.data[s].icon,
            label: res.data[s].name,
            value: res.data[s].name
          });
        }
        this.searchEngines.select = this.searchEngines.options[0].value;
        this.searchEngines.select_engine_id = this.searchEngines.options[0].id;
        this.searchEngines.main_url = this.searchEngines.options[0].main_url;
        this.searchEngines.auto_complete_url = this.searchEngines.options[0].auto_complete_url;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async search() {
      for (var s = 0; s < this.searchEngines.options.length; s++) {
        if (this.searchEngines.options[s].value == this.searchEngines.select) {
          break;
        }
      }
      this.searchEngines.select_engine_id = this.searchEngines.options[s].id;
      var searchUrl = this.searchEngines.options[s].main_url.replace(
        "%word%",
        this.word
      );
      window.open(searchUrl);
      try {
        var user = sessionStorage.getItem("user").replace(/\"/g, "");
      } catch (error) {
        var user = undefined;
      }
      this.word = "";
      this.autoComplete("");
      try {
        const { data: res } = await axios.post(api.searchLog, {
          user: user,
          engine_id: this.searchEngines.select_engine_id,
          search_text: this.word
        });
      } catch (e) {
        console.log(e);
      }
    },
    async autoComplete(queryString, cb) {
      if (
        queryString === "" ||
        queryString === [] ||
        queryString === undefined
      ) {
        try {
          cb([]);
        } catch (e) {}
      } else {
        var lastWord = sessionStorage.getItem("lastWord");
        if (lastWord == queryString) {
          cb(eval(sessionStorage.getItem("lastWordAutoComplete")));
        } else {
          sessionStorage.setItem("lastWord", queryString);
          var autoCompleteUrl = this.searchEngines.auto_complete_url.replace(
            "%word%",
            this.word
          );
          try {
            var user = sessionStorage.getItem("user").replace(/\"/g, "");
          } catch (error) {
            var user = undefined;
          }
          try {
            const { data: res } = await axios.post(
              api.searchEnginesAutoComplete,
              {
                autoCompleteUrl: autoCompleteUrl,
                name: this.searchEngines.select,
                user: user
              }
            );
            function String2Dict(x) {
              return {
                value: x
              };
            }
            var result = res.data.map(String2Dict);
            sessionStorage.setItem(
              "lastWordAutoComplete",
              JSON.stringify(result)
            );
            cb(result);
          } catch (e) {
            console.log(e);
            this.$message({
              message: e.response.data.msg,
              type: "error"
            });
          }
        }
      }
    }
  },
  created() {
    this.searchEnginesDataFront();
  },
  mounted() {
    this.$refs["input"].focus();
  }
};
</script>
<style scoped>
.search-icon {
  font-size: 100px;
  padding-top: 80px;
  padding-bottom: 60px;
}
.search-input {
  margin-left: 50px;
  margin-right: 50px;
  width: 60%;
}
.search-engine-select {
  width: 120px;
}
.search-button {
  width: 70px;
}
</style>
