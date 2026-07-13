#!/usr/bin/env python3
import re
import json
import argparse
from collections import defaultdict, deque
import sys
from pathlib import Path
from typing import Set, Dict
import csv
import opencc
import hanzidentifier

IDS_OPERATORS = set((*'⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻\t', '@apparent='))

cdp_mapping = {
    '&CDP-8CC9;': '𰯲',
}

T2_EXCEPTIONS = {
    '言', '金', '睪' '糸'
}

def extract_all_components(char: str, char_to_ids: dict) -> Set[str]:

    components = set()

    queue = deque(char_to_ids.get(char, set()))

    # DFS to search for all subcomponents
    while queue:
        cur = queue.popleft()
        components.add(cur)
        sub = char_to_ids.get(cur, set()) - components
        queue.extend(sub)

    return components


def load_simpl_map(file_path: Path) -> Dict[str, str]:
    """trad_comp -> simp_comp (supports multiple trad per line)"""
    simpl_map: Dict[str, str] = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Example line formats we now support:
            # 车    車
            # 历    歷曆
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                simp = parts[0]
                trad_str = parts[1]
                for trad in re.split(r'[,，]', trad_str):
                    trad = trad.strip()
                    if trad:
                        simpl_map[trad] = simp
    print(f"Loaded {len(simpl_map)} simplification mappings from {file_path}")
    return simpl_map

def parse_ids(file_path: Path) -> Dict[str, Set(str)]:
    char_to_ids = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        ids_pat = re.compile(r'&[\w\-\+]+;|@apparent=|\t|.')

        for line in f:
            line = line.strip()
            if not line or line.startswith(';;'):
                continue

            parts = line.split('\t', maxsplit=2)
            if len(parts) >= 3:
                char = parts[1]
                ids_parts = set()

                for t in set(ids_pat.findall(parts[2])) - IDS_OPERATORS:
                    if t in cdp_mapping:
                        ids_parts.add(cdp_mapping[t])
                    else:
                        ids_parts.add(t)

                char_to_ids[char] = ids_parts
    print(f"Loaded {len(char_to_ids)} characters")
    return char_to_ids

def load_freq_table(file_path: Path) -> Dict[str, int]:
    freq_table = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            char, freq = line.split('\t')
            freq = int(freq)
            freq_table[char] = freq

    return freq_table


def write_csv_data(file_path: Path, freq_table, pattern_dict, trad_map):

    total_freq = {}
    for simpl, chars in pattern_dict.items():

        total_freq[simpl] = sum(freq_table.get(t, 0) for t, s in chars)

    total_freq = dict(sorted(total_freq.items(), key=lambda x: x[1], reverse=True))

    total_count = sum(total_freq.values())

    # pattern_dict[k] ... /was sorted_patterns.. applicble chrrs

    # trad_map : inv map of the simplifications: yes...
    # sorted patterns s: [ applicble chars(t, s)]
    # freq_table trad_char: frequency
    # sorted keys.. all simp part of patterns (sorted by freq of the pattern.. but)
    # total_freq...

    cum_freq = 0
    data = []

    for k in sorted(total_freq, key=lambda k: total_freq[k], reverse=True):

        # Get the first example T/S pair that is not exactly the pattenr itself
        # or none if none exist
        example = next(iter(c for c in pattern_dict[k] if not {*trad_map[k]} & {*c[0]} ), ())
        example = '➔'.join(example)

        data.append(
            {
                "Traditional Key": "".join(trad_map[k]),
                "Simplified Key": k,
                "Example": example,
                "Frequency": total_freq[k],
                "Cumulative Frequency": (cum_freq := cum_freq + total_freq[k]),
                "Cumulative %" : 100 * cum_freq / total_count,
            }
        )

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        # Python dicts maintain insertion order
        fieldnames = data[0].keys()

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    parser = argparse.ArgumentParser(description="Chinese simplification patterns with self-pattern support.")
    parser.add_argument('-s', '--simp-t1-map', required=True, type=Path, help="Simplification table 1 (non-repeated tranformations) map file")
    parser.add_argument('-S', '--simp-t2-map', required=True, type=Path, help="Simplification table 2 (repeated transformations) map file")
    parser.add_argument('-i', '--ids', required=True, type=Path, help="IDS-UCS-Basic.txt")
    parser.add_argument('-f', '--freq', required=True, type=Path, help="Frequency table")
    parser.add_argument('-o', '--output', default='simplification_patterns.json', type=Path)
    parser.add_argument('-c', '--csv-output', type=Path)
    args = parser.parse_args()

    freq_table = load_freq_table(args.freq)

    if not args.simp_t1_map.exists():
        print("Error: Simplification Table 1 not found.", file=sys.stderr)
        sys.exit(1)
    elif not args.simp_t2_map.exists():
        print("Error: Simplification Table 2 not found.", file=sys.stderr)
        sys.exit(1)
    elif not args.ids.exists():
        print("Error: IDS file not found.", file=sys.stderr)
        sys.exit(1)

    simp_t1_map = load_simpl_map(args.simp_t1_map)
    simp_t2_map = load_simpl_map(args.simp_t2_map)

    # Make a reverse map of the simplifciations
    trad_map = defaultdict(list)
    for k, v in simp_t1_map.items():
        trad_map[v].append(k)
    for k, v in simp_t2_map.items():
        trad_map[v].append(k)

    char_to_ids = parse_ids(args.ids)

    pattern_dict = defaultdict(list)
    validated_count = 0
    simplifying_chars = 0

    for trad_char in char_to_ids:
        # Filter to likely traditional characters
        if hanzidentifier:
            ident = hanzidentifier.identify(trad_char)
            if ident == hanzidentifier.SIMPLIFIED:
                continue


        simp_char = t2s.convert(trad_char) if t2s else trad_char
        if simp_char == trad_char and trad_char not in simp_t1_map and trad_char not in simp_t2_map:
            continue

        simp_ids_comps  = char_to_ids.get(simp_char, set())
        simplifying_chars += 1
        all_trad_comps = extract_all_components(trad_char, char_to_ids)
        all_simp_comps = extract_all_components(simp_char, char_to_ids)

        if trad_char in simp_t1_map:
            pattern_dict[simp_t1_map[trad_char]].append((trad_char, simp_char))
            validated_count += 1

        for trad_comp, simp_comp in simp_t2_map.items():
            # For repeated transformations, we must also compare the components
            # Improved condition for n:1 cases like 里
            if (trad_comp in all_trad_comps) or (trad_comp == trad_char and trad_char not in T2_EXCEPTIONS):
                # Extra check: the simplified form should contain the simplified component
                if (simp_comp in all_simp_comps) or (simp_comp == simp_char) or (trad_comp == trad_char):
                    pattern_dict[simp_comp].append((trad_char, simp_char))
                    validated_count += 1

    # Deduplicate lists
    # for k in pattern_dict:
    #     pattern_dict[k] = sorted(set(pattern_dict[k]))
    pattern_dict = {k: sorted(dict(v).items(), key=lambda x: freq_table.get(x[0], 0), reverse=True) for k, v in pattern_dict.items()}

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(pattern_dict, f, ensure_ascii=False, indent=2)

    # Summary
    sorted_patterns = sorted(pattern_dict.items(), key=lambda x: len(x[1]), reverse=True)
    print(f"\nFound {simplifying_chars} simplifying characters.")
    print(f"Generated {len(pattern_dict)} patterns ({validated_count} associations).")
    print("\nTop 20 patterns:")

    # for simpl, chars in sorted_patterns:
    #     print(f"  {simpl}: {len(chars)} characters (e.g. {', '.join(chars[:10])}...)")

    print(f"Found {simplifying_chars} characters that actually simplify.")

    if 'csv_output' in args:
        write_csv_data(args.csv_output, freq_table, pattern_dict, trad_map)

if __name__ == "__main__":
    main()
