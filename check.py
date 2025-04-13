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






# import asyncio
# import httpx

# async def check(url: str, idx: int):
#     print(f"📌 {idx + 1}-so‘rov yuborildi")
#     try:
#         async with httpx.AsyncClient(follow_redirects=True) as client:
#             response = await client.get(
#                 "http://localhost:8000/youtube/media/",
#                 params={"yt_url": url},
#                 timeout=100
#             )
#             if response.status_code != 200:
#                 raise ValueError(f"Serverdan yomon javob: {response.status_code}")

#             try:
#                 result = response.json()
#             except ValueError as e:
#                 raise ValueError(f"Javob JSON formatida emas: {e}. Javob: {response.text}")

#     except Exception as e:
#         # Agar error details bo'sh bo'lsa fallback xabar qo'yamiz
#         error_details = str(e) or "No error details provided"
#         result = {"error": True, "details": error_details}

#     print(f"✅ {idx + 1}-javob tayyor")
#     return idx, result

# async def main():
#     url = "https://youtu.be/YsdZcpCFAPY?si=_OjHXX_iAY739Bls"
#     urls = [url] * 50  # 50 ta URL uchun so'rov

#     tasks = [asyncio.create_task(check(url, idx)) for idx, url in enumerate(urls)]
#     results = await asyncio.gather(*tasks)

#     correct_responses = 0
#     error_responses = 0

#     for idx, result in sorted(results, key=lambda x: x[0]):
#         if result.get("error"):
#             error_responses += 1
#             print(f"❌ Response {idx + 1}: Xato - {result}")
#         else:
#             correct_responses += 1
#             print(f"✅ Response {idx + 1}: To'g'ri")

#     print(f"\n📊 Xulosa:")
#     print(f"✅ To'g'ri javoblar: {correct_responses}")
#     print(f"❌ Xato javoblar: {error_responses}")

# asyncio.run(main())


# import asyncio
# import httpx
# async def check(url: str, idx: int):
#     print(f"📌 {idx + 1}-so‘rov yuborildi")
#     try:
#         async with httpx.AsyncClient(follow_redirects=True) as client:
#             response = await client.get(
#                 "http://localhost:8000/youtube/test/",
#                 params={"url": url},
#                 timeout=360
#             )
#             if response.status_code != 200:
#                 raise ValueError(f"Serverdan yomon javob: {response.status_code}")

#             try:
#                 result = response.json()
#             except ValueError as e:
#                 raise ValueError(f"Javob JSON formatida emas: {e}. Javob: {response.text}")

#     except Exception as e:
#         # Errorni yaxshiroq tekshirish va batafsil ma'lumot olish
#         error_details = repr(e) if hasattr(e, '__repr__') else str(e) or "No error details provided"
#         result = {"error": True, "details": error_details}

#     print(f"✅ {idx + 1}-javob tayyor")
#     return idx, result


# async def main():
#     url = "https://youtu.be/YsdZcpCFAPY?si=_OjHXX_iAY739Bls"
#     urls = [url] * 50  # 50 ta URL uchun so'rov

#     tasks = [asyncio.create_task(check(url, idx)) for idx, url in enumerate(urls)]
#     results = await asyncio.gather(*tasks)

#     correct_responses = 0
#     error_responses = 0

#     # Process the results
#     for idx, result in sorted(results, key=lambda x: x[0]):
#         if "error" in result and result["error"]:
#             error_responses += 1
#             print(f"❌ Response {idx + 1}: Xato - {result['details']}")
#         else:
#             correct_responses += 1
#             print(f"✅ Response {idx + 1}: Success - {result}")

#     print(f"\nTotal Correct Responses: {correct_responses}")
#     print(f"Total Error Responses: {error_responses}")
# asyncio.run(main())





# from secure_proxy import SecureProxyClient


# async def main():
#     client = SecureProxyClient(proxy_token="proxy_token")
#     response = await client.request(url="https://example.com")
#     print(response)

import asyncio
import aiofiles
from secure_proxy import SecureProxyClient

# PROXY_TOKEN = "59d9a6ba500b23deb274a0cb76d9e7f7"
#
# VIDEO_URL = "https://rr4---sn-q4flrnek.googlevideo.com/videoplayback?expire=1744511150&ei=Tsz6Z8G2Bay-kucPwdbGuQc&ip=2605%3A5fc2%3A200c%3Abc77%3A80ab%3Ae38b%3Ad3a7%3A87ea&id=o-AK7j8pznk6gPT5HusaEezYPnS6wvqL14CdzrMdkMdBSL&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1744489550%2C&mh=Kw&mm=31%2C26&mn=sn-q4flrnek%2Csn-a5mekn6d&ms=au%2Conr&mv=m&mvi=4&pl=32&rms=au%2Cau&initcwndbps=2388750&bui=AccgBcPomrw2C6oi3VTIawaVEsWzGkipSYawyeZZ7mG6ZF4EX5rEu-H4Mf-WgNiq-7yZsw50CXaaaiOq&vprv=1&svpuc=1&mime=audio%2Fmp4&ns=5ro9ThZD4eZaDih2afWwoBgQ&rqh=1&gir=yes&clen=7165249&dur=442.688&lmt=1718065243287985&mt=1744489021&fvip=3&keepalive=yes&lmw=1&c=TVHTML5&sefc=1&txp=5318224&n=5J8wJnp0Ogxekg&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRAIgN8k0XACgNlo8BkhR5rfFyXc2eYP3910_smJ5xAwSlosCIESb1zjGRp2SIMEs8_C7vaXFRbn8Kn3ow34t46WCpcqx&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=ACuhMU0wRQIgXC2gXI-lJEfMYskrBvWernE607UWQFWq5f-1ftJlDiYCIQDgC674ZJhl5alFvzOTjlzsVd34nd-yuHtkNpO5kBXaCw%3D%3D"
#
# OUTPUT_FILE = "video.m4a"
#
# async def download_video():
#     """ Video yuklab olish va saqlash """
#     client = SecureProxyClient(proxy_token=PROXY_TOKEN)
#
#     print("📥 Yuklab olinmoqda...")
#
#     # 🔗 Proxy orqali video faylni yuklab olish
#     content, status = await client.request(url=VIDEO_URL)
#     print(content, status)
#     if status != 200:
#         print(f"❌ Xatolik: HTTP {status}")
#         return
#
#     # 💾 Faylni saqlash
#     async with aiofiles.open(OUTPUT_FILE, "wb") as f:
#         await f.write(content)
#
#     print(f"✅ Video muvaffaqiyatli yuklandi! ({OUTPUT_FILE})")
#
# if __name__ == "__main__":
#     asyncio.run(download_video())


# import requests
# url = ""
# res = requests.post(url=)