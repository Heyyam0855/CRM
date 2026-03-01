# Git Əmrləri

## Repository: https://github.com/Heyyam0855/CRM.git

---

## Yeni Repository Başlatma

```bash
echo "# CRM" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Heyyam0855/CRM.git
git push -u origin main
```

---

## Mövcud Repository-ni Qoşma

```bash
git remote add origin https://github.com/Heyyam0855/CRM.git
git branch -M main
git push -u origin main
```

---

## Remote URL-ni Dəyişmə

```bash
git remote set-url origin https://github.com/Heyyam0855/CRM.git
git remote -v   # yoxla
```

---

## Gündəlik Push Qaydası

> Hər dəyişiklikdən sonra bu ardıcıllıqla push et:

```bash
# 1. Bütün dəyişiklikləri stage et
git add .

# 2. Commit mesajı yaz (Azərbaycan dilində)
#    Format: "<emoji> <nə edildi> (<fayl sayı> fayl) — dd.MM.yyyy HH:mm"
git commit -m "✅ Tapşırıq tamamlandı (3 fayl) — 01.03.2026 14:30"

# 3. GitHub-a push et
git push origin main
```

### Commit Emoji Seçim Cədvəli

| Dəyişən fayllar              | Emoji | Nümunə mesaj                           |
|------------------------------|-------|----------------------------------------|
| `models.py`                  | 🗃️   | Model strukturu yeniləndi              |
| `views.py`                   | 👁️   | View-lar yeniləndi                     |
| `services.py`                | 🔧    | Servis məntiqi yeniləndi              |
| `tasks.py`                   | ⚡    | Celery task-lar yeniləndi              |
| `tests/`, `test_*.py`        | 🧪    | Testlər əlavə edildi/yeniləndi         |
| `*.html` + `*.py`            | ✅    | Backend və frontend yeniləndi          |
| `*.html`                     | 🎨    | Template və UI yeniləndi               |
| `*.md`                       | 📝    | Sənədlər yeniləndi                     |
| `.json`, `.yaml`, `.env`     | ⚙️   | Konfiqurasiya yeniləndi                |
| Digər / qarışıq              | ✅    | Tapşırıq tamamlandı                   |

---

## Faydalı Əmrlər

```bash
# Status yoxla
git status

# Son commitləri gör
git log --oneline -10

# Dəyişiklikləri gör
git diff

# Yanlış add-ı geri al
git restore --staged <fayl>

# Son commiti düzəlt (push edilməmişsə)
git commit --amend -m "yeni mesaj"
```
