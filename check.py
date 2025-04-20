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

PROXY_TOKEN = "ed7969c47d92e19950de9af5e8b787c1"

VIDEO_URL = "https://rr4---sn-q4flrnek.googlevideo.com/videoplayback?expire=1744826291&ei=U5v_Z8KlOcG1kucPu_b6oAI&ip=2605%3A5fc2%3A73b5%3Abef5%3A4df8%3Aa731%3A6a23%3A297&id=o-AJW74LEa6uwTwFIKFV2KLdmflT3jt92ZFzlZwAVv0gJP&itag=249&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1744804691%2C&mh=B4&mm=31%2C29&mn=sn-q4flrnek%2Csn-q4fl6n6s&ms=au%2Crdu&mv=m&mvi=4&pl=32&rms=au%2Cau&initcwndbps=2407500&bui=AccgBcP4brezWoTShorCSY0-GFO0DDfKS_eFKgWIWNYOmVQNoXmCFy-vmc5jqVVCfvD0chK0NfhY51ax&vprv=1&svpuc=1&mime=audio%2Fwebm&ns=1yO8v4Z4K4_jErMi0H6icFgQ&rqh=1&gir=yes&clen=3775526&dur=604.961&lmt=1743855214229886&mt=1744804150&fvip=2&keepalive=yes&lmw=1&c=TVHTML5&sefc=1&txp=5532534&n=-63LNIlCyzhb-w&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=ACuhMU0wRQIhAN1bYZHIVohFaFwMgBMzGT1qkMDiK4EwA4R-Yd7WB69wAiBSD6azI2AzH_mdOJjzWTrwE26ASypbQWvS1a69P3TG_w%3D%3D&sig=AJfQdSswRQIgaRsM2kP4Q0_YHf0eVphIEaGwmfdrnIZhyUoJWW4utY0CIQCHxiPPG6PYm_4e2Jrb64m2vdU3gONfvBU4fxxPc9hnBQ%3D%3D"

OUTPUT_FILE = "video.webm"

async def download_video():
     """ Video yuklab olish va saqlash """
     client = SecureProxyClient(proxy_token=PROXY_TOKEN)

     print("📥 Yuklab olinmoqda...")

     # 🔗 Proxy orqali video faylni yuklab olish
     content, status = await client.request(url=VIDEO_URL)
     print(content, status)
     if status != 200:
         print(f"❌ Xatolik: HTTP {status}")
         return

     # 💾 Faylni saqlash
     async with aiofiles.open(OUTPUT_FILE, "wb") as f:
         await f.write(content)

     print(f"✅ Video muvaffaqiyatli yuklandi! ({OUTPUT_FILE})")

# if __name__ == "__main__":
#      asyncio.run(download_video())


# import requests
# url = ""
# res = requests.post(url=)


import httpx
import asyncio

async def download_audio(url: str, output_path: str):
    try:
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            print("Ketti")
            response = await client.get(url)
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)

        print(f"✅ Audio saqlandi: {output_path}")
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP status xatolik: {e.response.status_code} - {e}")
    except Exception as e:
        print(f"❌ Boshqa xatolik: {e}")

# Misol uchun test qilish:
# if __name__ == "__main__":
    # url = "https://rr4---sn-q4flrnek.googlevideo.com/videoplayback?expire=1744826291&ei=U5v_Z8KlOcG1kucPu_b6oAI&ip=2605%3A5fc2%3A73b5%3Abef5%3A4df8%3Aa731%3A6a23%3A297&id=o-AJW74LEa6uwTwFIKFV2KLdmflT3jt92ZFzlZwAVv0gJP&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1744804691%2C&mh=B4&mm=31%2C29&mn=sn-q4flrnek%2Csn-q4fl6n6s&ms=au%2Crdu&mv=m&mvi=4&pl=32&rms=au%2Cau&initcwndbps=2407500&bui=AccgBcNprv-FNDM2uMXNHYrds48j4EPhv5YrFImTD2yu9phtmgbmKJwD0t1F5E3BIm2Sq9-woW83-K_o&vprv=1&svpuc=1&mime=video%2Fmp4&ns=m5x4rv2OiH75bBzkdjvYqSgQ&rqh=1&cnr=14&ratebypass=yes&dur=604.995&lmt=1743860981674372&mt=1744804150&fvip=2&lmw=1&c=TVHTML5&sefc=1&txp=5538534&n=eKClj9xOMAsRmQ&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Ccnr%2Cratebypass%2Cdur%2Clmt&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=ACuhMU0wRQIhAN1bYZHIVohFaFwMgBMzGT1qkMDiK4EwA4R-Yd7WB69wAiBSD6azI2AzH_mdOJjzWTrwE26ASypbQWvS1a69P3TG_w%3D%3D&sig=AJfQdSswRgIhAJiyPzEuRlGfMk-lwt-ayyakQV8EOplmndYMma3lc12vAiEAjy3D7zvaZcQcwJJlJjFJq4m-4iJV8Xm78ZZ05pRSqD4%3D"
    # output_path = "media/test_audio.mp4"
    # asyncio.run(download_audio(url, output_path))



# import requests

# url = "https://instagram-media-downlaoder.p.rapidapi.com/instagram/media/service/"

# querystring = {"in_url":"https://www.instagram.com/reel/DIZD7JfiIKQ/?utm_source=ig_web_copy_link"}

# headers = {
# 	"X-RapidAPI-Key": "4a6adb31edmsh5a2e06261669117p1aaeeejsn7676eb48c8f1",
# 	"X-RapidAPI-Host": "instagram-media-downlaoder.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, json=querystring)

# print(response.json())


# import requests

# url = "https://instagram-media-downlaoder.p.rapidapi.com/instagram/media/"

# querystring = {"in_url":"https://www.instagram.com/reel/DIZD7JfiIKQ/?utm_source=ig_web_copy_link"}

# headers = {
#     "X-RapidAPI-Key": "4a6adb31edmsh5a2e06261669117p1aaeeejsn7676eb48c8f1",
#     "X-RapidAPI-Host": "instagram-media-downlaoder.p.rapidapi.com",
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

# import requests

# url = "https://instagram-media-downlaoder.p.rapidapi.com/instagram/media/service/"

# payload = { "url": "https://www.instagram.com/reel/DIZD7JfiIKQ/?utm_source=ig_web_copy_link" }
# headers = {
# 	"x-rapidapi-key": "4a6adb31edmsh5a2e06261669117p1aaeeejsn7676eb48c8f1",
# 	"x-rapidapi-host": "instagram-media-downlaoder.p.rapidapi.com",
# 	"Content-Type": "application/json"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.json())

# import requests

# url = "https://videoyukla.uz/instagram/media/service/"
# url = "https://videoyukla.uz/instagram/media/service/"

# payload = { "url": "https://www.instagram.com/reel/DIZD7JfiIKQ/?utm_source=ig_web_copy_link" }


# response = requests.post(url, json=payload)

# print(response.json())

# import requests

# url = "https://youtube-media-downloader.p.rapidapi.com/v2/misc/list-items"

# payload = {
    
# }
# headers = {
# 	"x-rapidapi-key": "54e518fa11msha164dc2cecb21c8p18d479jsn65ee0a8c6b70",
# 	"x-rapidapi-host": "youtube-media-downloader.p.rapidapi.com",
# 	"Content-Type": "application/x-www-form-urlencoded"
# }

# response = requests.post(url, data=payload, headers=headers)

# print(response.json())

# import yt_dlp


# def download_tiktok_video(url):
#     ydl_opts = {
#         'outtmpl': '%(title)s.%(ext)s',  # Fayl nomi video nomiga qarab bo'ladi
#         'format': 'best',  # Eng yaxshi sifatni tanlaydi
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=False)

#     print(f"Video yuklandi: {info}")


# # Misol uchun video URL
# tiktok_url = 'https://vt.tiktok.com/ZSrLJ2KnQ/'

# download_tiktok_video(tiktok_url)