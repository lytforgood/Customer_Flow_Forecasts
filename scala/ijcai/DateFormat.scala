package ijcai

import java.text.SimpleDateFormat
import java.util.{Calendar, Date, Locale}

import org.apache.spark.{SparkConf, SparkContext}

/**
  * Created by yuyin on 17/1/11.
  * 22127870,1862,2015-12-25 17:00:00
  * 数据格式化为 用户,商户,年,月,日,时,星期
  * 22127870,1862,20151225,2015,12,25,17,5
  */
object DateFormat {

  def main(args: Array[String]) {
    //    //传入的参数为 输入目录 输出目录
    //    if (args.length != 2) {
    //      System.err.println("Usage: input  output")
    //      System.exit(1)
    //    }
    //  }

    val conf = new SparkConf().setAppName("SparkWordCount").setMaster("local[2]")
    val sc = new SparkContext(conf)
    //  val line=sc.textFile(args(0)).flatMap(_.split(","))
    val path = "/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/user_view.txt"
//    val path = "/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/user_pay.txt"

    //  val line = sc.textFile(path).flatMap(_.split(","))
    //时间转换
    def change01(x: String): String = {
      val loc = new Locale("en")
      val fm = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", loc)
      val fm2 = new SimpleDateFormat("yyyyMMdd", loc)
      val dt2 = fm.parse(x)
      fm2.format(dt2)
    }

    //判断周几
    def getWeeks(date_string:String)={
      val df:SimpleDateFormat=new SimpleDateFormat("yyyyMMdd")
      val tmp:Date=df.parse(date_string)
      val cal:Calendar = Calendar.getInstance()
      cal.setTime(tmp)
      var w:Int = cal.get(Calendar.DAY_OF_WEEK) - 1
      if (w == 0) {
        w = 7
      }
      w
    }

    val line = sc.textFile(path).map(x => (x.split(",")(0), x.split(",")(1), change01(x.split(",")(2)), x.split(",")(2).substring(11, 13)))

    val re = line.map(x => (x._1, x._2, x._3, x._3.substring(0, 4), x._3.substring(4, 6), x._3.substring(6, 8), x._4,getWeeks(x._3)))
//    re.take(2)
    //re2去掉括号  coalesce(1)生成单文件
    val re2=re.map(x=>x.toString().replaceAll("\\(","").replaceAll("\\)",""))
    re2.coalesce(1).saveAsTextFile("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/user_view_re")

//    re2.coalesce(1).saveAsTextFile("/Users/yuyin/Downloads/笔记学习/天池比赛/IJCAI-17口碑商家客流量预测/data/dataset/user_pay_re")

    sc.stop()

  }
}
