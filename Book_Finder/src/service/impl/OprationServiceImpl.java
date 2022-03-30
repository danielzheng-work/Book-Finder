package service.impl;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import service.OpeationService;

public class OprationServiceImpl implements OpeationService {

	@Override
	public boolean getKeyAndWordCloudByBookName(String bookName) {
		return (boolean) get("word_freq.py",bookName).get("flag");
	}

	@Override
	public Map<String,Object> getWebScraperByBookName(String asin) {
		return get("web_scraper.py",asin);
	}
	
	@Override
	public Map<String,Object> getMatchingBooks(String asin) {
		return get("graph.py",asin);
	}
	
	public Map<String,Object> get(String pythonName,String bookName) {
		Map<String,Object> map = new LinkedHashMap<String, Object>();
		boolean flag = false;
		try {
			File file = new File("");
	        String filePath = file.getCanonicalPath();
	        String exe = "";
	        // get the system os to make sure the python directory works across many machines 
			if (System.getProperty("os.name").equals("Windows 10")) {
				exe = "python";
			}
			else if (System.getProperty("os.name").equals("Mac OS X")){
				exe = "/usr/local/bin/python3";
			}
			String command = filePath+"/py/"+pythonName;
			System.out.println(command);
			String[] cmdArr = {exe,command,bookName};
			Process process = Runtime.getRuntime().exec(cmdArr,null,new File(filePath+"/py"));
			BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
			String line;
			List<String> lines = new LinkedList<String>();
			while( ( line = in.readLine() ) != null ) {
				System.out.println(line);
				lines.add(line);
			}
			map.put("data", lines);
			in.close();
			int result = process.waitFor();
			if(result == 0 ) {
				flag = true;
			}
			System.out.println("result:" + result);
		} catch (IOException | InterruptedException e) {
			e.printStackTrace();
		}
		map.put("flag", flag);
		return map;
	}

	@Override
	public Map<String,Object> init(String keyWord) {
		return get("json_sampler.py",keyWord);
	}

}
