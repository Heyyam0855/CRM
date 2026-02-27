# ============================================================
#  LMS — Auto Commit & Push Hook
#  Claude Sonnet 4.6 | Hər tapşırıq bitdikdən sonra işə düşür
# ============================================================

Set-Location "C:\Users\Samir\Desktop\Project"

# 1. Dəyişiklik varmı yoxla
$untracked = git ls-files --others --exclude-standard
$modified  = git diff --name-only
$staged    = git diff --cached --name-only

if (-not ($untracked -or $modified -or $staged)) {
    Write-Host "[Auto-commit] Heç bir dəyişiklik yoxdur, keç." -ForegroundColor Yellow
    exit 0
}

# 2. Hamısını stage et
git add .

# 3. Dəyişən faylların siyahısını al
$changed = git diff --cached --name-only
$count   = ($changed | Measure-Object).Count
$date    = Get-Date -Format "dd.MM.yyyy HH:mm"

# 4. Fayl tipinə görə Azərbaycanca commit mesajı yaz
$pyFiles  = $changed | Where-Object { $_ -match "\.py$" }
$htmlFiles= $changed | Where-Object { $_ -match "\.html$" }
$mdFiles  = $changed | Where-Object { $_ -match "\.md$" }
$jsFiles  = $changed | Where-Object { $_ -match "\.(js|ts|css)$" }
$cfgFiles = $changed | Where-Object { $_ -match "\.(json|yaml|yml|toml|env|cfg|ini)$" }

if ($pyFiles -and $htmlFiles) {
    $msg = "✅ Backend və frontend yeniləndi ($count fayl) — $date"
} elseif ($pyFiles) {
    # Model, view, service, task fərqləndir
    $models   = $pyFiles | Where-Object { $_ -match "model" }
    $views    = $pyFiles | Where-Object { $_ -match "view" }
    $services = $pyFiles | Where-Object { $_ -match "service" }
    $tasks    = $pyFiles | Where-Object { $_ -match "task" }
    $tests    = $pyFiles | Where-Object { $_ -match "test" }

    if ($models)   { $msg = "🗃️ Model strukturu yeniləndi ($count fayl) — $date" }
    elseif ($views)    { $msg = "👁️ View-lar yeniləndi ($count fayl) — $date" }
    elseif ($services) { $msg = "🔧 Servis məntiqi yeniləndi ($count fayl) — $date" }
    elseif ($tasks)    { $msg = "⚡ Celery task-lar yeniləndi ($count fayl) — $date" }
    elseif ($tests)    { $msg = "🧪 Testlər əlavə edildi/yeniləndi ($count fayl) — $date" }
    else               { $msg = "🐍 Python kodu yeniləndi ($count fayl) — $date" }

} elseif ($htmlFiles) {
    $msg = "🎨 Template və UI yeniləndi ($count fayl) — $date"
} elseif ($mdFiles) {
    $msg = "📝 Sənədlər yeniləndi ($count fayl) — $date"
} elseif ($jsFiles) {
    $msg = "💻 Frontend (JS/CSS) yeniləndi ($count fayl) — $date"
} elseif ($cfgFiles) {
    $msg = "⚙️ Konfiqurasiya yeniləndi ($count fayl) — $date"
} else {
    $msg = "✅ Tapşırıq tamamlandı ($count fayl) — $date"
}

# 5. Commit et
git commit -m $msg
if ($LASTEXITCODE -ne 0) {
    Write-Host "[Auto-commit] Commit uğursuz oldu." -ForegroundColor Red
    exit 1
}

# 6. Push et
git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "[Auto-commit] Push uğursuz oldu." -ForegroundColor Red
    exit 1
}

Write-Host "[Auto-commit] ✅ Uğurla commit edildi: $msg" -ForegroundColor Green
