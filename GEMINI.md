# Tugas Gemini: memperpanjang cerita makhluk di Mitoloka

> Berkas ini adalah instruksi tugas untuk Gemini. Baca seluruhnya di awal setiap sesi, lalu baca `materi-gemini/README.md` (kalau sudah ada) untuk melanjutkan dari tempat sesi sebelumnya berhenti.

Repo: https://github.com/asaddin02/asadin-edu-mitoloka
Situs: https://mitoloka.asadinedu.com (halaman makhluk: `/creature/<slug>`)

## Latar

Mitoloka adalah ensiklopedia makhluk mitologi dari seluruh dunia dalam bahasa Indonesia dan Inggris. Status per 14 Oktober:
- **3.533 makhluk** sudah punya entri: 3.166 lengkap dan 367 belum lengkap;
- **1.324** makhluk masih berupa nama tanpa entri.

Masalah terbesarnya: **banyak cerita terlalu pendek**. Asal-usul, legenda, wujud, kemampuan, cara menangkal, variasi antardaerah, dan jejaknya di budaya modern sering hanya beberapa kalimat.

Tugasmu: **riset sebebas dan seluas mungkin, lalu tulis cerita dan pengetahuan tentang makhluk-makhluk ini selengkap-lengkapnya di satu folder baru.** Kamu cukup menulis materinya. Setelah itu, Claude Code memindahkan materimu ke data Mitoloka supaya tampil di situs, dan Codex merapikan tampilannya.

## Cari sendiri apa yang kurang

- `data/gemini/fill-status.json` berisi status setiap slug:
  - `tidak-lengkap`: entrinya ada tetapi tipis, dan field `kurang` menyebut kekurangannya;
  - `belum-ada-entri`: makhluknya belum punya entri;
  - `lengkap-…`: entrinya sudah lengkap, tetapi ceritanya mungkin masih pendek.
- Buka halaman makhluk di situs untuk melihat isinya sekarang. `data/creatures.json` terlalu besar untuk dibaca (45 MB).
- Bebas memilih urutan. Saran: mulai dari makhluk terkenal yang ceritanya masih pendek, makhluk Nusantara, lalu entri `tidak-lengkap`.
- Baca `docs/gemini/00-instruksi-utama.md` untuk memahami cara Mitoloka memisahkan tradisi, sejarah, tafsir akademik, dan budaya populer.

## Tempat menulis

Tulis semuanya di folder **`materi-gemini/`** di akar repo, dalam Markdown:

```
materi-gemini/
  README.md            status, daftar isi, dan catatan untuk Claude
  makhluk/
    <slug>.md          satu berkas per makhluk; slug sama dengan di situs dan fill-status.json
```

Isi setiap berkas makhluk boleh sepanjang yang didukung sumber, misalnya:
- nama lain dan nama dalam bahasa aslinya;
- asal budaya dan wilayah;
- wujud, sifat, dan kemampuan;
- legenda dan cerita utama, diceritakan ulang dengan lengkap;
- variasi antardaerah;
- cara menangkal atau menghadapinya menurut tradisi;
- sejarah catatan tertulis tertua;
- tafsir akademik;
- penggambaran modern (film, game, sastra), yang **dipisahkan** dari tradisi.

## Kutipan untuk fakta penting

Situs Mitoloka menampilkan setiap fakta bersama kutipan dari sumbernya. Karena itu, untuk fakta-fakta penting, sertakan **kutipan pendek kata per kata** dari halaman sumber, dalam bahasa asli halaman itu, di samping faktanya. Contoh:

> Pocong digambarkan terbungkus kain kafan. — "…kutipan persis dari halaman…" ([sumber](https://…))

Ceritanya sendiri tetap kamu tulis dengan kata-katamu sendiri. Kutipan hanya bukti.

## Beberapa aturan saja

1. **Bahasa Indonesia** yang baku sebagai bahasa utama. Kalau sempat, sertakan versi bahasa Inggris; kalau tidak, Claude yang menerjemahkan.
2. **Setiap berkas ditutup dengan bagian "Sumber"** berisi tautan halaman yang benar-benar kamu baca. Utamakan:
   - teks primer (misalnya di Sacred Texts, Project Gutenberg, atau Internet Archive);
   - kajian akademik dan jurnal;
   - museum dan lembaga kebudayaan;
   - Britannica dan World History Encyclopedia;
   - Wikipedia hanya sebagai pelengkap.
3. **Dilarang:** wiki penggemar (Fandom, Wikia), blog anonim, konten buatan AI, dan media sosial.
4. Jangan menambah detail yang tidak ada di sumber, walaupun terdengar cocok. Jangan mencampur detail dari film atau game ke dalam cerita tradisi.
5. Kalau ragu akan suatu fakta, tandai dengan `> Perlu dicek:` daripada menebak.
6. Lewati tokoh manusia (nabi, orang suci, raja, pahlawan) dan hewan biasa.
7. Jangan mengurus gambar; itu dikerjakan terpisah.
8. **Hanya tulis di dalam `materi-gemini/`.** Jangan mengubah berkas atau folder lain di repo.
9. Commit ke cabang **`gemini/materi`**, bukan `main`. Folder ini tidak ikut ter-deploy ke situs.

## Status dan tanda selesai

Baris pertama `materi-gemini/README.md` selalu berisi status:

- `Status: BERJALAN`, selama kamu masih menambah materi;
- `Status: SELESAI`, **hanya kalau menurutmu informasinya sudah lebih dari cukup**.

Claude baru mulai mengecek dan memindahkan materi ke situs setelah status berubah menjadi `SELESAI`. Jadi tidak perlu terburu-buru: lanjutkan riset di sesi berikutnya sampai kamu sendiri yakin materinya lengkap.

README juga berisi:
- daftar semua makhluk yang sudah ditulis;
- yang belum sempat ditulis;
- semua tanda `Perlu dicek`;
- catatan sampai mana sesi terakhir berhenti.
