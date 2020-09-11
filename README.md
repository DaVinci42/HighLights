# Tools to manage clippings

- [x] Kindle
    - [x] Parse `My Clippings.txt` to `Clipping` type        
    - [x] Sync to Notion, with default or customized layout
- [ ] KoReader
    - [ ] Parse clippings from KoReader
    - [ ] Sync to Notion

---

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

