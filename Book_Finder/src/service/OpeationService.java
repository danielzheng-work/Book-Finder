package service;

import java.util.Map;

public interface OpeationService {
	
	
	
	/**
	 * Generate wordcloud by book name
	 * @param bookName
	 * @return
	 */
	boolean getKeyAndWordCloudByBookName(String bookName);
	/**
	 * get book name by asin though web scraper
	 * @param bookName
	 * @return return map data type，data from python output，flag to check if it is success
	 */
	
	Map<String,Object> getWebScraperByBookName(String asin);
	
	
	/**
	 * Generate list of other books which use words from the top 5 most used words for a book
	 * @param asin
	 * @return
	 */	
	Map<String,Object> getMatchingBooks(String asin);
	
	
	/**
	 * initial
	 * @param keyWord
	 * @return 
	 */
	Map<String,Object> init(String keyWord);
}
