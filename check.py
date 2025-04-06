import asyncio
import httpx

async def check(url, idx):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://videoyukla.uz/checker/", params={"url": url}, timeout=25)
            print(response, "Response")
            return idx, response.json()  # Index bilan javobni qaytaramiz
    except Exception as e:
        return idx, {"error": "Xatolik yuz berdi, qayta urunib ko‘ring", "details": str(e)}

async def main():
    url = "https://www.instagram.com/p/DIGz6HRz7Ur/?utm_source=ig_web_copy_link"  # Test uchun URL
    urls = [url] * 2  # 50 ta bir xil so‘rov
    
    tasks = []
    results = []

    # So'rovlarni ketma-ket yuborish
    for idx, url in enumerate(urls):
        task = asyncio.create_task(check(url, idx))  # Har bir so'rovni yaratamiz
        tasks.append(task)

    for task in tasks:
        idx, result = await task  # Har bir taskni kutib, javobni olish
        results.append((idx, result))  # Index va javobni saqlaymiz

    # Javoblar ketma-ket chiqariladi
    for idx, result in sorted(results, key=lambda x: x[0]):
        print(f"Response {idx + 1}: {result}")

# Asinxron kodni ishga tushiramiz
asyncio.run(main())
