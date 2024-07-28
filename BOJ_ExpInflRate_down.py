from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.stat-search.boj.or.jp/ssi/cgi-bin/famecgi2?cgi=$nme_s050")
    page.get_by_label("\n\t\t\t\t\t\t\tデータコードを入力してください(複数入力可)\n\t\t\t\t\t\t").fill("CO'TK99F0000206HCQ00000\nCO'TK99F2011206HCQ00000\nCO'TK99F2019206HCQ00000\nCO'TK99F2012206HCQ00000\nCO'TK99F2081206HCQ00000")
    page.get_by_role("button", name="検索").click()
    page.get_by_text("全てのデータ系列を選択する").first.click()
    page.get_by_text("抽出条件に追加", exact=True).click()
    with page.expect_popup() as page1_info:
        page.get_by_text("抽出", exact=True).click()

    page1 = page1_info.value
    with page1.expect_popup() as page2_info:
        page1.get_by_text("ダウンロード", exact=True).click()

    page2 = page2_info.value
    with page2.expect_download() as download_info:
        page2.locator('td > a').click()
    download = download_info.value
    # Save downloaded file in current directory under name "BOJ_ExpInflRate_down.csv"
    download.save_as("./BOJ_ExpInflRate_down.csv")

    page2.close()
    page1.close()
    page.close()
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

