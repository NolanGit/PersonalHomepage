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
import {
  searchEnginesData,
  searchEnginesAutoComplete,
  searchLog
} from "../api/search";

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
    searchEnginesDataFront() {
      searchEnginesData().then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          for (let s = 0; s < data.data.length; s++) {
            this.searchEngines.options.push({
              id: data.data[s].id,
              main_url: data.data[s].main_url,
              auto_complete_url: data.data[s].auto_complete_url,
              icon: data.data[s].icon,
              label: data.data[s].name,
              value: data.data[s].name
            });
          }
          this.searchEngines.select = this.searchEngines.options[0].value;
          this.searchEngines.select_engine_id = this.searchEngines.options[0].id;
          this.searchEngines.main_url = this.searchEngines.options[0].main_url;
          this.searchEngines.auto_complete_url = this.searchEngines.options[0].auto_complete_url;
        }
      });
    },
    search() {
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
      let para = {
        user: user,
        engine: this.searchEngines.select_engine_id,
        search_text: this.word
      };
      searchLog(para).then(data => {
        if (data["code"] !== 200) {
          console.log(data["msg"]);
        } else {
        }
      });
      this.word = "";
    },
    autoComplete(queryString, cb) {
      if (
        queryString === "" ||
        queryString === [] ||
        queryString === undefined
      ) {
        cb([]);
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
          var para = {
            autoCompleteUrl: autoCompleteUrl,
            name: this.searchEngines.select,
            user: user
          };
          searchEnginesAutoComplete(para).then(data => {
            function String2Dict(x) {
              return {
                value: x
              };
            }
            var result = data.data.map(String2Dict);
            sessionStorage.setItem(
              "lastWordAutoComplete",
              JSON.stringify(result)
            );
            cb(result);
          });
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
