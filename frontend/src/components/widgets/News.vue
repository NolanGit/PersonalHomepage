<template>
  <section>
    <el-row>
      <el-col :span="6">
        <el-card>
          <!-- title area -->
          <el-row>
            <el-radio-group v-model="radio1">
              <el-radio-button label="上海"></el-radio-button>
              <el-radio-button label="北京"></el-radio-button>
              <el-radio-button label="广州"></el-radio-button>
              <el-radio-button label="深圳"></el-radio-button>
            </el-radio-group>
          </el-row>
          <!-- content area -->
          <el-row> </el-row>
        </el-card>
      </el-col>
    </el-row>
  </section>
</template>