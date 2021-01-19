const express =require("express");
const router = express.Router();
const service = require("./service.js");




//从all_list表中获取统计后的物料信息
router.get("/lists",service.all_list);//主页显示数据调用


module.exports = router;