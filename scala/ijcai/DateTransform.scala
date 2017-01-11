package ijcai

import java.text.{DecimalFormat, SimpleDateFormat}
import java.util.{Calendar, Date}

/**
  * Created by yuyin on 17/1/11.
  * 时间转换的例子
  * 导入jar包的快捷键alt+enter（光标紧跟在类的后面）
  */
object DateTransform {

  def main(args: Array[String]): Unit = {
//    print("现在时间："+getNowDate())
//    print("昨天时间："+getYesterday())
//    print("本周开始"+getNowWeekStart())
//    print("本周结束"+getNowWeekEnd())
//
//    print("本月开始"+getNowMonthStart())
//    print("本月结束"+getNowMonthEnd())
//
//    print("\n")
//
//    print(timeFormat("1436457603"))
//    print(DateFormat("1436457603"))

//    cal.set(Calendar.DATE, 1)
//     cal.get(Calendar.DAY_OF_WEEK);
    print(getWeeks("20170108"))

  }

  //获取今天日期
  def getNowDate():String={
    var now:Date = new Date()
    var  dateFormat:SimpleDateFormat = new SimpleDateFormat("yyyy-MM-dd")
    var hehe = dateFormat.format(now)
    hehe
  }
  //获取昨天的日期
  def getYesterday():String= {
    var dateFormat: SimpleDateFormat = new SimpleDateFormat("yyyy-MM-dd")
    var cal: Calendar = Calendar.getInstance()
    cal.add(Calendar.DATE, -1)
    var yesterday = dateFormat.format(cal.getTime())
    yesterday
  }
  //获取本周开始日期
  def getNowWeekStart():String={
    var period:String=""
    var cal:Calendar =Calendar.getInstance();
    var df:SimpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
    cal.set(Calendar.DAY_OF_WEEK, Calendar.MONDAY)
    //获取本周一的日期
    period=df.format(cal.getTime())
    period
  }
  //获取本周末的时间
  def getNowWeekEnd():String={
    var period:String=""
    var cal:Calendar =Calendar.getInstance();
    var df:SimpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
    cal.set(Calendar.DAY_OF_WEEK, Calendar.SUNDAY);//这种输出的是上个星期周日的日期，因为老外把周日当成第一天
    cal.add(Calendar.WEEK_OF_YEAR, 1)// 增加一个星期，才是我们中国人的本周日的日期
    period=df.format(cal.getTime())
    period
  }
  //本月的第一天
  def getNowMonthStart():String={
    var period:String=""
    var cal:Calendar =Calendar.getInstance();
    var df:SimpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
    cal.set(Calendar.DATE, 1)
    period=df.format(cal.getTime())//本月第一天
    period
  }
  //本月的最后一天
  def getNowMonthEnd():String={
    var period:String=""
    var cal:Calendar =Calendar.getInstance();
    var df:SimpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
    cal.set(Calendar.DATE, 1)
    cal.roll(Calendar.DATE,-1)
    period=df.format(cal.getTime())//本月最后一天
    period
  }
  //将时间戳转化成日期
  def DateFormat(time:String):String={
    var sdf:SimpleDateFormat = new SimpleDateFormat("yyyy-MM-dd")
    var date:String = sdf.format(new Date((time.toLong*1000l)))
    date
  }
  //时间戳转化为时间，原理同上
  def timeFormat(time:String):String={
    var sdf:SimpleDateFormat = new SimpleDateFormat("HH:mm:ss")
    var date:String = sdf.format(new Date((time.toLong*1000l)))
    date
  }
  //计算时间差
  //核心工作时间，迟到早退等的的处理
  def getCoreTime(start_time:String,end_Time:String)={
    var df:SimpleDateFormat=new SimpleDateFormat("HH:mm:ss")
    var begin:Date=df.parse(start_time)
    var end:Date = df.parse(end_Time)
    var between:Long=(end.getTime()-begin.getTime())/1000//转化成秒
    var hour:Float=between.toFloat/3600
    var decf:DecimalFormat=new DecimalFormat("#.00")
    decf.format(hour)//格式化

  }

  //判断周几
  def getWeeks(date_string:String)={
    val df:SimpleDateFormat=new SimpleDateFormat("yyyyMMdd")
    val tmp:Date=df.parse(date_string)
    val cal:Calendar = Calendar.getInstance()
    cal.setTime(tmp)
    var w:Int = cal.get(Calendar.DAY_OF_WEEK) - 1
    //周日标为7
    if (w == 0) {
      w = 7
    }
    w
  }


}
