from playwright.async_api import async_playwright


async def download_prod_img(downloads_folder: str, product_name: str, prod_id: str):
    async with async_playwright() as p:

        browser = await p.firefox.launch_persistent_context(
            './img_inserter/playwright',
            headless=False
        )
        
        page = await browser.new_page()
        await page.goto('https://www.google.com.br/imghp?hl=pt-BR&authuser=0&ogbl')
        await page.wait_for_selector('#APjFqb')
        search_input = page.locator('#APjFqb')
        await search_input.type(product_name)
        await page.wait_for_selector('[jsname="Tg7LZd"]')
        await page.click('[jsname="Tg7LZd"]')
        await page.wait_for_selector('[jsname="Q4LuWd"]')
        img_element = page.locator('[jsname="Q4LuWd"]').first
        screenshot_data = await img_element.screenshot()
        
        with open(f'{downloads_folder}/{prod_id}.png', 'wb') as f:
            f.write(screenshot_data)


