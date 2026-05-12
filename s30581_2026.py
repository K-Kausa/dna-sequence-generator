# Numer albumu: s30581
# Data: 12.05.2026
# Opis: Generator sekwencji DNA w formacie FASTA z dodatkowymi funkcjami.

import random

def generate_sequence(length: int) -> str:
    """Zwraca losową sekwencję DNA o zadanej długości."""
    return ''.join(random.choices(['A', 'C', 'G', 'T'], k=length))

def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.
    Klucze: "A", "C", "G", "T" (wartości % wystąpienia),
            "GC" (wartość % wystąpienia)."""
    seq_len = len(sequence)
    
    return {
        "A": (sequence.count('A') / seq_len) * 100,
        "C": (sequence.count('C') / seq_len) * 100,
        "G": (sequence.count('G') / seq_len) * 100,
        "T": (sequence.count('T') / seq_len) * 100,
        "GC": ((sequence.count('G') + sequence.count('C')) / seq_len) * 100
    }

def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię w losową pozycję sekwencji.
    Imię zapisane małymi literami."""
    if not name:
        return sequence
    pos = random.randint(0, len(sequence))
    return sequence[:pos] + name.lower() + sequence[pos:]

def format_fasta(seq_id: str, description: str, sequence: str) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    header = f">{seq_id} {description}".strip()
    lines = [header]
    line_width = 80
    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i+line_width])
    return "\n".join(lines)

def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu.
    W przypadku błędu powtarza pytanie."""
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")

def find_motif(sequence: str, motif: str) -> list[int]:
    """Wyszukuje motyw w sekwencji i zwraca listę pozycji (indeksowane od 1)."""
    positions = []
    start = 0
    while True:
        start = sequence.find(motif, start)
        if start == -1:
            break
        positions.append(start + 1)
        start += 1
    return positions

def get_complementary(sequence: str) -> str:
    """Zwraca nić komplementarną DNA."""
    mapping = str.maketrans('ACGT', 'TGCA')
    return sequence.translate(mapping)

def get_reverse_complementary(sequence: str) -> str:
    """Zwraca nić odwrotnie komplementarną DNA."""
    return get_complementary(sequence)[::-1]

def transcribe(sequence: str) -> str:
    """Transkrypcja in silico: zamiana DNA na mRNA (T -> U)."""
    return sequence.replace('T', 'U')

def translate(sequence: str) -> str:
    """Translacja sekwencji DNA na białko z użyciem standardowej tabeli kodonów."""
    codon_table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*', 'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
    }
    protein = []
    for i in range(0, len(sequence) - (len(sequence) % 3), 3):
        codon = sequence[i:i+3]
        protein.append(codon_table.get(codon, '?'))
    return "".join(protein)

def validate_motif(prompt: str) -> str:
    """Pobiera od użytkownika motyw DNA i waliduje jego poprawność."""
    valid_nucleotides = set("ACGT")
    while True:
        motif = input(prompt).strip().upper()
        
        if not motif:
            print("Błąd: Motyw nie może być pusty.")
            continue
            
        if set(motif).issubset(valid_nucleotides):
            return motif
            
        print("Błąd: Motyw może zawierać wyłącznie znaki A, C, G, T. Przykład: ATG")

def main():
    length = validate_positive_int("Podaj długość sekwencji: ")
    
    while True:
        seq_id = input("Podaj ID sekwencji: ")
        if " " not in seq_id and "\t" not in seq_id and len(seq_id) > 0:
            break
        print("Błąd: ID sekwencji nie może być puste ani zawierać białych znaków.")
        
    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")
    
    base_sequence = generate_sequence(length)
    stats = calculate_stats(base_sequence)
    
    final_sequence = insert_name(base_sequence, name)
    fasta_content = format_fasta(seq_id, description, final_sequence)
    
    motif = validate_motif("Podaj motyw do wyszukania (tylko A, C, G, T): ")
    motif_positions = find_motif(base_sequence, motif)
    
    comp_seq = get_complementary(base_sequence)
    rev_comp_seq = get_reverse_complementary(base_sequence)
    mrna_seq = transcribe(base_sequence)
    protein_seq = translate(base_sequence)
    
    fasta_content += "\n" + format_fasta(seq_id + "_comp", "Nici komplementarna", comp_seq)
    fasta_content += "\n" + format_fasta(seq_id + "_revcomp", "Nici odwrotnie komplementarna", rev_comp_seq)
    fasta_content += "\n" + format_fasta(seq_id + "_mRNA", "Transkrypt mRNA", mrna_seq)
    fasta_content += "\n" + format_fasta(seq_id + "_protein", "Sekwencja aminokwasowa", protein_seq)
    
    filename = f"{seq_id}.fasta"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(fasta_content)
        
    print(f"\nSekwencja zapisana do pliku: {filename}\n")
    print(f"Statystyki sekwencji (n={length}):")
    print(f"A: {stats['A']:.2f}%")
    print(f"C: {stats['C']:.2f}%")
    print(f"G: {stats['G']:.2f}%")
    print(f"T: {stats['T']:.2f}%")
    print(f"GC-content: {stats['GC']:.2f}%\n")
    
    print("--- Dodatkowe informacje ---")
    print(f"Znaleziono motyw '{motif}' na pozycjach: {motif_positions}")

if __name__ == "__main__":
    main()