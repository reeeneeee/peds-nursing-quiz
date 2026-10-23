import re, json
SRC = [
 ("../nur774-exam2-practice/parts/01.md", "Eczema, Impetigo & Lyme", 1),
 ("../nur774-exam2-practice/parts/02.md", "Rashes & Exanthems", 1),
 ("../nur774-exam2-practice/parts/03.md", "Tinea (Fungal)", 1),
 ("../nur774-exam2-practice/parts/04.md", "Dermatitis, Varicella & Warts", 1),
 ("../nur774-exam2-practice/set2/parts/01.md", "Eczema, Impetigo & Lyme", 2),
 ("../nur774-exam2-practice/set2/parts/02.md", "Rashes & Exanthems", 2),
 ("../nur774-exam2-practice/set2/parts/03.md", "Tinea (Fungal)", 2),
 ("../nur774-exam2-practice/set2/parts/04.md", "Dermatitis, Varicella & Warts", 2),
 ("../nur774-exam2-practice/exam3/exam3_20Q.md", "Respiratory & Cardiac", 2),
 ("../nclex-fnp-derm-qbank/parts/01.md", "Tinea (Fungal)", 3),
 ("../nclex-fnp-derm-qbank/parts/02.md", "Dermatitis, Varicella & Warts", 3),
 ("../nclex-fnp-derm-qbank/parts/03.md", "Herpes & Shingles", 3),
 ("../nclex-fnp-derm-qbank/parts/04.md", "Dermatitis, Varicella & Warts", 3),
 ("../nclex-fnp-derm-qbank/parts/05.md", "Rashes & Exanthems", 3),
 ("../nclex-fnp-derm-qbank/parts/06.md", "Rashes & Exanthems", 3),
]
def clean(s): return re.sub(r'\*(?!\*)(.+?)\*', r'\1', s).strip()
bank=[]
for path, topic, level in SRC:
    txt=open(path).read()
    for b in re.split(r'\n\s*---\s*\n', txt):
        m=re.search(r'\*\*Q\d+\.\s*\[(SATA|Single)\]\*\*\s*(.+?)\n((?:[A-F]\.\s.*\n?)+)', b, re.S)
        a=re.search(r'\*\*Answer:\*\*\s*([A-F](?:\s*,\s*[A-F])*)', b)
        r=re.search(r'\*\*Rationale:\*\*\s*(.+)', b, re.S)
        if not (m and a and r): continue
        opts=[clean(l[3:]) for l in m.group(3).strip().split('\n') if re.match(r'^[A-F]\.\s',l)]
        ans=[ord(x.strip())-65 for x in a.group(1).split(',')]
        if max(ans)>=len(opts): continue
        bank.append({"t":topic,"l":level,"s":m.group(1)=="SATA","q":clean(m.group(2)),"o":opts,"a":ans,"r":clean(r.group(1).strip())})
json.dump(bank, open('bank.json','w'), separators=(',',':'))
from collections import Counter
print(len(bank), Counter(q['t'] for q in bank), Counter(q['l'] for q in bank))
