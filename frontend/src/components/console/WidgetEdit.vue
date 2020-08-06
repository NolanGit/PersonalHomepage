<template>
  <div>
    <SlickList
      :lockToContainerEdges="true"
      axis="x"
      lockAxis="x"
      v-model="items"
      class="slick_list"
      @input="getChangeLists"
    >
      <SlickItem v-for="(item, index) in items" class="slick_list_item" :index="index" :key="index">
        {{ item.name }}
        <SlickList :lockToContainerEdges="true" class="slick_list" lockAxis="y" v-model="item.itemArr">
          <SlickItem
            class="slick_list_item"
            v-for="(item, index) in item.itemArr"
            :index="index"
            :key="index"
          >{{ item }}</SlickItem>
        </SlickList>
      </SlickItem>
    </SlickList>
  </div>
</template>
<script>
import axios from "axios";
import { SlickList, SlickItem } from "vue-slicksort";
const api = {
  get: "/widget/get",
  suiteGet: "/widget/suite/get",
};

export default {
  name: "widgetEdit",
  props: {
    user_id: Number,
  },
  components: {
    SlickItem,
    SlickList,
  },
  watch: {},
  data() {
    return {
      items: [
        {
          name: "title1",
          itemArr: ["Item1", "Item2", "Item3"],
        },
        {
          name: "title2",
          itemArr: ["Item4", "Item5", "Item6"],
        },
        {
          name: "title3",
          itemArr: ["Item7", "Item8", "Item9"],
        },
      ],
    };
  },
  methods: {},
  mounted() {},
};
</script>
<style scoped>
body,
html {
  -moz-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}
h3,
h4 {
  text-align: center;
}
.list {
  max-height: 80vh;
  margin: 0 auto;
  padding: 0;
  overflow: auto;
  background-color: #f3f3f3;
  border: 1px solid #efefef;
  max-width: 600px;
  cursor: pointer;
}
.list-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 20px;
  background-color: #fff;
  border-bottom: 1px solid #efefef;
  box-sizing: border-box;
  user-select: none;
  color: #333;
  font-weight: 400;
}
.stylizedHelper {
  background: blue;
  color: #fff;
}
.SortableList {
  display: flex;
  width: 600px;
  white-space: nowrap;
  max-height: 80vh;
  margin: 0 auto;
  padding: 0;
  overflow: auto;
  background-color: #f3f3f3;
  border: 1px solid #efefef;
  cursor: pointer;
}
.SortableItem {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 20px;
  background-color: #fff;
  border-bottom: 1px solid #efefef;
  box-sizing: border-box;
  user-select: none;
  color: #333;
  font-weight: 400;
  border: 1px solid #ccc;
}
.SortableList2 {
  width: 300px;
  margin: 20px auto;
  border: 1px solid #efefef;
}
.SortableItem2 {
  width: 300px;
  border: 1px solid #efefef;
  text-align: center;
}
.SortableItem2 p {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  background: #efefef;
  margin: 0;
  height: 30px;
}
</style>
