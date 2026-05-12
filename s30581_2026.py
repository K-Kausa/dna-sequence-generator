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
    
if __name__ == "__main__":
    main()