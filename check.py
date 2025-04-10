# import asyncio
# import httpx

# async def check(url, idx):
#     print(f"📌 {idx + 1}-so‘rov yuborildi") 
#     try:
#         async with httpx.AsyncClient(follow_redirects=True) as client:
#             response = await client.get("https://videoyukla.uz/youtube/media/", params={"yt_url": url}, timeout=25)
#             result = response.json()
#     except Exception as e:
#         result = {"error": "Xatolik yuz berdi, qayta urunib ko‘ring", "details": str(e)}

#     print(f"✅ {idx + 1}-javob tayyor")  
#     return idx, result

# async def main():
#     # url = "https://www.instagram.com/stories/imperatoruz" stoires
#     # url = "https://www.instagram.com/p/DH5gya1xo6H/?utm_source=ig_web_copy_link" one pic
#     # url = "https://www.instagram.com/p/DHgWbewsTwH/?utm_source=ig_web_copy_link" # album and image
#     url = "https://youtu.be/k26urW-idB8?si=k3LTr3x7Bj3RSHlC" # album images

#     urls = [url] * 50  
    
#     tasks = [asyncio.create_task(check(url, idx)) for idx, url in enumerate(urls)]  

#     results = await asyncio.gather(*tasks)  

#     for idx, result in sorted(results, key=lambda x: x[0]):
#         print(f"🔍 Response {idx + 1}: {result}")

# asyncio.run(main())



# from secure_proxy import SecureProxyClient
# import aiofiles

# url = "https://rr4---sn-q4fl6nsl.googlevideo.com/videoplayback?expire=1744270069&ei=lR73Z6v-JM-AkucPw5XegA4&ip=2605%3A5fc2%3A1896%3Aedbb%3A9505%3A5867%3Ab2b9%3A55fa&id=o-ACHUeLzaNMu7vwbMHbasVDI5598MT5cnu14t0Fy7Td2Q&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1744248469%2C&mh=bg&mm=31%2C26&mn=sn-q4fl6nsl%2Csn-a5msen7z&ms=au%2Conr&mv=m&mvi=4&pl=32&rms=au%2Cau&initcwndbps=2201250&bui=AccgBcN14g2ZfnASegfxbZFc0mN_i-4x8hqRxwjmR-_Y2VmdLSVpxBRPNbwTOrwlB7QLiAt9tgqhx6vp&vprv=1&svpuc=1&mime=video%2Fmp4&ns=to-UDNr49wlNaLuLkvdlxOUQ&rqh=1&gir=yes&clen=38510712&ratebypass=yes&dur=1040.161&lmt=1744204629190684&mt=1744248060&fvip=3&lmw=1&c=TVHTML5&sefc=1&txp=3309224&n=jCA4JQXaGKgH0w&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRAIgMFWJUYCKLNMFY_x74iy-6339rlQD_wtY2pjnO98t00oCIBB9urhqU2nTzPp4pSbgHsIcKlZ8-jqXYlgs25jkj-lJ&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=ACuhMU0wRgIhAOT-4VoCfRybwkyAQkH0AT9Bz_fM0Tkg-DGAbLQekD0PAiEAki0Y889S5Nqlw8qaR11gBf3EKewPJQEDV1OIWNLBgWU%3D"
# async def check(token: str, file_path: str, url: str):
#     client = SecureProxyClient(proxy_token=token)
#     content, status = await client.request(url=url)
#     if status != 200:
#         print(f"❌ Xatolik: HTTP {status}")
#         return
#     async with aiofiles.open(file_path, "wb") as f:
#         await f.write(content)
#     return file_path

# async def main():
#     token = "cac19de53bec89e9343a4dfe532be215"
#     file_path = "media/1.mp4"
#     await check(token, file_path, url)
# import asyncio
# asyncio.run(main())