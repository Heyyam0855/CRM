# Windows Command Prompt (CMD) — Əsas Komandalar

> Windows Command Prompt (cmd.exe) terminalında istifadə olunan ən vacib və tez-tez istifadə edilən komandaların kateqoriyalara görə siyahısı.

---

## 1. Fayl və Qovluq Əməliyyatları

| Komanda | İzah |
|---------|------|
| `dir` | Qovluqdakı fayl və alt qovluqların siyahısını göstərir |
| `cd` / `chdir` | Cari qovluğu dəyişir (başqa qovluğa keçid) |
| `md` / `mkdir` | Yeni qovluq yaradır |
| `rd` / `rmdir` | Qovluğu silir |
| `copy` | Bir və ya bir neçə faylı başqa yerə kopyalayır |
| `xcopy` | Fayl və qovluqları genişləndirilmiş seçimlərlə kopyalayır |
| `robocopy` | Güclü fayl/qovluq kopyalama aləti (etibarlı kopyalama) |
| `move` | Faylları bir qovluqdan digərinə köçürür |
| `del` / `erase` | Bir və ya bir neçə faylı silir |
| `ren` / `rename` | Faylın və ya qovluğun adını dəyişir |
| `type` | Mətn faylının məzmununu ekranda göstərir |
| `tree` | Qovluq strukturunu qrafik şəkildə göstərir |
| `attrib` | Fayl atributlarını göstərir və ya dəyişir (gizli, yalnız oxuma və s.) |
| `mklink` | Simvolik link (symbolic link) yaradır |
| `replace` | Faylları yeniləyir və ya əvəz edir |

---

## 2. Şəbəkə Komandaları

| Komanda | İzah |
|---------|------|
| `ping` | Şəbəkə bağlantısını yoxlayır (paket göndərir) |
| `ipconfig` | IP ünvanı, subnet mask, default gateway və DNS məlumatlarını göstərir |
| `netstat` | Aktiv şəbəkə bağlantılarını, portları və statistikanı göstərir |
| `nslookup` | DNS sorğusu edir — domen adını IP-yə çevirir |
| `tracert` | Paketlərin uzaq hosta gedən marşrutunu izləyir |
| `pathping` | Tracert + ping birləşməsi — paket itkisi və gecikmə göstərir |
| `arp` | ARP (Address Resolution Protocol) cədvəlini göstərir/idarə edir |
| `netsh` | Şəbəkə interfeyslərini, firewall-u konfiqurasiya edir |
| `nbtstat` | NetBIOS over TCP/IP statistikasını göstərir |
| `ftp` | FTP serverlə fayl transferi edir |
| `curl` | Serverdən/serverə məlumat göndərir/alır (HTTP, HTTPS) |
| `ssh` | Uzaq serverə təhlükəsiz bağlantı qurur (OpenSSH) |
| `route` | Şəbəkə marşrutlama cədvəlini göstərir/idarə edir |
| `getmac` | Kompüterin MAC ünvanını göstərir |
| `telnet` | TELNET protokolu ilə uzaq hosta qoşulur |

---

## 3. Sistem Məlumatı və İdarəetmə

| Komanda | İzah |
|---------|------|
| `systeminfo` | Sistem haqqında ətraflı məlumat göstərir (OS, RAM, CPU və s.) |
| `hostname` | Kompüterin şəbəkə adını göstərir |
| `ver` | Windows versiyasını göstərir |
| `whoami` | Cari istifadəçi adını və domenini göstərir |
| `date` | Tarixi göstərir və ya dəyişir |
| `time` | Saatı göstərir və ya dəyişir |
| `wmic` | WMI vasitəsilə sistem məlumatları əldə edir (hardware, software) |
| `driverquery` | Quraşdırılmış cihaz sürücülərinin siyahısını göstərir |
| `msinfo32` | Sistem məlumat pəncərəsini açır |
| `winget` | Windows Paket Meneceri — proqram quraşdırma/yeniləmə |

---

## 4. Disk Əməliyyatları

| Komanda | İzah |
|---------|------|
| `chkdsk` | Diski yoxlayır və xətaları düzəldir |
| `diskpart` | Disk bölmələrini idarə edir (interaktiv alət) |
| `format` | Diski formatlaşdırır |
| `defrag` | Diski defragmentasiya edir (optimallaşdırma) |
| `fsutil` | Fayl sistemi utilitləri (geniş imkanlı) |
| `vol` | Diskin etiketini və seriya nömrəsini göstərir |
| `label` | Disk etiketini dəyişir |
| `convert` | FAT fayl sistemini NTFS-ə çevirir |
| `compact` | NTFS bölməsində faylları sıxışdırır |
| `mountvol` | Disk bölmə nöqtəsini idarə edir |

---

## 5. Proses və Xidmət İdarəetməsi

| Komanda | İzah |
|---------|------|
| `tasklist` | İşləyən proseslərin siyahısını göstərir |
| `taskkill` | Prosesi sonlandırır (PID və ya ad ilə) |
| `start` | Yeni proqram, komanda və ya pəncərə başladır |
| `sc` | Windows xidmətlərini idarə edir (start, stop, query, create, delete) |
| `schtasks` | Planlaşdırılmış tapşırıqlar yaradır/idarə edir |
| `shutdown` | Kompüteri söndürür, yenidən başladır və ya session bağlayır |
| `logoff` | İstifadəçi sessiyasını bağlayır |
| `runas` | Proqramı başqa istifadəçi hesabı ilə işə salır |
| `msiexec` | Windows Installer paketlərini quraşdırır/silir |

---

## 6. Mətn Axtarışı və Emalı

| Komanda | İzah |
|---------|------|
| `find` | Faylda mətn sətri axtarır |
| `findstr` | Fayllarda regex dəstəyi ilə mətn axtarır (güclü axtarış) |
| `sort` | Girişi əlifba sırası ilə sıralayır |
| `more` | Çıxışı səhifə-səhifə göstərir |
| `fc` | İki faylın məzmununu müqayisə edir |
| `comp` | İki faylı bayt-bayt müqayisə edir |

---

## 7. Şəbəkə Paylaşımı (NET Komandaları)

| Komanda | İzah |
|---------|------|
| `net user` | İstifadəçi hesablarını idarə edir (əlavə, silmə, parol) |
| `net use` | Şəbəkə disk paylaşımına qoşulur/ayırır |
| `net share` | Paylaşılan qovluqları göstərir/idarə edir |
| `net view` | Şəbəkədəki kompüterləri və paylaşımları göstərir |
| `net start` / `net stop` | Windows xidmətlərini başladır/dayandırır |
| `net localgroup` | Yerli qrupları idarə edir |
| `net session` | Aktiv şəbəkə sessiyalarını göstərir |

---

## 8. Batch Scripting (Skript Yazma)

| Komanda | İzah |
|---------|------|
| `echo` | Mesajı ekranda göstərir və ya əks-sədanı aktivləşdirir/söndürür |
| `set` | Mühit dəyişənlərini göstərir, təyin edir və ya silir |
| `setx` | Mühit dəyişənini daimi olaraq təyin edir |
| `if` | Şərti əməliyyat icra edir |
| `for` | Dövr (loop) əməliyyatı — fayl, qovluq, siyahı üzrə |
| `goto` | Batch faylında etiketlənmiş sətirə keçir |
| `call` | Bir batch faylından digərini çağırır |
| `pause` | Batch faylının icrasını dayandırır ("davam etmək üçün düyməyə basın") |
| `rem` / `::` | Batch faylında şərh/qeyd yazır |
| `setlocal` | Mühit dəyişənlərinin lokallaşdırılmasını başladır |
| `endlocal` | Mühit dəyişənlərinin lokallaşdırılmasını bitirir |
| `shift` | Batch faylı parametrlərinin mövqeyini dəyişir |
| `choice` | İstifadəçidən klaviatura ilə seçim tələb edir |
| `timeout` | Batch faylının icrasını müəyyən müddət gözlədir |
| `exit` | Skriptdən və ya CMD-dən çıxır |
| `title` | CMD pəncərəsinin başlığını dəyişir |

---

## 9. Təhlükəsizlik və İcazələr

| Komanda | İzah |
|---------|------|
| `icacls` | Fayl/qovluq icazələrini göstərir və dəyişir |
| `cacls` | Fayl icazələrini dəyişir (köhnə versiya, icacls tövsiyə olunur) |
| `takeown` | Faylın sahibliyini öz üzərinə götürür |
| `cipher` | Fayl/qovluqları şifrələyir və ya deşifrə edir (NTFS) |
| `sfc` | Sistem fayllarını yoxlayır və zədələnmiş faylları bərpa edir |
| `reg` | Windows Registry-ni idarə edir (oxuma, yazma, silmə, ixrac) |
| `regedit` | Registry redaktoru pəncərəsi açır |
| `manage-bde` | BitLocker disk şifrələməsini idarə edir |
| `certutil` | Sertifikat idarəetmə aləti |

---

## 10. Digər Faydalı Komandalar

| Komanda | İzah |
|---------|------|
| `cls` | Ekranı təmizləyir |
| `color` | CMD pəncərəsinin rəngini dəyişir |
| `clip` | Çıxışı panoya (clipboard) kopyalayır |
| `doskey` | Komanda tarixçəsini idarə edir, makrolar yaradır |
| `prompt` | Komanda satırının görünüşünü dəyişir |
| `subst` | Qovluğa disk hərfi təyin edir |
| `where` | Faylı qovluq ağacında axtarır (which əvəzi) |
| `help` | Komandalar haqqında kömək məlumatı göstərir |
| `powercfg` | Enerji tərəfləri parametrlərini konfiqurasiya edir |
| `tar` | Arxiv faylları yaradır və çıxarır |
| `expand` | CAB fayllarını açır |
| `cmd` | Yeni CMD pəncərəsi/sessiyası başladır |
| `explorer` | Windows Explorer pəncərəsini açır |
| `mstsc` | Uzaq masaüstü bağlantısı (Remote Desktop) açır |
| `dism` | Windows təsvirlərini xidmət edir (Deployment Image Servicing) |
| `slmgr` | Windows lisenziyasını idarə edir |

---

> **Qeyd**: İstənilən komanda haqqında ətraflı məlumat almaq üçün CMD-də `komanda_adı /?` yazın.
> Məsələn: `ipconfig /?`, `robocopy /?`, `schtasks /?`
