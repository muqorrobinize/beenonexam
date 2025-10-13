import os
import json

# Konfigurasi
KUIS_FOLDER = 'kuis'
OUTPUT_HTML = 'index.html'

def generate_quiz_data():
    """Membaca folder kuis dan menghasilkan list of dictionary."""
    quiz_data = []
    print(f"Membaca folder '{KUIS_FOLDER}'...")

    if not os.path.isdir(KUIS_FOLDER):
        print(f"Error: Folder '{KUIS_FOLDER}' tidak ditemukan.")
        print("Silakan buat folder tersebut dan letakkan file-file kuis Anda di dalamnya.")
        # Buat folder jika belum ada agar skrip tidak gagal total
        os.makedirs(KUIS_FOLDER)
        print(f"Folder '{KUIS_FOLDER}' telah dibuat.")
        return []

    files = sorted(os.listdir(KUIS_FOLDER))
    
    for filename in files:
        if filename.endswith('.html'):
            parts = filename.replace('.html', '').split('_')
            if len(parts) >= 2:
                # Kategori adalah bagian pertama, Nama Kuis adalah sisanya
                category = parts[0]
                quiz_name = " ".join(parts[1:])
                
                # Membuat deskripsi otomatis dari nama kuis
                description = f"Kumpulan soal dan latihan untuk {quiz_name}."
                
                quiz_item = {
                    "filename": filename,
                    "description": description
                }
                quiz_data.append(quiz_item)
                print(f"  -> Menemukan kuis: {filename}")
            else:
                print(f"  -> Peringatan: Melewatkan file '{filename}' karena format nama tidak sesuai (KATEGORI_Nama Kuis.html)")

    return quiz_data

def update_html_file(quiz_data):
    """Memperbarui file index.html dengan data kuis yang baru."""
    try:
        with open(OUTPUT_HTML, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{OUTPUT_HTML}' tidak ditemukan. Pastikan file ini ada di folder yang sama dengan skrip.")
        return

    # Mengubah list python menjadi string format array JavaScript
    # indent=4 agar mudah dibaca jika ingin di-debug
    js_data_string = json.dumps(quiz_data, indent=4) 

    # Mencari baris yang perlu diganti
    target_line_start = '        const quizData = '
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        found = False
        for line in lines:
            # strip() untuk menghapus spasi di awal/akhir baris
            if line.strip().startswith(target_line_start.strip()):
                f.write(f"{target_line_start}{js_data_string};\n")
                found = True
            else:
                f.write(line)

    if found:
        print(f"\nBerhasil! File '{OUTPUT_HTML}' telah diperbarui dengan {len(quiz_data)} kuis.")
    else:
        print(f"\nError: Tidak dapat menemukan baris '{target_line_start}' di file '{OUTPUT_HTML}'.")
        print("Pastikan Anda menggunakan file index.html yang benar.")


if __name__ == "__main__":
    data = generate_quiz_data()
    if data:
        update_html_file(data)
    else:
        print("\nTidak ada data kuis yang valid untuk diproses.")
        # Tetap update HTML dengan array kosong jika tidak ada kuis
        update_html_file([])
