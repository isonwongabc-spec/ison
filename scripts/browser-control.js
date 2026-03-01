const { chromium } = require('playwright');

(async () => {
  const args = process.argv.slice(2);
  const url = args[0] || 'https://www.youtube.com';
  
  try {
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle' });
    
    console.log(`✅ 已打开: ${url}`);
    console.log(`📄 标题: ${await page.title()}`);
    
    // 保持浏览器打开
    // await browser.close();
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
})();
