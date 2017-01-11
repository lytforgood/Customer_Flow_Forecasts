package ijcai

import org.apache.spark.{SparkConf, SparkContext}

/**
  * Created by yuyin on 17/1/11.
  * 用户,商户,年,月,日,时,星期
  * 22127870,1862,20151225,2015,12,25,17,5
  * 进行SQL处理
  */
object DataSQL {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("SparkWordCount").setMaster("local[2]")
    val sc = new SparkContext(conf)
    val sqlContext = new org.apache.spark.sql.SQLContext(sc)

    val path = "/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/user_pay_re/part-00000"
    case class user_pay(user_id:String,shop_id:String,time:Int,year:Int,mouth:Int,day:Int,minute:Int,week:Int)
    val data = sc.textFile(path).map(x => (x.split(",")(0), x.split(",")(1), x.split(",")(2), x.split(",")(3), x.split(",")(4), x.split(",")(5), x.split(",")(6), x.split(",")(7)))

    val df=data.map(x=>user_pay(x._1.toString,x._2.toString,x._3.toInt,x._4.toInt,x._5.toInt,x._6.toInt,x._7.toInt,x._8.toInt)).toDF()
    //    df.show(2)
    //将DataFrame注册成表commitlog
    df.registerTempTable("pay")
    //显示前2行数据
    val re=sqlContext.sql("SELECT * FROM pay where week=1")
    //去掉多余括号
    val re2=re.map(x=>x.toString().replaceAll("\\[","").replaceAll("\\]",""))
    re2.coalesce(1).saveAsTextFile("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/user_view_sql")

  }

}
