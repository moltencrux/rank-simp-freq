# **漢字簡化模式優先學習工具 (Chinese Simplification Patterns Frequency Analyzer)**

#### (Choose your language below / 請在下方選擇您的語言 /请在下方选择您的语言 )
[![English](https://img.shields.io/badge/Language-English-blue)](README.md)
[![繁體中文](https://img.shields.io/badge/Language-繁體中文-green)](README.zh-TW.md)
[![简体中文](https://img.shields.io/badge/Language-简体中文-red)](README.zh-CN.md)

一個用於統計與排序繁簡漢字轉換規律（部件簡化模式）出現頻率的工具。

本專案旨在減輕同時學習繁簡兩種字體，或是想從其中一種字體過渡到另一種字體的學生的學習負擔。透過優先學習出現頻率最高的規律（例如：訁➔讠、糹➔纟、門➔门、貝➔贝、車➔车），學生可以花最少的時間，快速掌握較不熟悉的字體變體。雖然這個排名主要對外國學習者特別有幫助，但對於想要學習閱讀或書寫另一種字體的母語者來說，也同樣具有參考價值。大多數非技術學習者可能只對分析結果感興趣，這些結果包含在下面的鏈接中。

### [下載最新版 CSV 頻率排名表](https://github.com/moltencrux/rank-simp-freq/releases/download/latest/simp_rank.csv)

## **運作原理**

1. 載入簡化規則（兩張對照表）  
2. 解析 IDS 漢字結構拆解資料（支援遞迴部件提取與 CDP 字形）  
3. 使用 OpenCC 驗證哪些漢字實際上發生了簡化  
4. 透過部件分析，將漢字歸類至一個或多個分類，用以標示該漢字在轉換過程中套用了哪些簡化規律  
5. 累加每個規律的總出現頻率  
6. 根據受影響漢字的總頻率對這些規律進行排序  
7. 輸出 JSON 以及包含範例字和累計覆蓋率的排序後 CSV 檔案

## **功能特點**

* 解析 IDS（漢字結構描述序列，Ideographic Description Sequences）以進行部件拆解  
* 支援非類推簡化（表一）與可類推/偏旁部首簡化（表二）  
* 使用 OpenCC 進行精確的繁轉簡轉換  
* 處理多對一的情況（例如：裏 / 裡 / 里 ➔ 里）  
* 支援 CDP 字形編碼（`&CDP-XXXX;`）  
* 依據真實世界的字頻對簡化規律進行排序  
* 匯出結果為 JSON \+ CSV（含累計頻率）

## **專案結構**

| 檔案名稱 | 說明 |
| :---- | :---- |
| ├── `rank_simp.py` | - 主程式腳本 |
| ├── `simpT1.txt` | - 非類推簡化字表（簡體在前） |
| ├── `simpT2.txt` | - 可類推 / 偏旁部首簡化字表（簡體在前） |
| ├── `IDS-UCS-Basic.txt` | - 來自 CHISE 的漢字部件資料 |
| ├── `freq_trad.txt` | - 繁體字字頻表 |
| ├── `patterns.json` | - 輸出檔案：簡化規律 ➔ 對應漢字 |
| └── `simp_rank.csv` | - 輸出檔案：便於閱讀的排序結果 |

## **安裝說明**

```bash  
pip install opencc hanzidentifier
```

## **使用方法**

```bash  
python rank_simp.py \    
  -s simpT1.txt \    
  -S simpT2.txt \    
  -i IDS-UCS-Basic.txt \    
  -f freq_trad.txt \    
  -o patterns.json \    
  -c simp_rank.csv
```

### **輸入檔案格式**

**簡化對照表** (`simpT1.txt`, `simpT2.txt`):

```text  
车  車    
历  歷,曆    
监  監    
钅  金    
里  裏,裡
```

**字頻表**（以 Tab 鍵分隔）：

```text  
的  1234567    
一  987654  
```

## **核心概念**

* **表一 (Table 1\)**：個別簡化字（通常不作為偏旁部首類推使用）  
* **表二 (Table 2\)**：偏旁部首 / 可類推簡化規則（例如：車 → 车、金 → 钅）  
* **多對一情況 (n:1 cases)**：多個繁體字對應到同一個簡體字（例如：裏/裡/里 → 里）  
* **CDP 字形**：將如 \&CDP-8CC9; 等特殊預留代碼映射到其對應的正確偏旁部首

## **開發藍圖 / 未來改進**

* 位置感知比對（例如：金 → 钅 僅在左側偏旁時成立）  
* 更完善的 CDP 映射表  
* 更妥善地處理異體字

## **數據來源**

* IDS 結構拆解：[CHISE IDS-UCS-Basic](https://github.com/chise/ids)  
* 官方簡化字規範：[1986 簡化字總表](https://zh.wikisource.org/wiki/%E7%AE%80%E5%8C%96%E5%AD%97%E6%80%BB%E8%A1%A8%EF%BC%881986%E5%B9%B4%E7%89%88%EF%BC%89)  
* 字頻數據：[字頻總表 \- 中華民國教育部全球資訊網](https://language.moe.gov.tw/001/Upload/files/SITE_CONTENT/M0001/BIAU1.zip)

