# Chinese Simplification Patterns Frequency Analyzer

#### (Choose your language below / 請在下方選擇您的語言 /请在下方选择您的语言 )
[![English](https://img.shields.io/badge/Language-English-blue)](README.md)
[![繁體中文](https://img.shields.io/badge/Language-繁體中文-green)](README.zh-TW.md)
[![简体中文](https://img.shields.io/badge/Language-简体中文-red)](README.zh-CN.md)

A tool to rank the frequency of the transformation patterns between traditional and simplified character variants

The goal of this project is to reduce the learning burden for students who are learning both scripts or students of one script that want to transition from one script to another. By learning the most frequently occuring patterns first (e.g.  訁➔讠, 糹➔纟, 門➔门, 貝➔贝, 車➔车), students can minimize the time needed to gain a working proficiency with the less familiar variants. While this ranking may be primarily useful to foreign learners, it may also be useful to native speakers who want to learn to read/write the opposite script. Most non-technical learners will probably just be interested in the results of the analysis, which are contained in the link below.  

### [Download the most recent CSV rankings](https://github.com/moltencrux/rank-simp-freq/releases/download/latest/simp_rank.csv)

## **How It Works**

1. Loads simplification rules (two tables)  
2. Parses IDS decompositions (with recursive component extraction \+ CDP support)  
3. Uses OpenCC to verify which characters actually simplify  
4. Using component analysis, places characters into one or more categories that denote which simplification pattern(s) were applied in the transformation
5. Tallies the total frequency for each pattern
6. Ranks patterns by total frequency of affected characters  
7. Outputs JSON \+ ranked CSV with examples and cumulative coverage

## **Features**

- Parses IDS (Ideographic Description Sequences) for component decomposition  
- Supports both non-repeated (Table 1) and repeated/class-push (Table 2) simplifications  
- Uses OpenCC for accurate traditional → simplified conversion  
- Handles n:1 cases (e.g. 裏 / 裡 / 里 ➔ 里)  
- Supports CDP glyph references (`&CDP-XXXX;`)  
- Ranks patterns by real-world character frequency  
- Exports results as JSON + CSV (with cumulative frequency)

## **Project Structure**  

 Filename               | Description
------------------------|----------
├── `rank_simp.py`      | - Main script  
├── `simpT1.txt`        | - Non-repeated simplifications (simp first)  
├── `simpT2.txt`        | - Repeated / radical simplifications (simp first)  
├── `IDS-UCS-Basic.txt` | - Component data from CHISE  
├── `freq_trad.txt`     | - Traditional character frequency table  
├── `patterns.json`     | - Output: patterns ➔ characters    
└── `simp_rank.csv`     | - Human-readable ranked output


## **Installation**

```bash  
pip install opencc hanzidentifier
```

## **Usage**

```bash  
python rank_simp.py \  
  -s simpT1.txt \  
  -S simpT2.txt \  
  -i IDS-UCS-Basic.txt \  
  -f freq_trad.txt \  
  -o patterns.json \  
  -c simp_rank.csv
```

### **Input File Formats**

**Simplification Maps** (`simpT1.txt`, `simpT2.txt`):

```text  
车	車  
历	歷,曆  
监	監  
钅	金  
里	裏,裡
```

**Frequency Table** (tab-separated):

```text  
的	1234567  
一	987654  
```



## **Key Concepts**

* **Table 1**: One-off simplifications (usually not used as components)  
* **Table 2**: Radical / repeatable simplifications (e.g. 車 → 车, 金 → 钅)  
* **n:1 cases**: Multiple traditional characters map to the same simplified form (e.g. 裏/裡/里 → 里)  
* **CDP glyphs**: Special placeholders like `&CDP-8CC9;` are mapped to their proper radicals

## **Roadmap / Future Improvements**

* Position-aware matching (e.g. 金 → 钅 only on the left)  
* Better CDP mapping table  
* Better handling of variant characters

## **Data Sources**

* IDS decompositions: [CHISE IDS-UCS-Basic](https://github.com/chise/ids)  
* Official simplifications: [1986 简化字总表](https://zh.wikisource.org/wiki/%E7%AE%80%E5%8C%96%E5%AD%97%E6%80%BB%E8%A1%A8%EF%BC%881986%E5%B9%B4%E7%89%88%EF%BC%89)
* Frequency data: [字頻總表 - 教育部全球資訊網](https://language.moe.gov.tw/001/Upload/files/SITE_CONTENT/M0001/BIAU1.zip)

