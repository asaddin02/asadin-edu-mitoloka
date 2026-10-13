/**
 * Static pages for search engines, built by scripts/build-site.mjs.
 * Every public route gets one HTML file (dist/creature/garuda.html → /creature/garuda on Cloudflare Pages) made
 * of the application shell with page-specific metadata and <main id="app"> pre-filled with the page's content as
 * plain, linked HTML. When the app boots it renders the same route over this content, so visitors see the
 * interactive version while crawlers (and readers without JavaScript) get the text and the links.
 */

import { SCALES } from '../js/scaling.js';
import { lessons } from '../js/learning-content.js';

const SITE_NAME = 'Mitoloka';
const FEATURED = ['garuda', 'kitsune', 'jormungandr', 'barong'];
const esc = value =>
  String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
// Bilingual fields are { id, en } objects; some legacy fields are plain strings.
const id = field => (field && typeof field === 'object' ? field.id || field.en || '' : field || '');
const en = field => (field && typeof field === 'object' ? field.en || '' : '');
// Research text carries claim markers such as [garuda-c12]; they belong to the app's footnotes, not to crawlers.
const text = value => String(value ?? '').replace(/<[^>]*>/g, '').replace(/\s*\[[a-z0-9-]+-c\d+\]/gi, '').replace(/\s+/g, ' ').trim();
const clip = (value, max = 300) => {
  const clean = text(value);
  return clean.length <= max ? clean : `${clean.slice(0, max - 1).replace(/\s+\S*$/, '')}…`;
};
const words = value => String(value || '').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
/** An Indonesian paragraph followed by its English counterpart, when both exist. */
const bilingual = (field, tag = 'p') => {
  const a = text(id(field));
  const b = text(en(field));
  if (!a && !b) return '';
  return `<${tag}>${esc(a || b)}</${tag}>${b && b !== a ? `<${tag} lang="en">${esc(b)}</${tag}>` : ''}`;
};
const link = (href, label) => `<a href="${esc(href)}">${esc(label)}</a>`;
const list = items => (items.length ? `<ul>${items.map(item => `<li>${item}</li>`).join('')}</ul>` : '');

const SECTIONS = [
  ['/explore', 'Bestiary', 'Semua makhluk dan legenda dalam arsip'],
  ['/cultures', 'Peradaban', 'Tradisi dan budaya asal setiap legenda'],
  ['/regions', 'Atlas Dunia', 'Kawasan dunia dan tradisi di dalamnya'],
  ['/compare', 'Bandingkan', 'Sandingkan dua legenda'],
  ['/scales', 'Klasifikasi', 'Panduan kelas kekuatan, ancaman, dan rasa takut'],
  ['/learn', 'Ruang Belajar', 'Belajar membaca mitos, legenda, dan sumbernya'],
  ['/journal', 'Jurnal Saya', 'Favorit dan penemuanmu'],
  ['/dukung', 'Dukung Mitoloka', 'Dukungan sukarela untuk ruang belajar gratis'],
];
const sectionNav = () =>
  `<nav class="prerender-sections" aria-label="Bagian situs"><h2>Jelajahi Mitoloka</h2>${list(
    SECTIONS.map(([href, label, desc]) => `${link(href, label)} — ${esc(desc)}`)
  )}</nav>`;

/**
 * @param {object} ctx
 * @param {{ creatures: object[], cultures: object[], regions: object[] }} ctx.data the published library
 * @param {string} ctx.siteURL absolute origin ("https://mitoloka.pages.dev") or ""
 * @param {Record<string, string>} ctx.editorialArt creature slug → artwork URL as the app serves it
 * @param {(data: object, slug: string) => object} ctx.getCreatureBySlug the query engine's resolver
 * @param {string} ctx.today ISO date used as lastmod for pages without their own date
 * @returns {Array<{ route: string, title: string, description: string, image?: string, lastmod: string,
 *   body: string, jsonLd: object[], type: 'website'|'article', noindex?: boolean }>}
 */
export function buildPages({ data, siteURL, editorialArt, getCreatureBySlug, today }) {
  const creatures = data.creatures.filter(c => c.status === 'published' && /^[a-zA-Z0-9_-]+$/.test(c.slug));
  const bySlug = new Map(creatures.map(c => [c.slug, c]));
  const cultures = data.cultures.filter(c => /^[a-zA-Z0-9_-]+$/.test(c.id));
  const cultureById = new Map(cultures.map(c => [c.id, c]));
  const regions = data.regions.filter(r => /^[a-zA-Z0-9_-]+$/.test(r.id));
  const regionById = new Map(regions.map(r => [r.id, r]));
  const regionByName = new Map(regions.map(r => [String(r.name?.en || '').toLowerCase(), r]));
  const regionOf = c => regionById.get(cultureById.get(c.culture)?.region_id) || regionByName.get(String(c.region || '').toLowerCase()) || null;
  const creaturesIn = region =>
    creatures.filter(c => (region.cultures || []).includes(c.culture) || cultureById.get(c.culture)?.region_id === region.id || regionByName.get(String(c.region || '').toLowerCase()) === region);
  const absolute = url => (url && siteURL && url.startsWith('/') ? `${siteURL}${url}` : url);
  const artwork = c => editorialArt[c.slug] || c.images?.[0]?.preview_url || c.images?.[0]?.url || '/assets/logo.png';
  const cultureName = cid => id(cultureById.get(cid)?.name) || words(cid);
  const creatureLink = c => link(`/creature/${c.slug}`, c.canonical_name);
  const creatureItem = c => `${creatureLink(c)}${en(c.display_name) && en(c.display_name) !== c.canonical_name ? ` <span lang="en">(${esc(en(c.display_name))})</span>` : ''} — ${esc(clip(id(c.short_description), 160))}`;
  const breadcrumb = trail => ({
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [['Mitoloka', '/'], ...trail].map(([name, path], i) => ({ '@type': 'ListItem', position: i + 1, name, item: absolute(path) || path })),
  });
  const intro = `<p>Mitoloka adalah ensiklopedia digital dwibahasa (Bahasa Indonesia &amp; English) tentang makhluk mitologi, arwah folklor, naga purba, dan entitas supernatural dari seluruh peradaban dunia, dengan rujukan sumber dan konteks budaya.</p><p lang="en">Mitoloka is a bilingual digital encyclopedia of mythological creatures, folklore spirits, ancient dragons and supernatural beings from world civilizations, with cited sources and cultural context.</p>`;
  const pages = [];
  const page = p => pages.push({ type: 'website', lastmod: today, jsonLd: [], ...p });

  // Home
  const featured = FEATURED.map(slug => bySlug.get(slug)).filter(Boolean);
  const activeCultures = cultures.filter(cu => creatures.some(c => c.culture === cu.id));
  page({
    route: '/',
    title: 'Mitoloka — Ensiklopedia Makhluk Mitologi & Folklor Dunia',
    description: 'Mitoloka adalah ensiklopedia digital dwibahasa untuk mengeksplorasi makhluk mitologi, arwah legenda, naga purba, dan entitas supernatural dari seluruh peradaban dunia dengan rujukan sumber dan konteks budaya.',
    body: `<article class="prerender container"><h1>Mitoloka — Ensiklopedia Makhluk Mitologi &amp; Folklor Dunia</h1>${intro}<p>${creatures.length.toLocaleString('id-ID')} makhluk dan legenda dari ${activeCultures.length} tradisi budaya di ${regions.length} kawasan dunia.</p>
<section><h2>Legenda pilihan</h2>${list((featured.length ? featured : creatures.slice(0, 4)).map(creatureItem))}</section>
<section><h2>Peradaban</h2>${list(activeCultures.map(cu => `${link(`/cultures/${cu.id}`, id(cu.name))} (${creatures.filter(c => c.culture === cu.id).length})`))}</section>
<section><h2>Atlas dunia</h2>${list(regions.map(r => `${link(`/regions/${r.id}`, id(r.name))} — ${esc(clip(id(r.description), 160))}`))}</section>
${sectionNav()}</article>`,
    jsonLd: [{ '@context': 'https://schema.org', '@type': 'WebSite', name: SITE_NAME, url: absolute('/') || '/', inLanguage: ['id', 'en'], description: 'Ensiklopedia dwibahasa makhluk mitologi dan folklor dunia.' }],
  });

  // Creatures
  for (const c of creatures) {
    const full = getCreatureBySlug(data, c.slug) || c;
    const culture = cultureById.get(c.culture);
    const region = regionOf(c);
    const displayEn = en(c.display_name);
    const facts = [
      ['Budaya / Culture', culture ? link(`/cultures/${culture.id}`, id(culture.name)) : esc(words(c.culture))],
      ['Kawasan / Region', region ? link(`/regions/${region.id}`, id(region.name)) : esc(c.region)],
      ['Negara / Country', esc(c.country)],
      ['Era', esc(c.era)],
      ['Klasifikasi / Classification', c.classification ? link(`/explore?classification=${encodeURIComponent(c.classification)}`, words(c.classification)) : ''],
      ['Habitat', esc(c.habitat)],
      ['Elemen / Element', esc(c.element)],
      ['Kemampuan / Abilities', (c.documented_abilities || []).map(a => esc(text(id(a.name)) || text(a.name))).filter(Boolean).join(', ')],
    ].filter(([, v]) => v);
    const related = (full.resolved_related || []).filter(r => bySlug.has(r.slug));
    const sameCulture = creatures.filter(x => x.culture === c.culture && x.slug !== c.slug && !related.some(r => r.slug === x.slug)).slice(0, 6);
    const alternates = (c.alternate_names || []).map(a => a.name).filter(Boolean);
    const description = clip(id(c.short_description) || en(c.short_description), 300);
    const image = absolute(artwork(c));
    const title = `${c.canonical_name}${displayEn && displayEn !== c.canonical_name ? ` (${displayEn})` : ''} — ${culture ? id(culture.name) : words(c.culture)} | ${SITE_NAME}`;
    page({
      route: `/creature/${c.slug}`,
      type: 'article',
      title,
      description,
      image,
      lastmod: (c.updated_at || today).slice(0, 10),
      body: `<article class="prerender container"><nav aria-label="Breadcrumb">${link('/', 'Mitoloka')} › ${link('/explore', 'Bestiary')} › ${culture ? link(`/cultures/${culture.id}`, id(culture.name)) : esc(words(c.culture))}</nav>
<header><h1>${esc(c.canonical_name)}${displayEn && displayEn !== c.canonical_name ? ` <span lang="en">${esc(displayEn)}</span>` : ''}</h1>${c.original_name && c.original_name !== c.canonical_name ? `<p class="prerender-original">${esc(c.original_name)}</p>` : ''}</header>
<figure><img src="${esc(artwork(c))}" alt="${esc(displayEn || c.canonical_name)}" loading="lazy" decoding="async"><figcaption>${editorialArt[c.slug] ? 'Ilustrasi editorial · interpretasi artistik AI' : esc(text(c.images?.[0]?.caption?.id || c.images?.[0]?.caption || ''))}</figcaption></figure>
<section><h2>Ringkasan</h2>${bilingual(c.short_description)}</section>
<section><h2>Kisah dan tradisi</h2>${bilingual(c.long_description)}${c.cultural_context ? `<h3>Konteks budaya</h3>${bilingual(c.cultural_context)}` : ''}</section>
<section><h2>Fakta utama</h2><dl>${facts.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${v}</dd>`).join('')}</dl></section>
${alternates.length ? `<section><h2>Nama lain / Alternate names</h2><p>${alternates.map(esc).join(', ')}</p></section>` : ''}
${c.did_you_know ? `<section><h2>Tahukah kamu? / Did you know?</h2>${bilingual(c.did_you_know)}</section>` : ''}
${related.length || sameCulture.length ? `<section><h2>Makhluk terkait / Related beings</h2>${list([...related, ...sameCulture].map(r => `${creatureLink(bySlug.get(r.slug))}${en(r.display_name) && en(r.display_name) !== r.canonical_name ? ` <span lang="en">(${esc(en(r.display_name))})</span>` : ''}`))}</section>` : ''}
<section><h2>Lanjutkan</h2>${list([
        culture ? `${link(`/cultures/${culture.id}`, `Semua makhluk ${id(culture.name)}`)}` : '',
        region ? `${link(`/regions/${region.id}`, `Kawasan ${id(region.name)}`)}` : '',
        link(`/compare?a=${encodeURIComponent(c.slug)}&b=${c.slug === 'garuda' ? 'kitsune' : 'garuda'}`, `Bandingkan ${c.canonical_name}`),
        link('/scales', 'Panduan kelas kekuatan'),
      ].filter(Boolean))}</section>
${sectionNav()}</article>`,
      jsonLd: [
        {
          '@context': 'https://schema.org',
          '@type': 'Article',
          headline: `${c.canonical_name}${displayEn && displayEn !== c.canonical_name ? ` — ${displayEn}` : ''}`,
          alternativeHeadline: displayEn || undefined,
          description,
          image: image || undefined,
          inLanguage: 'id',
          dateModified: (c.updated_at || today).slice(0, 10),
          datePublished: (c.created_at || c.updated_at || today).slice(0, 10),
          author: { '@type': 'Organization', name: SITE_NAME },
          publisher: { '@type': 'Organization', name: SITE_NAME, url: absolute('/') || undefined },
          mainEntityOfPage: absolute(`/creature/${c.slug}`) || undefined,
          about: { '@type': 'Thing', name: c.canonical_name, alternateName: [displayEn, c.original_name, ...alternates].filter(n => n && n !== c.canonical_name) },
          keywords: [c.canonical_name, culture ? id(culture.name) : c.culture, c.classification, c.country].filter(Boolean).join(', '),
        },
        breadcrumb([['Bestiary', '/explore'], culture ? [id(culture.name), `/cultures/${culture.id}`] : null, [c.canonical_name, `/creature/${c.slug}`]].filter(Boolean)),
      ],
    });
  }

  // Cultures
  page({
    route: '/cultures',
    title: `Peradaban & Tradisi Budaya — ${SITE_NAME}`,
    description: 'Setiap budaya, semesta yang berbeda: telusuri tradisi asal makhluk mitologi dari Nusantara, Yunani, Nordik, Jepang, hingga Mesoamerika.',
    body: `<article class="prerender container"><h1>Peradaban &amp; Tradisi Budaya</h1><p>Setiap budaya, semesta yang berbeda. Telusuri asal-usul makhluk dari mitologi Yunani, Nordik, Shinto Jepang, hingga tradisi Mesoamerika.</p><p lang="en">Every culture, a different universe. Journey from Hellenic and Norse myth to Japanese Shinto lore and Mesoamerican traditions.</p>${list(
      activeCultures.map(cu => `${link(`/cultures/${cu.id}`, id(cu.name))} <span lang="en">(${esc(en(cu.name) || id(cu.name))})</span> — ${esc([cu.region, cu.country].filter(Boolean).join(' · '))}; ${creatures.filter(c => c.culture === cu.id).length} entri`)
    )}${sectionNav()}</article>`,
    jsonLd: [breadcrumb([['Peradaban', '/cultures']])],
  });
  for (const cu of cultures) {
    const own = creatures.filter(c => c.culture === cu.id);
    const region = regionById.get(cu.region_id);
    page({
      route: `/cultures/${cu.id}`,
      title: `${id(cu.name)}${en(cu.name) && en(cu.name) !== id(cu.name) ? ` (${en(cu.name)})` : ''} — Makhluk Mitologi & Folklor | ${SITE_NAME}`,
      description: clip(id(cu.description) || en(cu.description) || `Makhluk mitologi dan folklor dari tradisi ${id(cu.name)}.`, 300),
      body: `<article class="prerender container"><nav aria-label="Breadcrumb">${link('/', 'Mitoloka')} › ${link('/cultures', 'Peradaban')}</nav><h1>${esc(id(cu.name))}${en(cu.name) && en(cu.name) !== id(cu.name) ? ` <span lang="en">${esc(en(cu.name))}</span>` : ''}</h1>${bilingual(cu.description)}
<dl>${region ? `<dt>Kawasan / Region</dt><dd>${link(`/regions/${region.id}`, id(region.name))}</dd>` : cu.region ? `<dt>Kawasan / Region</dt><dd>${esc(cu.region)}</dd>` : ''}${cu.country ? `<dt>Negara / Country</dt><dd>${esc(cu.country)}</dd>` : ''}<dt>Entri</dt><dd>${own.length} makhluk</dd></dl>
<section><h2>Makhluk dalam tradisi ini / Beings of this tradition</h2>${own.length ? list(own.map(creatureItem)) : '<p>Belum ada entri yang diterbitkan untuk tradisi ini. / No published entries yet.</p>'}</section>
<p>${link(`/explore?culture=${encodeURIComponent(cu.id)}`, `Jelajahi ${id(cu.name)} di Bestiary`)}</p>${sectionNav()}</article>`,
      jsonLd: [breadcrumb([['Peradaban', '/cultures'], [id(cu.name), `/cultures/${cu.id}`]])],
    });
  }

  // Regions
  page({
    route: '/regions',
    title: `Atlas Dunia — Kawasan & Tradisi | ${SITE_NAME}`,
    description: 'Peta imajinasi manusia: kawasan dunia dan tradisi budaya tempat makhluk mitologi dan legenda berasal.',
    body: `<article class="prerender container"><h1>Atlas Dunia</h1><p>Satu dunia, banyak keajaiban. Telusuri dunia melalui kisahnya: kawasan, tradisi, dan makhluk yang lahir di sana.</p><p lang="en">One world, many wonders. Discover the world through its stories: regions, traditions and the beings born there.</p>${list(
      regions.map(r => `${link(`/regions/${r.id}`, id(r.name))} <span lang="en">(${esc(en(r.name) || id(r.name))})</span> — ${esc(clip(id(r.description), 200))}`)
    )}${sectionNav()}</article>`,
    jsonLd: [breadcrumb([['Atlas Dunia', '/regions']])],
  });
  for (const r of regions) {
    const own = creaturesIn(r);
    const traditions = (r.cultures || []).map(cid => cultureById.get(cid)).filter(Boolean);
    page({
      route: `/regions/${r.id}`,
      title: `${id(r.name)}${en(r.name) && en(r.name) !== id(r.name) ? ` (${en(r.name)})` : ''} — Atlas Makhluk Mitologi | ${SITE_NAME}`,
      description: clip(id(r.description) || en(r.description), 300),
      body: `<article class="prerender container"><nav aria-label="Breadcrumb">${link('/', 'Mitoloka')} › ${link('/regions', 'Atlas Dunia')}</nav><h1>${esc(id(r.name))}${en(r.name) && en(r.name) !== id(r.name) ? ` <span lang="en">${esc(en(r.name))}</span>` : ''}</h1>${bilingual(r.description)}
<section><h2>Tradisi di kawasan ini / Traditions</h2>${list(traditions.map(cu => `${link(`/cultures/${cu.id}`, id(cu.name))} (${creatures.filter(c => c.culture === cu.id).length})`))}</section>
<section><h2>Makhluk dari kawasan ini / Beings of this region</h2>${own.length ? list(own.map(creatureItem)) : '<p>Belum ada entri yang diterbitkan untuk kawasan ini. / No published entries yet.</p>'}</section>
<p>${link(`/explore?region=${encodeURIComponent(r.id)}`, `Jelajahi ${id(r.name)} di Bestiary`)}</p>${sectionNav()}</article>`,
      jsonLd: [breadcrumb([['Atlas Dunia', '/regions'], [id(r.name), `/regions/${r.id}`]])],
    });
  }

  // Explore: the complete index, so every entry is one link away from a section page.
  const byLetter = new Map();
  for (const c of [...creatures].sort((a, b) => a.canonical_name.localeCompare(b.canonical_name))) {
    const letter = (c.canonical_name[0] || '#').toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const key = /[A-Z]/.test(letter) ? letter : '#';
    byLetter.set(key, [...(byLetter.get(key) || []), c]);
  }
  page({
    route: '/explore',
    title: `Bestiary — Semua Makhluk Mitologi & Legenda | ${SITE_NAME}`,
    description: `Indeks lengkap ${creatures.length.toLocaleString('id-ID')} makhluk mitologi, arwah folklor, dan legenda dari seluruh dunia, dengan pencarian dan filter budaya, kawasan, klasifikasi, dan kelas kekuatan.`,
    body: `<article class="prerender container"><h1>Bestiary</h1><p>Temui makhluk dari setiap legenda: ${creatures.length.toLocaleString('id-ID')} entri yang dapat disaring menurut budaya, kawasan, klasifikasi, dan kelas kekuatan.</p><p lang="en">Meet the beings behind every legend: ${creatures.length.toLocaleString('en')} entries, filterable by culture, region, classification and power class.</p>
<section><h2>Peradaban</h2>${list(activeCultures.map(cu => link(`/cultures/${cu.id}`, id(cu.name))))}</section>
${[...byLetter.entries()].map(([letter, group]) => `<section><h2>${esc(letter)}</h2>${list(group.map(c => `${creatureLink(c)} — ${esc(cultureName(c.culture))}`))}</section>`).join('')}
${sectionNav()}</article>`,
    jsonLd: [breadcrumb([['Bestiary', '/explore']])],
  });

  // Scales
  const scaleNames = { power: ['Kelas kekuatan', 'Power'], threat: ['Skala ancaman', 'Threat'], fear: ['Skala rasa takut', 'Fear'] };
  page({
    route: '/scales',
    title: `Panduan Kelas Kekuatan, Ancaman & Rasa Takut | ${SITE_NAME}`,
    description: 'Tujuh kelas kekuatan dari Mortal hingga Transcendent, tujuh tingkat ancaman, dan enam tingkat rasa takut: skala editorial Mitoloka untuk membaca makhluk mitologi.',
    body: `<article class="prerender container"><h1>Panduan Klasifikasi</h1><p>Skala editorial Mitoloka untuk membaca makhluk mitologi: kelas kekuatan, tingkat ancaman, dan tingkat rasa takut. Skala ini tidak menggantikan tradisi; ia membantu membandingkan.</p><p lang="en">Mitoloka' editorial scales for reading mythological beings: power class, threat level and fear level. They do not replace tradition; they help comparison.</p>
${Object.entries(SCALES).map(([axis, levels]) => `<section><h2>${esc(scaleNames[axis]?.[0] || axis)} <span lang="en">${esc(scaleNames[axis]?.[1] || '')}</span></h2><ol>${levels.map(l => `<li><strong>${esc(l.name)}</strong>${axis === 'power' ? ` — ${link(`/explore?power=${l.id}`, 'lihat makhluk')}` : ''}${bilingual(l.description)}</li>`).join('')}</ol></section>`).join('')}
${sectionNav()}</article>`,
    jsonLd: [breadcrumb([['Klasifikasi', '/scales']])],
  });

  // Learn
  page({
    route: '/learn',
    title: `Ruang Belajar — Membaca Mitos, Legenda & Sumbernya | ${SITE_NAME}`,
    description: 'Pelajari cara membaca mitos, legenda, dan folklor: jenis cerita, simbol, menelusuri sumber, dan menguji pemahaman di Ruang Belajar Mitoloka.',
    body: `<article class="prerender container"><h1>Ruang Belajar</h1><p>Belajar melihat di balik legenda: pahami simbol, telusuri sumber, dan uji pemahamanmu.</p><p lang="en">Learn to read between the legends: explore symbols, trace sources, and test your understanding.</p>
${lessons.map(l => `<section><h2>${esc(id(l.title))} <span lang="en">${esc(en(l.title))}</span></h2>${bilingual(l.summary)}${(l.objectives || []).length ? list(l.objectives.map(o => esc(text(id(o))))) : ''}<p>${link(`/learn?module=${encodeURIComponent(l.id)}`, `Buka modul (${l.minutes} menit)`)}</p></section>`).join('')}
${sectionNav()}</article>`,
    jsonLd: [breadcrumb([['Ruang Belajar', '/learn']])],
  });

  // Compare
  const a = bySlug.get('garuda') || creatures[0];
  const b = bySlug.get('kitsune') || creatures[1] || creatures[0];
  page({
    route: '/compare',
    title: `Bandingkan Legenda — Kekuatan & Perbedaannya | ${SITE_NAME}`,
    description: 'Sandingkan dua makhluk mitologi dari tradisi berbeda: asal, klasifikasi, kemampuan, dan kelas kekuatan dibandingkan berdampingan.',
    body: `<article class="prerender container"><h1>Sandingkan Legenda</h1><p>Kenali kekuatan dan perbedaannya: pilih dua makhluk dan bandingkan asal, klasifikasi, kemampuan, dan kelas kekuatannya.</p><p lang="en">Uncover their powers and differences: pick two beings and compare origin, classification, abilities and power class side by side.</p>
${a && b ? `<p>Contoh: ${link(`/compare?a=${a.slug}&b=${b.slug}`, `${a.canonical_name} vs ${b.canonical_name}`)}</p>` : ''}
<section><h2>Mulai dari</h2>${list((featured.length ? featured : creatures.slice(0, 4)).map(creatureItem))}</section>${sectionNav()}</article>`,
    jsonLd: [breadcrumb([['Bandingkan', '/compare']])],
  });

  // Journal
  page({
    route: '/journal',
    title: `Jurnal Saya — Favorit & Penemuan | ${SITE_NAME}`,
    description: 'Jurnal pribadi Mitoloka: makhluk favorit dan legenda yang sudah kamu temukan, tersimpan di perangkatmu.',
    body: `<article class="prerender container"><h1>Jurnal Saya</h1><p>Favorit dan penemuanmu tersimpan di perangkat ini. Tandai makhluk sebagai favorit dari halaman detailnya, lalu kembali ke sini untuk melanjutkan penjelajahan.</p><p lang="en">Your favorites and discoveries are kept on this device. Mark beings as favorites from their pages, then return here to continue exploring.</p>${sectionNav()}</article>`,
    jsonLd: [breadcrumb([['Jurnal Saya', '/journal']])],
  });

  // Support
  page({
    route: '/dukung',
    title: `Dukung Mitoloka — Ruang Belajar Gratis | ${SITE_NAME}`,
    description: 'Mitoloka adalah ruang belajar gratis. Orang tua, guru, dan sahabat pendidikan dapat mendukung pengembangannya secara sukarela.',
    body: `<article class="prerender container"><h1>Dukung Mitoloka</h1><p>Mitoloka adalah ruang belajar gratis. Jika bermanfaat, orang tua, guru, dan sahabat pendidikan dapat mendukung pengembangannya secara sukarela. Dukungan bersifat sukarela; belajar tetap gratis.</p><p lang="en">Mitoloka is a free learning space. Parents, teachers and friends of education can voluntarily support its development. Support is optional; learning stays free.</p>${sectionNav()}</article>`,
    jsonLd: [breadcrumb([['Dukung Mitoloka', '/dukung']])],
  });

  return pages;
}

/**
 * Renders a page into the application shell: head metadata replaced, <main id="app"> pre-filled.
 * @param {string} shell dist/index.html as build-site.mjs prepared it (static-mode metas, verification)
 * @param {ReturnType<typeof buildPages>[number]} page
 * @param {string} siteURL absolute origin or ""
 */
export function renderPage(shell, page, siteURL) {
  const url = siteURL ? `${siteURL}${page.route === '/' ? '/' : page.route}` : '';
  const image = page.image || (siteURL ? `${siteURL}/assets/logo.png` : '/assets/logo.png');
  let html = shell;
  const replaceTag = (pattern, replacement) => {
    if (!pattern.test(html)) throw new Error(`index.html head changed (${pattern}); update scripts/prerender.mjs`);
    html = html.replace(pattern, replacement);
  };
  replaceTag(/<title>[^<]*<\/title>/, `<title>${esc(page.title)}</title>`);
  replaceTag(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${esc(page.description)}">`);
  replaceTag(/<meta property="og:type" content="[^"]*">/, `<meta property="og:type" content="${page.type === 'article' ? 'article' : 'website'}">`);
  replaceTag(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${esc(page.title)}">`);
  replaceTag(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${esc(page.description)}">`);
  replaceTag(/<meta property="og:image" content="[^"]*">/, `<meta property="og:image" content="${esc(image)}">`);
  replaceTag(/<meta name="twitter:title" content="[^"]*">/, `<meta name="twitter:title" content="${esc(page.title)}">`);
  replaceTag(/<meta name="twitter:description" content="[^"]*">/, `<meta name="twitter:description" content="${esc(page.description)}">`);
  replaceTag(/<meta name="twitter:image" content="[^"]*">/, `<meta name="twitter:image" content="${esc(image)}">`);
  // og:url and canonical exist only when the site knows its public origin.
  html = html.replace(/\s*<meta property="og:url" content="[^"]*">/, url ? `\n  <meta property="og:url" content="${esc(url)}">` : '');
  html = html.replace(/\s*<link rel="canonical" href="[^"]*">/, '');
  if (url) html = html.replace('</head>', `  <link rel="canonical" href="${esc(url)}">\n</head>`);
  if (page.noindex) html = html.replace('</head>', '  <meta name="robots" content="noindex">\n</head>');
  if (page.jsonLd?.length)
    html = html.replace(
      '</head>',
      `${page.jsonLd.map(data => `  <script type="application/ld+json">${JSON.stringify(data).replace(/</g, '\\u003c')}</script>`).join('\n')}\n</head>`
    );
  const main = /<main id="app"[^>]*>[\s\S]*?<\/main>/;
  if (!main.test(html)) throw new Error('index.html lost <main id="app">; update scripts/prerender.mjs');
  html = html.replace(main, `<main id="app" role="main" tabindex="-1">\n${page.body}\n  </main>`);
  return html;
}

/** dist/<route>.html for a route; the home page is index.html. */
export function fileFor(route) {
  return route === '/' ? 'index.html' : `${route.replace(/^\//, '')}.html`;
}
