import { test, expect } from '@playwright/test';

const CHATBOT_URL = 'http://localhost:3000';

test.describe('Agentic UI Streaming & Orchestration Test', () => {

  test('User can book a bus route dynamically', async ({ page }) => {
    await page.goto(CHATBOT_URL);

    const chatInput = page.locator('#chat-input');
    const sendButton = page.locator('#send-button');
    const messageHistory = page.locator('.message-history');

    const userPrompt = "I need a bus from Hyderabad to Amalapuram tomorrow.";
    // Notice the backticks around this string!
    console.log(`\n[User] Sending prompt: "${userPrompt}"`);

    await chatInput.fill(userPrompt);
    await sendButton.click();

    console.log("[Test] Waiting for AI streaming to complete...");
    await page.waitForSelector('.streaming-done', { timeout: 15000 }); 

    const aiResponseLocator = messageHistory.locator('.ai-message').last();
    const actualAiText = await aiResponseLocator.innerText();
    
    // Notice the backticks here too!
    console.log(`\n[AI Response Captured]:\n"${actualAiText}"`);

    expect(actualAiText.toLowerCase()).toContain('amalapuram');
    expect(actualAiText.toLowerCase()).toContain('hyderabad');

    const asksForTime = actualAiText.toLowerCase().includes('time');
    const confirmsBooking = actualAiText.toLowerCase().includes('booked') || actualAiText.toLowerCase().includes('confirmed');
    
    expect(asksForTime || confirmsBooking).toBeTruthy();
  });

});