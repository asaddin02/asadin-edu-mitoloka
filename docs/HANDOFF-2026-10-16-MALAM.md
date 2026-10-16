# Serah terima 16 Oktober 2026, malam

Lanjutan dari `HANDOFF-2026-10-16.md`. Semua yang di bawah sudah di-push ke `main`.

## 1. Mitoloka: 111 gambar Codex dipasang

- Commit `118c70cc`. Codex menyelesaikan sesi 2.000 ilustrasi: 113 PNG baru lolos dua tinjauan (Codex native/200px, lalu `root_visual_review` Claude dengan hash yang cocok), dan 32 receipt ditolak karena tidak bisa digambar.
- **111 terpasang. Ilustrasi aktif sekarang 1.998.** `npm run check` dan `npm test` lulus.
- **Ditahan karena `culture: null`:** **bajbur** (batch 2029) dan **germakochi** (batch 2079). Keduanya menyusul praded, mich, dan frankensteins-monster, yang masih menunggu keputusan pemilik soal budaya.
- `scripts/integrate-artwork-batch.mjs` sekarang punya `--skip slug,slug`. Receipt yang ditahan tidak lagi menghentikan sisa batch:
  ```bash
  node scripts/prepare-reviewed-artwork-records.mjs data/artwork-batch-<n>.json --apply --allow-skipped
  node scripts/integrate-artwork-batch.mjs <n> --skip <slug-ditahan>
  ```
  Urutannya harus begitu. Kalau `integrate` dijalankan sebelum `prepare`, prosesnya berhenti di slug pertama yang belum punya rekaman katalog.

## 2. Alur Gemini untuk kelima repo -loka

- Setiap repo punya **`GEMINI.md`** di akarnya: instruksi riset bebas untuk Gemini (web task, satu repo per sesi). Salinan lokalnya ada di `~/Projects/PROMPT-GEMINI/<proyek>.md` di PC asal; kalau mengubah satu, ubah keduanya.
- Pesan pembuka setiap sesi Gemini:
  ```
  Baca GEMINI.md di akar repo ini; itu tugasmu. Kalau materi-gemini/README.md sudah ada, baca juga dan lanjutkan dari tempat sesi sebelumnya berhenti. Kerjakan sebanyak mungkin di sesi ini.
  ```
- Gemini menulis di `materi-gemini/`. Folder ini tidak ikut build atau deploy di repo mana pun. Biotaloka dan Kimialoka mengecualikannya dari prettier.
- **Gemini tidak bisa push.** Ia menyerahkan seluruh folder `materi-gemini/` sebagai zip. Pemilik mengunduhnya, misalnya ke `~/Downloads/materi-gemini-<repo>.zip`, lalu Claude mengekstraknya ke repo, mengoreksi, memasang ke situs, dan push.
- Claude baru mengerjakan sebuah repo kalau baris pertama `materi-gemini/README.md` berbunyi `Status: SELESAI`.

## 3. Kodeloka: kelas HTML, CSS, JavaScript, PHP tayang (94 modul)

- Commit `5f7e185` berisi materi mentah, `e625ac8` koreksinya, dan `f04afea` pemasangan kelasnya. Situs kini punya **23 kelas dan 637 modul**.
- **Tayang:** HTML 27, CSS 20, JavaScript 22, PHP 25 modul.
- **Koreksi:** lima subagen meninjau semua pelajaran. Lognya ada di `materi-gemini/koreksi-claude/`.
- **111 pelajaran templat ditunda:** HTML 27–44, CSS 20–49, JavaScript 22–54, PHP 25–54. Tabel, latihan, dan kuisnya generik.
  - Kecuali CSS 20–49, semuanya dikembalikan ke Gemini, dengan instruksi di `materi-gemini/README.md`.
  - **CSS 20–49 sudah ditulis ulang oleh subagen Claude** dan menunggu keputusan pemilik: tayangkan, atau serahkan ke Gemini.
- **`pembaruan-19-kelas/` (61 modul untuk kelas lama) belum dipasang.** Auditnya ("0 modul") salah, banyak modul mengulang materi yang sudah ada, dan tidak ada kuis per modul. Masalah ini juga sudah dicatat di README untuk Gemini.
- **Cara memasang ulang setelah Gemini mengirim zip baru:**
  ```bash
  cd ~/Projects/asadin-edu-kodeloka
  # ekstrak zip ke materi-gemini/ (timpa), cek diff, koreksi
  # keluarkan nomor yang sudah layak dari "tunda" di scripts/materi-gemini-kelas.json
  node scripts/import-materi-gemini.mjs     # menulis html/ css/ javascript/ php/ app.js
  npm run extract && npm test
  # perbarui angka modul di index.html (TOPIK), courses.json, dan README
  ```
- **Untuk Codex:** tampilan keempat kelas baru masih memakai mesin dan CSS linux apa adanya, ditambah dua aturan agar tabel dan kode tidak meluber di ponsel. Pemilik ingin Codex mempercantiknya di akhir.

## 4. Catatan mesin (PC asal sesi ini)

- Disk `/` tersisa sekitar 4,5 GB (98%).
- Playwright Chromium (headless shell v1243) baru dipasang untuk `npm run extract` Kodeloka.
- PHP tidak terpasang, jadi contoh PHP hanya diperiksa dengan membaca manual.
