const db = require("./mysql.js");


exports.all_list = (req,res)=>{
    let sql = "select * from qixin_data";
    let data = null;
    db.base(sql,data,(result)=>{
          res.json(result);
    })
};

