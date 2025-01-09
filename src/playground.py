import requests


cookies = {
    '_cls_v': 'f80f52ff-471b-4557-8b4a-f66718fd36ef',
    '_cls_s': 'a6a9955f-75e8-4c3f-b384-65ae82beb194:0',
    'byInitialState_wy9yZSmxjBQzxhoxpszOlg%3d%3d': '',
    'rto': 'c0',
    'com.silverpop.iMAWebCookie': '7bcdd635-18c6-0154-aee1-86470dc96267',
    'usfu_wy9yZSmxjBQzxhoxpszOlg%3d%3d': 'true',
    'com.silverpop.iMA.session': '53be918a-1a05-a7c3-c54a-218bd8698e60',
    'com.silverpop.iMA.page_visit': '2136470536:',
    'TS991741c8027': '0807fcf310ab20001cfa7785e1ca89e46458572d3801974314b40048802d9fad1c2ca8265a90b75308a2298aa71130009425ace6e9c72e4796597fccaaf45b4cbf886d2536c10410bfb0dbb87e169251bcb5582be6246f90201abca0f0cd9628',
}

headers = {
    'Accept': 'application/json; charset=utf-8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJNYWNjYWJpIiwiYXVkIjoiTWFjY2FiaSIsImlhdCI6MTczNjM4MDYxNDE5NSwiZXhwIjoxNzM2MzgxMjE0MTk1LCJvcmlnIjoiaHR0cHM6Ly9vbmxpbmUubWFjY2FiaTR1LmNvLmlsIiwiUmVsYXlTdGF0ZSI6IiIsImFjcyI6Imh0dHBzOi8vb25saW5lLm1hY2NhYmk0dS5jby5pbC9zYW1sL3NwL3Byb2ZpbGUvcG9zdC9hY3MifQ.BUlnW4Xg1a678_512epiL2IUHgdT9k3hhHwGMzG6ByCjrsX-Enggkp8caUm4pg8seu1hDjgpEqgOH7NmXxaczROpdrLmSzPz6tuWABOpTvAIQOZ2Qx0KSFX_6b7ZJIBPQWSWooSvQVLBG-kv3_5KHjHMtymeidnx6b1yTohjXNyB6lzX2R5ivU2ql5jJ0VwS3OZUJ2WXmedfdvQTqyq5kzX6S2Bw3kbMKNF-AF-ASbXZeX-MNA9y8FBdttzOAEkp2VXGZq5PtY0fSwJXaixzlLFDIJ7coPM-ByNtvmu7Nb9JrrZQD-x_gGjkp_WeUfzjs03XneAKqIqVhh0y8QggrQ',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    # 'Cookie': '_cls_v=f80f52ff-471b-4557-8b4a-f66718fd36ef; _cls_s=a6a9955f-75e8-4c3f-b384-65ae82beb194:0; byInitialState_wy9yZSmxjBQzxhoxpszOlg%3d%3d=; rto=c0; com.silverpop.iMAWebCookie=7bcdd635-18c6-0154-aee1-86470dc96267; usfu_wy9yZSmxjBQzxhoxpszOlg%3d%3d=true; com.silverpop.iMA.session=53be918a-1a05-a7c3-c54a-218bd8698e60; com.silverpop.iMA.page_visit=2136470536:; TS991741c8027=0807fcf310ab20001cfa7785e1ca89e46458572d3801974314b40048802d9fad1c2ca8265a90b75308a2298aa71130009425ace6e9c72e4796597fccaaf45b4cbf886d2536c10410bfb0dbb87e169251bcb5582be6246f90201abca0f0cd9628',
    'Origin': 'https://mac.maccabi4u.co.il',
    'Pragma': 'no-cache',
    'Referer': 'https://mac.maccabi4u.co.il/login?SAMLRequest=fZLbTsMwDIZfpcr9mrRlY43WSmUTYhKHaitccIOy1NsipUmJUw5vT9eBGELatX9%2Ftj95hqLRLS86vzcreO0AffDRaIN8KGSkc4ZbgQq5EQ0g95Kvi7tbHoeMt856K60mQYEIzitr5tZg14Bbg3tTEh5XtxnZe98ip9QarQyEjZBSbNRFF0obKk0Pgyi2tKdtlQbaWvRUSCTBot9GGXHg%2FlL69n8IbXfKkGC5yMhLGkUwTlhU1%2BM0nkh5KSZiGiViComU8TZN67pOkz6M2MHSoBfGZyRm8XjEohGbVnHCWcIjFjIWP5Pg2joJg5%2BMbIVGIEH5ffeVMrUyu%2FOSNscQ8puqKkflw7oiwRM4HI7qAySfHQzwYR93Iv88VvwYJ%2Fl5vzN6gj%2FOavl9z1suSquV%2FAwKre373IHwkBHvOiA0P3b9fYz8Cw%3D%3D&SigAlg=http%3A%2F%2Fwww%2Ew3%2Eorg%2F2000%2F09%2Fxmldsig%23rsa%2Dsha1&Signature=Zjgh5qn8K%2ByJzKxyv82rv0souU4h9%2B9IzxFddD2CL1RbXv8%2BWk2WvGpL7bgt5C33t1ygyMQB3PZfh5hQOtO5RswEgdO9UoIaxOWt9oWIUkkZt7eTeHe9ePr7TnuROLbN4WS9tvZ4rwxwVOTZFjfRKW8K8Bqw0%2BNXsASIW6Ieh%2BnLlNYkCxXZiBIRvZ1iPyXcEK9uCy12%2FK1mZfm5s0EnUU80AptvcYqQP5q2nHQOdE0ZHy9%2FNQHHOUSxHuCv9kK%2BwbNmb0LXeuNzVJW1EMfwKjsJHm2zeYDKN%2B4jfcqFy8yplyO2Hj5pkcL3hFQ11M%2Fr7XDBvoSHr4c7ZQ1JTe%2B2ww%3D%3D',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'type': 'password',
    'id': '0-307518472',
    'password': 'Candy007',
}

url = 'https://mac.maccabi4u.co.il/infosec/auth'
# response = requests.post(url, cookies=cookies, headers=headers, json=json_data)
session = requests.Session()
response = session.post(url, json=json_data, headers=headers, cookies=cookies)

print(response.json())