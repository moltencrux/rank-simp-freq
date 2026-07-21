# **汉字简化模式优先学习工具 (Chinese Simplification Patterns Frequency Analyzer)**

#### (Choose your language below / 請在下方選擇您的語言 /请在下方选择您的语言 )
[![English](https://img.shields.io/badge/Language-English-blue)](README.md)
[![繁體中文](https://img.shields.io/badge/Language-繁體中文-green)](README.zh-TW.md)
[![简体中文](https://img.shields.io/badge/Language-简体中文-red)](README.zh-CN.md)

一个用于统计与排序繁简汉字转换规律（部件简化模式）出现频率的工具。

本专案旨在减轻同时学习繁简两种字体，或是想从其中一种字体过渡到另一种字体的学生的学习负担。透过优先学习出现频率最高的规律（例如：讠➔讠、纟➔纟、门➔门、贝➔贝、车➔车），学生可以花最少的时间，快速掌握较不熟悉的字体变体。虽然这个排名主要对外国学习者特别有帮助，但对于想要学习阅读或书写另一种字体的母语者来说，也同样具有参考价值。多数非技术学习者可能只对分析结果感兴趣，这些结果包含在下面的链接中。

### [下载最新版 CSV 频率排名表](https://github.com/moltencrux/rank-simp-freq/releases/download/latest/simp_rank.csv)

## **运作原理**

1. 载入简化规则（两张对照表）  
2. 解析 IDS 汉字结构拆解资料（支援递回部件提取与 CDP 字形）  
3. 使用 OpenCC 验证哪些汉字实际上发生了简化  
4. 透过部件分析，将汉字归类至一个或多个分类，用以标示该汉字在转换过程中套用了哪些简化规律  
5. 累加每个规律的总出现频率  
6. 根据受影响汉字的总频率对这些规律进行排序  
7. 输出 JSON 以及包含范例字和累计覆盖率的排序后 CSV 档案

## **功能特点**

* 解析 IDS（汉字结构描述序列，Ideographic Description Sequences）以进行部件拆解  
* 支援非类推简化（表一）与可类推/偏旁部首简化（表二）  
* 使用 OpenCC 进行精确的繁转简转换  
* 处理多对一的情况（例如：裏 / 裡 / 里 ➔ 里）  
* 支援 CDP 字形编码（`&CDP-XXXX;`）  
* 依据真实世界的字频对简化规律进行排序  
* 汇出结果为 JSON \+ CSV（含累计频率）

## **专案结构**

| 档案名称 | 说明 |
| :---- | :---- |
| ├── `rank_simp.py` | - 主程式脚本 |
| ├── `simpT1.txt` | - 非类推简化字表（简体在前） |
| ├── `simpT2.txt` | - 可类推 / 偏旁部首简化字表（简体在前） |
| ├── `IDS-UCS-Basic.txt` | - 来自 CHISE 的汉字部件资料 |
| ├── `freq_trad.txt` | - 繁体字字频表 |
| ├── `patterns.json` | - 输出档案：简化规律 ➔ 对应汉字 |
| └── `simp_rank.csv` | - 输出档案：便于阅读的排序结果 |

## **安装说明**

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

### **输入档案格式**

**简化对照表** (`simpT1.txt`, `simpT2.txt`):

```text  
车  車    
历  歷,曆    
监  監    
钅  金    
里  裏,裡
```

**字频表**（以 Tab 键分隔）：

```text  
的  1234567    
一  987654  
```

## **核心概念**

* **表一 (Table 1\)**：个别简化字（通常不作为偏旁部首类推使用）  
* **表二 (Table 2\)**：偏旁部首 / 可类推简化规则（例如：車 → 车、金 → 钅）  
* **多对一情况 (n:1 cases)**：多个繁体字对应到同一个简体字（例如：裏/裡/里 → 里）  
* **CDP 字形**：将如 \&CDP-8CC9; 等特殊预留代码映射到其对应的正确偏旁部首

## **开发蓝图 / 未来改进**

* 位置感知比对（例如：金 → 钅 仅在左侧偏旁时成立）  
* 更完善的 CDP 映射表  
* 更妥善地处理异体字
* 找出相似的一次性简化模式组合（例如：構➔构、購➔购、溝➔沟），以进一步减轻学习负担。

## **数据来源**

* IDS 结构拆解：[CHISE IDS-UCS-Basic](https://github.com/chise/ids)  
* 官方简化字规范：[1986 简化字总表](https://zh.wikisource.org/wiki/%E7%AE%80%E5%8C%96%E5%AD%97%E6%80%BB%E8%A1%A8%EF%BC%881986%E5%B9%B4%E7%89%88%EF%BC%89)  
* 字频数据：[字频总表 \- 中华民国教育部全球资讯网](https://language.moe.gov.tw/001/Upload/files/SITE_CONTENT/M0001/BIAU1.zip)

