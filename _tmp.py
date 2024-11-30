# Funkcja przetwarzająca plik
def process_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                # Podział linii na części
                parts = line.split()
                
                # Sprawdzenie, czy linia ma odpowiednią strukturę
                if len(parts) != 4:
                    print(f"Pominięto linię: {line.strip()} (niepoprawny format)")
                    continue
                
                try:
                    # Parsowanie wartości
                    first = int(parts[0])
                    second = int(parts[1])
                    third = parts[2]
                    fourth = int(parts[3])
                    
                    # Dodanie 65 do drugiej wartości
                    second += 65
                    
                    # Zapisanie zmodyfikowanej linii do pliku wyjściowego
                    outfile.write(f"{first} {second} {third} {fourth}\n")
                except ValueError:
                    print(f"Pominięto linię: {line.strip()} (nieprawidłowe wartości)")
    except FileNotFoundError:
        print(f"Plik {input_file} nie został znaleziony.")

# Ścieżki do plików
input_file = "city.data.txt"
output_file = "city.datafix.txt"

# Wywołanie funkcji
process_file(input_file, output_file)
