val path = "/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/user_pay_re/part-00000"

val path = "/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/user_view_re/part-00000"
case class user_pay(user_id:String,shop_id:String,time:Int,year:Int,mouth:Int,day:Int,minute:Int,week:Int)

val data = sc.textFile(path).map(x => (x.split(",")(0), x.split(",")(1), x.split(",")(2), x.split(",")(3), x.split(",")(4), x.split(",")(5), x.split(",")(6), x.split(",")(7)))

val df=data.map(x=>user_pay(x._1.toString,x._2.toString,x._3.toInt,x._4.toInt,x._5.toInt,x._6.toInt,x._7.toInt,x._8.toInt)).toDF()
    //    df.show(2)
    //将DataFrame注册成表
df.registerTempTable("pay")

df.registerTempTable("view")
    //显示前2行数据
val re=sqlContext.sql("SELECT * FROM pay where week=1")
    //去掉多余括号
val re2=re.map(x=>x.toString().replaceAll("\\[","").replaceAll("\\]",""))
re2.coalesce(1).saveAsTextFile("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/re_sql")
//商家每天支付的支付行为次数
val re=sqlContext.sql("SELECT shop_id,time,year,mouth,day,count(user_id) FROM pay group by shop_id,time,year,mouth,day")
val re2=re.map(x=>x.toString().replaceAll("\\[","").replaceAll("\\]",""))
re2.coalesce(1).saveAsTextFile("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/re_sql")
///商家每天支付的用户人数（去掉重复来的人数）
val re=sqlContext.sql("SELECT shop_id,time,year,mouth,day,count(distinct user_id) FROM pay group by shop_id,time,year,mouth,day")

//商家每天浏览的浏览次数
val re=sqlContext.sql("SELECT shop_id,time,year,mouth,day,count(user_id) FROM view group by shop_id,time,year,mouth,day")
//商家每天浏览的用户人数
val re=sqlContext.sql("SELECT shop_id,time,year,mouth,day,count(distinct user_id) FROM view group by shop_id,time,year,mouth,day")




    val sortEntity = sc.textFile(args(0)).map(x=>{
      val lineArray = x.split("\t")
      val entityarray = lineArray(1).split(",")
      val entity = try{entityarray(0)}catch {case _ => ""}
      val entityweight = try{entityarray(1).toDouble}catch {case _=> 0}
      (entity,entityweight)

    }).reduceByKey(_+_).sortBy(x=>x._2,false).zipWithIndex().map(x=>{
      val entity = x._1._1
      val index = x._2
      val readcount = x._1._2
      (entity,index,readcount)
    }).persist()
    val count = sortEntity.count()
    //归一化
    sortEntity.map(x=>{
      val entity = x._1
      val index = x._2.toDouble / count.toDouble
      val readcount = x._3
      entity+","+index+","+readcount
    }).saveAsTextFile(args(1))
