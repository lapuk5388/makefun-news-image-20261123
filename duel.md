# Duel Varian — NI23 G3 Final 6 · THE LONG DAY POST

## Konsep
Halaman depan koran lurus (bukan template dekoratif): kicker hitungan jujur,
masthead Playfair Black 72px, strip 6 angka pool, 12 kartu utama berilustrasi
(lead + 11 grid), peta dunia titik-titik dengan 12 pin bernomor, timeline UTC
5 slot, kolom ALSO ON sampai 40 cerita, kotak DATE CHECK merah 6 buangan
bernama + bertanggal, footer verifikasi.

Lead (kartu #1): pool #6 — AS membuka lagi rekaman UFO yang difilmkan di
Timur Tengah (BBC). Trio lead: #6 UFO + #43 Demokrat menangi DPR 258–173 +
#12 anak Kyiv ditarik hidup dari reruntuhan. Semua angka dari ni23-pool.md
(258–173 · 720/9d · 14 hilang Kyiv · $3.538 · Rs 28.000 cr Tata Steel ·
65,9% IndiGo · $95 jt Ewing · $5 jt Google–IIT).

## Tiga varian yang diadu
- **A — abu muda · tinta ungu malam · aksen ungu muda:** palet sesuai konsep
  akun (abu muda / ungu malam / perak), masthead Playfair Black, kartu terang.
- **B — krem hangat · tinta plum · aksen emas tua:** masthead Playfair Bold;
  aksen emas melemahkan kontras strip angka dan tag sumber pada uji 300px.
- **C — abu lavendel · tinta ungu royal · aksen perak:** kartu lead dibalik
  (blok tinta penuh); fakta lead di atas blok gelap terbaca lebih berat dan
  halaman terasa lebih sesak di 300px.

## Pemenang: A
Kontras tinta-terhadap-kertas tertinggi dari ketiganya, masthead Black paling
tegas, dan pada uji 300px seluruh judul 12 kartu + tanggal + strip angka tetap
terbaca tanpa ada elemen yang tenggelam. B kalah di kontras aksen; C kalah di
keterbacaan fakta lead.

## Uji 300px
entry.png dikecilkan ke 300×300 (/tmp/ni23g3-final6-300.png) dan diperiksa:
masthead "THE LONG DAY POST", tanggal "Monday 23 November 2026", keenam angka
strip, judul lead, dan judul ke-12 kartu utama semuanya masih terbaca. LULUS.

## Verifikasi teknis
- entry.png: 280.616 byte (≤ 1.048.576), IHDR terverifikasi manual 1024×1024,
  sha256 62f204efff0663fdd5fac35369dbc61fb2a4dafb8174c9c063621a90da1f2b39.
- Margin checker (margin_check.py --fresh ni23-fresh.txt): 13/13 LOLOS.
- main.py stdlib-only copy-only; dua run uji byte-identik.

## Kenapa lebih kuat dari entry G2 akun ini
Entry G2 Final 6 memakai konsep "Jalur Domino" — susunan dekoratif yang tidak
menamai bentuk koran. G3 ini halaman depan koran sungguhan: masthead raksasa
bertanggal eksplisit, 12 kartu besar berfont ≥24px dengan tag sumber 100%,
peta berpin, timeline, dan keluasan 40 cerita — menjawab langsung kriteria
juri soal keluasan, keterbacaan di ±300px, dan penamaan hari.
