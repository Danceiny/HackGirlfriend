package com.iflytek.util;

import java.text.SimpleDateFormat;

public class Utils {
	
	public static String getAppid()
	{
		return "59201208";
	}
	
	public static boolean isEmpty(String string){
		if(string == null)
		{
			return true;
		}
		if(string.isEmpty())
		{
			return true;
		}
		return false;
	}
	
	public static void Log(String log)
	{
		SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"); 
		String date=dateFormat.format(new java.util.Date());
		if(true)
		    System.out.println("<" + date + ">" + log);
	}
}
