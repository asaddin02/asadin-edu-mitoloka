import { bi } from '../ui.js';

// Where corrections go until a public e-mail address exists. Creature pages pre-fill an issue here.
export const REPORT_URL = 'https://github.com/asaddin02/asadin-edu-mitoloka/issues/new';
const SITE = 'https://mitoloka.asadinedu.com';

/** A pre-filled correction report for one creature page (title, link and the questions a reviewer needs). */
export function reportURL(name, slug) {
  const page = `${SITE}/creature/${encodeURIComponent(slug)}`;
  const body = bi(
    `Halaman: ${page}\n\nKalimat atau data yang keliru:\n\n\nSeharusnya (sertakan sumber bila ada):\n\n`,
    `Page: ${page}\n\nSentence or data that is wrong:\n\n\nWhat it should say (include a source if you have one):\n\n`,
  );
  return `${REPORT_URL}?title=${encodeURIComponent(`${bi('Koreksi', 'Correction')}: ${name}`)}&body=${encodeURIComponent(body)}`;
}

const out = (url, label) => `<a class="text-link" href="${url}" target="_blank" rel="noopener noreferrer">${label} ↗</a>`;
const section = (id, title, body) => `<section class="card about-section" id="${id}" aria-labelledby="${id}-title"><h2 id="${id}-title">${title}</h2>${body}</section>`;

export function renderAboutView(main) {
  document.title = `${bi('Tentang Mitoloka', 'About Mitoloka')} · Mitoloka`;
  const nav = [
    ['tentang', bi('Tentang', 'About')],
    ['sumber', bi('Sumber & cara kerja', 'Sources & method')],
    ['lisensi', bi('Lisensi & mengutip', 'Licence & citing')],
    ['privasi', bi('Privasi', 'Privacy')],
    ['koreksi', bi('Laporkan kesalahan', 'Report an error')],
    ['pendamping', bi('Untuk guru & orang tua', 'For teachers & parents')],
  ];
  main.innerHTML = `<div class="edu-support about-page">
    <header class="edu-support-head"><span class="eyebrow">MITOLOKA / ${bi('TENTANG', 'ABOUT')}</span>
      <h1>${bi('Tentang Mitoloka', 'About Mitoloka')}</h1>
      <p>${bi('Ensiklopedia dwibahasa yang gratis tentang makhluk mitologi dan cerita rakyat dari seluruh dunia, dengan sumber yang bisa kamu periksa sendiri.', 'A free bilingual encyclopedia of mythological beings and folklore from around the world, with sources you can check yourself.')}</p>
    </header>
    <nav class="about-toc" aria-label="${bi('Isi halaman', 'On this page')}"><ul>${nav.map(([id, label]) => `<li><a href="/tentang#${id}">${label}</a></li>`).join('')}</ul></nav>
    <div class="about-sections">
    ${section('tentang', bi('Tentang', 'About'), `
      <p>${bi('Mitoloka adalah bagian dari Asadin Edu, payung independen untuk pendidikan di Indonesia yang dikelola satu orang, Prasada Arif Nurudin. Bukan sekolah, bukan perusahaan. Biotaloka, Kimialoka, dan Fisikaloka berada di bawah payung yang sama.', 'Mitoloka is part of Asadin Edu, an independent umbrella for education in Indonesia run by one person, Prasada Arif Nurudin. It is not a school and not a company. Biotaloka, Kimialoka and Fisikaloka sit under the same umbrella.')}</p>
      <p>${bi('Mitoloka gratis, tanpa akun, dan tanpa iklan. Arsipnya terus bertambah: makhluk baru tampil setelah risetnya lengkap dan ilustrasinya lolos tinjauan.', 'Mitoloka is free, needs no account and shows no ads. The archive keeps growing: a being appears once its research is complete and its illustration has passed review.')}</p>
      <p>${out('https://asadinedu.com', 'asadinedu.com')}</p>`)}
    ${section('sumber', bi('Sumber & cara kerja', 'Sources & method'), `
      <p>${bi('Setiap fakta di halaman makhluk berasal dari klaim riset yang memuat kutipan kata demi kata dari sumbernya: teks klasik, kumpulan cerita rakyat, ensiklopedia, museum, dan Wikipedia. Riset dan penulisan dibantu alat AI, lalu setiap kutipan dicocokkan otomatis dengan halaman sumber aslinya. Kalimat yang tidak didukung kutipan tidak boleh tampil.', 'Every fact on a creature page comes from a research claim that carries a word-for-word quote from its source: classical texts, folklore collections, encyclopedias, museums and Wikipedia. Research and writing are assisted by AI tools, then every quote is automatically matched against the original source page. A sentence that no quote supports may not appear.')}</p>
      <p>${bi('Tradisi yang terdokumentasi dibedakan dari film, gim, dan budaya populer. Lencana Power, Threat, dan Fear adalah ringkasan editorial untuk menjelajah, bukan ukuran ilmiah atau klaim budaya asalnya. Penilaian yang hanya diperkirakan dari kisahnya ditandai sebagai perkiraan editorial.', 'Documented tradition is kept apart from films, games and popular culture. The Power, Threat and Fear badges are editorial summaries for exploring, not scientific measures or claims of the source culture. Levels estimated only from a story are marked as editorial estimates.')}</p>
      <p>${bi('Ilustrasi bertanda "AI · ART" dibuat dengan AI berdasarkan ciri yang tercatat di riset, lalu diperiksa dua kali sebelum dipasang. Ilustrasi itu interpretasi artistik, bukan artefak atau rekonstruksi ilmiah.', 'Illustrations marked "AI · ART" are generated with AI from the traits recorded in the research, then checked twice before they are installed. They are artistic interpretations, not artefacts or scholarly reconstructions.')}</p>
      <p><a class="text-link" href="/learn?module=reading">${bi('Belajar membaca sumber dan gambar', 'Learn to read sources and images')} →</a></p>`)}
    ${section('lisensi', bi('Lisensi & cara mengutip', 'Licence & how to cite'), `
      <p>${bi('Teks tulisan Mitoloka dan ilustrasi editorialnya dilisensikan dengan', 'Mitoloka’s own text and its editorial illustrations are licensed under')} ${out('https://creativecommons.org/licenses/by-sa/4.0/deed.id', 'Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)')}. ${bi('Kamu boleh menyalin, mengubah, dan memakainya, termasuk untuk keperluan komersial, asalkan menyebut Mitoloka beserta tautan halamannya dan membagikan hasil turunannya dengan lisensi yang sama.', 'You may copy, adapt and use them, including commercially, as long as you credit Mitoloka with a link to the page and share derived work under the same licence.')}</p>
      <ul>
        <li>${bi('Kutipan sumber tetap milik penerbitnya. Kutipan dari Wikipedia berlisensi CC BY-SA 4.0; sumber lain mengikuti ketentuannya masing-masing, yang tercantum di daftar sumber tiap makhluk.', 'Source quotes remain their publishers’ work. Quotes from Wikipedia are licensed CC BY-SA 4.0; other sources follow their own terms, listed with each creature’s sources.')}</li>
        <li>${bi('Gambar dokumenter, misalnya dari Wikimedia Commons, mengikuti lisensi dan atribusi yang tertera pada gambar itu.', 'Documentary images, for example from Wikimedia Commons, follow the licence and attribution shown with each image.')}</li>
        <li>${bi('Kode aplikasi Mitoloka berlisensi MIT.', 'The Mitoloka application code is MIT licensed.')}</li>
      </ul>
      <p>${bi('Contoh cara mengutip:', 'Example citation:')}</p>
      <p class="about-cite">Mitoloka. (2026). <em>Garuda</em>. Asadin Edu. ${SITE}/creature/garuda</p>`)}
    ${section('privasi', bi('Privasi', 'Privacy'), `
      <ul>
        <li>${bi('Mitoloka tidak memakai akun, formulir, iklan, cookie pelacak, atau analitik pengunjung.', 'Mitoloka uses no accounts, forms, ads, tracking cookies or visitor analytics.')}</li>
        <li>${bi('Pilihan bahasa, favorit, makhluk yang sudah kamu temukan, dan kemajuan belajar disimpan hanya di perangkatmu (penyimpanan lokal browser) dan tidak dikirim ke server. Hapus data situs di pengaturan browser untuk menghapusnya.', 'Your language, favourites, discovered beings and learning progress are stored only on your device (browser local storage) and are not sent to a server. Clear the site data in your browser settings to remove them.')}</li>
        <li>${bi('Situs dan gambarnya dilayani oleh Cloudflare, yang memproses data teknis permintaan seperti alamat IP dan jenis browser untuk mengirim halaman dan menjaga keamanan.', 'The site and its images are served by Cloudflare, which processes technical request data such as IP address and browser type to deliver pages and keep them secure.')} ${out('https://www.cloudflare.com/privacypolicy/', bi('Kebijakan privasi Cloudflare', 'Cloudflare privacy policy'))}</li>
        <li>${bi('Tautan keluar (sumber riset, GitHub, Saweria, Ko-fi) membawamu ke layanan lain dengan kebijakan privasinya sendiri.', 'Outbound links (research sources, GitHub, Saweria, Ko-fi) take you to other services with their own privacy policies.')}</li>
      </ul>`)}
    ${section('koreksi', bi('Laporkan kesalahan', 'Report an error'), `
      <p>${bi('Menemukan fakta yang keliru, kutipan yang tidak cocok, atau ilustrasi yang menyesatkan? Setiap halaman makhluk punya tombol "Laporkan kesalahan" yang sudah mengisi nama dan tautan makhluknya. Sebutkan kalimat yang keliru dan, bila ada, sumber yang benar.', 'Found a wrong fact, a quote that does not match, or a misleading illustration? Every creature page has a "Report an error" button that fills in the creature’s name and link. Say which sentence is wrong and, if you can, give the correct source.')}</p>
      <p>${bi('Laporan dikirim lewat GitHub Issues dan memerlukan akun GitHub gratis.', 'Reports are sent through GitHub Issues and need a free GitHub account.')} ${out(REPORT_URL, bi('Buat laporan umum', 'Open a general report'))}</p>`)}
    ${section('pendamping', bi('Untuk guru & orang tua', 'For teachers & parents'), `
      <p>${bi('Banyak makhluk berasal dari kisah tentang kematian, hantu, setan, dan perang, dan sebagian ilustrasinya sengaja dibuat seram. Untuk anak-anak, jelajahi bersama dan bicarakan bahwa ini kisah budaya, bukan bukti bahwa makhluk itu nyata.', 'Many beings come from stories about death, ghosts, demons and war, and some illustrations are meant to be frightening. With children, explore together and talk about these as cultural stories, not proof that the beings are real.')}</p>
      <p><a class="text-link" href="/learn">${bi('Buka Ruang Belajar', 'Open the Learning Room')} →</a></p>`)}
    </div></div>`;
  const target = location.hash && main.querySelector(location.hash);
  if (target) target.scrollIntoView({ block: 'start' });
}
