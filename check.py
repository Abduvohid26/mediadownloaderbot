import asyncio
import httpx

async def check(url, idx):
    print(f"📌 {idx + 1}-so‘rov yuborildi") 
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get("https://videoyukla.uz/youtube/media/", params={"yt_url": url}, timeout=25)
            result = response.json()
    except Exception as e:
        result = {"error": "Xatolik yuz berdi, qayta urunib ko‘ring", "details": str(e)}

    print(f"✅ {idx + 1}-javob tayyor")  
    return idx, result

async def main():
    # url = "https://www.instagram.com/stories/imperatoruz" stoires
    # url = "https://www.instagram.com/p/DH5gya1xo6H/?utm_source=ig_web_copy_link" one pic
    # url = "https://www.instagram.com/p/DHgWbewsTwH/?utm_source=ig_web_copy_link" # album and image
    url = "https://youtu.be/k26urW-idB8?si=k3LTr3x7Bj3RSHlC" # album images

    urls = [url] * 50  
    
    tasks = [asyncio.create_task(check(url, idx)) for idx, url in enumerate(urls)]  

    results = await asyncio.gather(*tasks)  

    for idx, result in sorted(results, key=lambda x: x[0]):
        print(f"🔍 Response {idx + 1}: {result}")

asyncio.run(main())
