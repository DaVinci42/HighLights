# Tools to manage clippings

- [x] Kindle
    - [x] Parse `My Clippings.txt` to `Clipping` type        
    - [x] Sync to Notion, with default or customized layout
- [x] KoReader
    - [x] Parse clippings from KoReader
    - [x] Sync to Notion

---
***5 sec delay after each book, to avoid exceeding API limit***

* Sync Kindle Clippings To Notion

  ```python
  syncer.sync_kindle(
  	# token_v2 from your cookie    
  	token="",  
  
  	# url of your target notion page
  	page="",
  
  	# your 'My Clippings' file path
  	file_path="", 
  	
  	# optional, just in case you wanna customize layout
  	page_render: Callable[[BasicBlock, List[List[Clipping]]], None]  
  )
  ```

* Sync KoReader Clippings
  
  ```python
  syncer.sync_koreader(
      token: str,
      page: str,
      
      # your clipping folder, or single clipping.html
      path: str,
      page_render: Callable[[BasicBlock, List[Tuple[str, List[str]]], bool], None] = render_koreader_page,
      # replace will add TOC, if not will just append
      replace: bool = False
  )
  ```
  
  

