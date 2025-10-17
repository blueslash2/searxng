# SPDX-License-Identifier: AGPL-3.0-or-later  
"""BochaAI Web Search Engine  
  
BochaAI is a web search API that provides comprehensive search results.  
API documentation: https://open.bochaai.com  
"""  
  
from json import dumps  
from datetime import datetime  
  
# about  
about = {  
    "website": 'https://www.bochaai.com',  
    "wikidata_id": None,  
    "official_api_documentation": 'https://open.bochaai.com',  
    "use_official_api": True,  
    "require_api_key": True,  
    "results": 'JSON',  
}  
  
# ===== 在这里添加必需的引擎属性 =====
name = 'bochaai'        # 引擎名称
engine = 'bochaai'      # 引擎文件名（不含.py）
shortcut = 'bca'        # 快捷方式，与你在settings.xml中配置的一致
timeout = 5.0           # 超时时间（秒）
safesearch = False      # 是否支持安全搜索

# engine dependent config  
categories = ['general', 'web']  
paging = False  # BochaAI uses count parameter instead of pagination  
time_range_support = True  
  
# API settings  
base_url = 'https://api.bochaai.com'  
search_url = base_url + '/v1/web-search'  
api_key = ''  
  
# Time range mapping  
time_range_map = {  
    'day': 'oneDay',  
    'week': 'oneWeek',  
    'month': 'oneMonth',  
    'year': 'oneYear',  
}  
  
  
def request(query, params):  
    """Build the search request"""  
      
    if not api_key:  
        return None  
      
    params['url'] = search_url  
    params['method'] = 'POST'  
    params['headers'] = {  
        'Authorization': f'Bearer {api_key}',  
        'Content-Type': 'application/json'  
    }  
      
    # Build request body  
    request_data = {  
        'query': query,  
        'freshness': 'noLimit',  
        'count': 10  
    }  
      
    # Handle time range if specified  
    if params.get('time_range'):  
        time_range = time_range_map.get(params['time_range'], 'noLimit')  
        request_data['freshness'] = time_range  
      
    params['data'] = dumps(request_data)  
      
    return params  
  
  
def response(resp):  
    """Parse the search response"""  
    results = []  
      
    json_data = resp.json()  
      
    # Check response status  
    if json_data.get('code') != 200:  
        return results  
      
    data = json_data.get('data', {})  
    web_pages = data.get('webPages', {})  
      
    # Parse web search results  
    for item in web_pages.get('value', []):  
        result = {  
            'url': item.get('url', ''),  
            'title': item.get('name', ''),  
            'content': item.get('snippet', ''),  
        }  
          
        # Add optional fields if available  
        if item.get('datePublished'):  
            try:  
                # Handle the timezone issue mentioned in API docs  
                date_str = item['datePublished']  
                result['publishedDate'] = datetime.fromisoformat(date_str)  
            except (ValueError, TypeError):  
                pass  
          
        if item.get('thumbnail'):  
            result['thumbnail'] = item['thumbnail']  
          
        results.append(result)  
      
    return results