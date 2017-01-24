package mahout.MahoutInAction_code;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
//Evaluate
public class Evaluate {
	private String trueurl;
	private String preurl;
	private final int T = 14;
	private final int N = 2000;
	private Map<String, Double> allscore;
	public Evaluate(String trueurl,String preurl){
		this.trueurl = trueurl;
		this.preurl = preurl;

	}



	public double score() throws IOException{


		BufferedReader tf = new BufferedReader(new FileReader(trueurl));
		BufferedReader pf = new BufferedReader(new FileReader(preurl));
		String truetemp = tf.readLine();
		String pretemp = pf.readLine();
		allscore = new HashMap<String, Double>();
		double score = 0.0;
		while(truetemp!=null){
			String trueArray[] = truetemp.split(",");
			String preArray[] = pretemp.split(",");
			String shopid = trueArray[0];
			Double tArray[] = new Double[trueArray.length-1];
			Double pArray[] = new Double[trueArray.length-1];
			for (int i = 1; i < trueArray.length; i++) {
				tArray[i-1] = Double.parseDouble(trueArray[i]);
				pArray[i-1] = Double.parseDouble(preArray[i]);

			}
			double itemscore = 0.0;
			for (int i = 0; i < pArray.length; i++) {

				double a = pArray[i] - tArray[i];
				double b = pArray[i] + tArray[i];
				double c = 0.0;
				try{
				c = Math.abs(a/b);}catch(Exception e){c=0.0;}
				itemscore+=c;
			}
			score += itemscore;
			allscore.put(shopid, itemscore);


			pretemp = pf.readLine();
			truetemp = tf.readLine();
		}
		tf.close();
		pf.close();

		return score/(N*T);
	}
	public List<Entry<String,Double>> sortByscore(){
		List<Entry<String, Double>> list = new ArrayList<Entry<String,Double>>(allscore.entrySet());
		Collections.sort(list,new Comparator<Entry<String,Double>>() {
			 public int compare(Map.Entry<String, Double> o1,
			            Map.Entry<String, Double> o2) {
			        return o1.getValue().compareTo(o2.getValue())*(-1);


			 }
	});
		return list;
	}


	public static void main(String[] args) throws IOException {
		//输入的文件要一一对应
		Evaluate e = new Evaluate("/Users/master/Desktop/stltest", "/Users/master/Desktop/stlpre");
		double score = e.score();//计算成绩

		List<Entry<String,Double>> list = e.sortByscore();
		//每个商家误差倒序排序
		System.out.println(score);
		/*
		for (Entry<String, Double> entry : list) {
			System.out.println(entry.getKey()+":"+entry.getValue());
		}
		*/
		e.allscore.get("");//等到某个商家的误差



	}
}
