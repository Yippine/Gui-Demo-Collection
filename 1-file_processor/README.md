# File Processor 2.0

File Processor 2.0 是一個強大的文件處理工具,可以幫助開發者快速瀏覽和處理項目中的文件。它支持多種程式語言,並提供了直觀的圖形用戶界面。

## 功能特點

- 支持多種主流程式語言
- 可自定義排除目錄和文件
- 可自定義包含文件
- 直觀的圖形用戶界面
- 實時處理和顯示結果
- 支持正則表達式匹配

## 安裝

1. 克隆此倉庫:
   ```
   git clone https://github.com/yourusername/file-processor-2.0.git
   ```

2. 進入項目目錄:
   ```
   cd file-processor-2.0
   ```

3. 創建並激活虛擬環境:
   ```
   python -m venv venv
   source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
   ```

4. 安裝依賴:
   ```
   pip install -r requirements.txt
   ```

5. 安裝項目:
   ```
   pip install -e .
   ```

## 使用方法

1. 運行主程序:
   ```
   python src/main.py
   ```

2. 在圖形界面中:
   - 選擇項目目錄
   - 選擇程式語言
   - 自定義排除目錄和文件(可選)
   - 自定義包含文件(可選)
   - 點擊"讀取目錄"或"讀取程式"按鈕

3. 查看處理結果和日誌

## 貢獻

歡迎提交 Pull Requests 來改進這個項目。對於重大更改,請先開 issue 討論您想要改變的內容。

## 許可證

[MIT](https://choosealicense.com/licenses/mit/)