const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  // 打开 YouTube 搜索
  await page.goto('https://www.youtube.com/results?search_query=%E8%A1%97%E7%81%AF%E6%99%9A%E9%A4%90+%E8%A1%9B%E8%98%AD', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  
  // 点击第一个视频
  try {
    const video = page.locator('ytd-video-renderer a#thumbnail, ytd-video-renderer a[href*="/watch"]').first();
    await video.click();
    console.log('已点击第一个视频');
  } catch (e) {
    // 备选方案
    const video = page.locator('ytd-video-renderer').first().locator('a').first();
    await video.click();
    console.log('已点击第一个视频(备选)');
  }
  
  await page.waitForTimeout(3000);
  
  // 按 F 键进入全屏
  await page.keyboard.press('f');
  console.log('✅ YouTube 已全屏播放');
})();
