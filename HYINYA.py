import json

# Чтение JSON-файла
with open('ip-ranges.json', 'r') as f:
    data = json.load(f)

# Извлечение всех ip_prefix и сохранение в текстовый файл
with open('ip_prefixes1.txt', 'w') as f:
    for item in data['prefixes']:
        f.write(item['ip_prefix'] + '\n')  # Каждый IP с новой строки

print("Готово! Результат сохранён в ip_prefixes.txt")