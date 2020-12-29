<template>
  <div class="search">
    <div class="search-icon-div">
      <i class="search-icon el-icon-search"></i>
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
          @change="searchEnginesChanged"
        >
          <el-option
            v-for="item in searchEngines.options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
            <span style="float: left">{{ item.label }}</span>
          </el-option>
        </el-select>
        <el-button
          class="search-button"
          slot="append"
          icon="el-icon-search"
          @click="search()"
        ></el-button>
      </el-autocomplete>
    </div>
  </div>
</template>
<script>
import md5 from "js-md5";
import axios from "axios";
import Router from "vue-router";
const default_suggest_url =
  "https://suggestion.baidu.com/su?wd=%word%&cb=window.baidu.sug";
const default_suggest_func =
  "window.baidu={sug:function(json){cb(json.s.map(function(x){return{'value':x}}))}}";
const api = {
  searchEngines: "/search/searchEngines",
  searchLog: "/search/searchLog",
};

export default {
  name: "search",
  props: {
    user_id: Number,
  },
  data() {
    return {
      word: "",
      searchIcon: "search-icon el-icon-search",
      searchEngines: {
        select: "",
        select_engine_id: 0,
        main_url: "",
        suggest_url: "",
        suggest_func: "",
        options: [],
      },
    };
  },
  methods: {
    searchEnginesChanged() {
      for (let x = 0; x < this.searchEngines.options.length; x++) {
        if (this.searchEngines.select == this.searchEngines.options[x].value) {
          this.searchEngines.select_engine_id = this.searchEngines.options[
            x
          ].id;
          this.searchEngines.main_url = this.searchEngines.options[x].main_url;
          this.searchEngines.suggest_url = this.searchEngines.options[
            x
          ].suggest_url;
          this.searchEngines.suggest_func = this.searchEngines.options[
            x
          ].suggest_func;
          this.searchIcon = this.searchEngines.options[x].icon;
          return;
        }
      }
    },
    async searchEnginesGet() {
      try {
        const { data: res } = await axios.get(api.searchEngines);
        for (let s = 0; s < res.data.length; s++) {
          let suggest_url = default_suggest_url;
          let suggest_func = default_suggest_func;
          if (md5(res.data[s].suggest_func) == res.data[s].s) {
            suggest_url = res.data[s].suggest_url;
            suggest_func = res.data[s].suggest_func;
          }
          this.searchEngines.options.push({
            id: res.data[s].id,
            main_url: res.data[s].main_url,
            suggest_url: suggest_url,
            suggest_func: suggest_func,
            icon: res.data[s].icon,
            label: res.data[s].name,
            value: res.data[s].name,
          });
        }
        this.searchEngines.select = this.searchEngines.options[0].value;
        this.searchEngines.select_engine_id = this.searchEngines.options[0].id;
        this.searchEngines.main_url = this.searchEngines.options[0].main_url;
        this.searchEngines.suggest_url = this.searchEngines.options[0].suggest_url;
        this.searchEngines.suggest_func = this.searchEngines.options[0].suggest_func;
        this.searchIcon = this.searchEngines.options[0].icon;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async search() {
      var searchUrl = this.searchEngines.main_url.replace("%word%", this.word);
      window.open(searchUrl);
      this.autoComplete("");
      try {
        const { data: res } = await axios.post(api.searchLog, {
          user_id: this.user_id,
          engine_id: this.searchEngines.select_engine_id,
          search_text: this.word,
        });
      } catch (e) {
        console.log(e);
      }
      this.word = "";
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
        var autoCompleteUrl = this.searchEngines.suggest_url.replace(
          "%word%",
          this.word
        );
        try {
          let script = document.createElement("script");
          script.src = autoCompleteUrl;
          eval(this.searchEngines.suggest_func);
          document.querySelector("head").appendChild(script);
          document.querySelector("head").removeChild(script);
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error",
          });
        }
      }
    },
  },
  created() {
    this.searchEnginesGet();
  },
  mounted() {
    this.$refs["input"].focus();
  },
};
</script>
<style scoped>
.search-icon-div {
  padding-top: 80px;
  padding-bottom: 60px;
}
.search-icon {
  font-size: 100px;
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
