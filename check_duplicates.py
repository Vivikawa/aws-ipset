def compare_files(file1_path, file2_path, output_file="output.txt"):
    # Читаем содержимое файлов с сохранением номеров строк
    lines1_dict = {}
    lines2_dict = {}
    
    with open(file1_path, 'r', encoding='utf-8') as f1:
        for line_num, line in enumerate(f1, 1):
            line = line.strip()
            if line:  # Пропускаем пустые строки
                if line not in lines1_dict:
                    lines1_dict[line] = []
                lines1_dict[line].append(line_num)
    
    with open(file2_path, 'r', encoding='utf-8') as f2:
        for line_num, line in enumerate(f2, 1):
            line = line.strip()
            if line:  # Пропускаем пустые строки
                if line not in lines2_dict:
                    lines2_dict[line] = []
                lines2_dict[line].append(line_num)
    
    # Находим различия
    lines1_set = set(lines1_dict.keys())
    lines2_set = set(lines2_dict.keys())
    
    only_in_file1 = lines1_set - lines2_set
    only_in_file2 = lines2_set - lines1_set
    common_lines = lines1_set & lines2_set
    
    # Записываем результаты в файл
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("=" * 60 + "\n")
        output.write("СРАВНЕНИЕ ФАЙЛОВ\n")
        output.write("=" * 60 + "\n")
        output.write(f"📁 Файл 1: {file1_path}\n")
        output.write(f"📁 Файл 2: {file2_path}\n")
        output.write("-" * 60 + "\n")
        output.write(f"📊 СТАТИСТИКА:\n")
        output.write(f"   • Общих строк: {len(common_lines)}\n")
        output.write(f"   • Только в файле 1: {len(only_in_file1)}\n")
        output.write(f"   • Только в файле 2: {len(only_in_file2)}\n")
        output.write(f"   • Всего уникальных строк в файле 1: {len(lines1_set)}\n")
        output.write(f"   • Всего уникальных строк в файле 2: {len(lines2_set)}\n")
        output.write("-" * 60 + "\n")
        
        # Показываем строки только в первом файле
        if only_in_file1:
            output.write(f"\n🔍 СТРОКИ ТОЛЬКО В {file1_path}:\n")
            output.write("-" * 40 + "\n")
            for line in sorted(only_in_file1):
                line_numbers = lines1_dict[line]
                output.write(f"'{line}' (строки: {', '.join(map(str, line_numbers))})\n")
        
        # Показываем строки только во втором файле
        if only_in_file2:
            output.write(f"\n🔍 СТРОКИ ТОЛЬКО В {file2_path}:\n")
            output.write("-" * 40 + "\n")
            for line in sorted(only_in_file2):
                line_numbers = lines2_dict[line]
                output.write(f"'{line}' (строки: {', '.join(map(str, line_numbers))})\n")
        
        # Показываем общие строки с номерами строк
        if common_lines:
            output.write(f"\n✅ ОБЩИЕ СТРОКИ:\n")
            output.write("-" * 40 + "\n")
            for line in sorted(common_lines):
                line1_nums = lines1_dict[line]
                line2_nums = lines2_dict[line]
                output.write(f"'{line}'\n")
                output.write(f"  → В {file1_path}: строки {', '.join(map(str, line1_nums))}\n")
                output.write(f"  → В {file2_path}: строки {', '.join(map(str, line2_nums))}\n")
                output.write("\n")
        
        output.write("=" * 60 + "\n")
    
    print(f"✅ Результаты сравнения сохранены в файл: {output_file}")

if __name__ == "__main__":
    # Замените на пути к вашим файлам
    file1 = "ipset-amazon.txt"
    file2 = "другой_файл.txt"  # Укажите путь ко второму файлу
    
    try:
        compare_files(file1, file2)
    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")