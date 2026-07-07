from playwright.sync_api import Playwright, sync_playwright, expect
import codecs
import pandas as pd

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
    file_path = "./BOJ_ExpInflRate_down.csv"
    download.save_as(file_path)

    # 2. PandasでDataFrameに読み込み（Shift_JISを指定）
    # ※日銀短観のCSVは上部に英語・日本語のタイトル行があるため、必要に応じて skiprows を調整してください
    df = pd.read_csv(file_path, encoding='cp932', skiprows=1)

    # 3. DataFrameの編集
    # 実際のCSV構造に合わせて変更してください
    df = df.rename(columns={
    '物価全般の見通し/５年後/企業の物価見通しの平均/全規模/全産業': '全規模/全産業',
    '物価全般の見通し/５年後/企業の物価見通しの平均/全規模/_建設': '全規模/建設',
    '物価全般の見通し/５年後/企業の物価見通しの平均/全規模/_不動産・物品賃貸': '全規模/不動産・物品賃貸',
    '物価全般の見通し/５年後/企業の物価見通しの平均/全規模/__不動産': '全規模/不動産',
    '物価全般の見通し/５年後/企業の物価見通しの平均/全規模/_対事業所サービス': '全規模/対事業所サービス'
    })

    df['系列名称'] = pd.to_datetime(df['系列名称'], format='%Y/%m').dt.strftime('%Y年%m月')

    num = len(df['全規模/全産業'].dropna())
    df = df.iloc(num-1)
    
    # 4. UTF-8に変換して新しいファイルに保存
    output_path = "./BOJ_ExpInflRate_utf8.csv"
    df.to_csv(output_path, index=False, encoding='utf-8')

    page2.close()
    page1.close()
    page.close()
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

