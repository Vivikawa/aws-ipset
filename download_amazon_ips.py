import requests
import json
import subprocess
import sys
from datetime import datetime

def download_file(url, filename, binary=False):
    mode = 'wb' if binary else 'w'
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(filename, mode) as f:
            if binary:
                f.write(resp.content)
            else:
                f.write(resp.text)
        print(f"✅ Файл скачан: {filename}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при скачивании {url}: {e}")
        return False

def extract_amazon_json_ips(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return set(prefix['ip_prefix'] for prefix in data.get('prefixes', []) if 'ip_prefix' in prefix)

def extract_txt_ips(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Разделяем по пробелу или переводу строки
    return set(ip.strip() for ip in content.replace('\n', ' ').split() if ip.strip())

def main():
    # URLs
    amazon_json_url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    amazon_txt_url = "https://raw.githubusercontent.com/V3nilla/IPSets-For-Bypass-in-Russia/refs/heads/main/ipset-amazon.txt"
    cloudflare_txt_url = "https://raw.githubusercontent.com/V3nilla/IPSets-For-Bypass-in-Russia/refs/heads/main/ipset-cloudflare.txt"

    # Filenames
    amazon_json_file = "amazon_ip_ranges.json"
    amazon_txt_file = "ipset-amazon.txt"
    cloudflare_txt_file = "ipset-cloudflare.txt"
    output_file = "unique_ip_list.txt"

    # Download all files
    download_file(amazon_json_url, amazon_json_file)
    download_file(amazon_txt_url, amazon_txt_file)
    download_file(cloudflare_txt_url, cloudflare_txt_file)

    # Extract IPs
    ips_amazon_json = extract_amazon_json_ips(amazon_json_file)
    ips_amazon_txt = extract_txt_ips(amazon_txt_file)
    ips_cloudflare_txt = extract_txt_ips(cloudflare_txt_file)

    # Union all sets
    all_unique_ips = ips_amazon_json | ips_amazon_txt | ips_cloudflare_txt

    # Write to output file (one per line, no formatting)
    with open(output_file, 'w', encoding='utf-8') as f:
        for ip in sorted(all_unique_ips):
            f.write(f"{ip}\n")
    print(f"\n🎉 Итоговый файл с уникальными IP-диапазонами сохранён как: {output_file}")


def git_add_commit_push(file_path, commit_message="Update unique IP list"):
    try:
        # Добавляем файл в индекс
        subprocess.run(["git", "add", file_path], check=True)
        # Делаем коммит
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        # Пушим изменения
        subprocess.run(["git", "push"], check=True)
        print("✅ Файл успешно отправлен на GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при работе с git: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    # После генерации файла заливаем его на гит
    git_add_commit_push("unique_ip_list.txt", "Автоматическое обновление уникального списка IP-диапазонов")
    git_add_commit_push(".")
