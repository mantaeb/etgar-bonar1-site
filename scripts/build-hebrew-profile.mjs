import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourcePath = path.join(root, "machine/he/profile.json");
const outputPath = path.join(root, "he/index.html");
const profile = JSON.parse(fs.readFileSync(sourcePath, "utf8"));

const escapeHtml = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#39;");

const ltr = (value) => `<bdi lang="en" dir="ltr">${escapeHtml(value)}</bdi>`;
const jsonForHtml = (value) => JSON.stringify(value, null, 2).replaceAll("<", "\\u003c");
const mixedHebrew = (value) => {
  let html = escapeHtml(value);
  for (const term of ["contact sales", "self-service", "PLG", "API", "AI"]) {
    html = html.replaceAll(term, `<bdi lang="en" dir="ltr">${term}</bdi>`);
  }
  return html;
};

const occupation = profile.career.map((item) => ({
  "@type": "Role",
  roleName: item.role,
  startDate: item.startDate,
  endDate: item.endDate,
  worksFor: {
    "@type": "Organization",
    name: item.company,
    alternateName: item.companyHebrew
  }
}));

const structuredData = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": profile.entity.id,
      name: profile.entity.name,
      alternateName: profile.entity.alternateName,
      url: profile.englishProfileUrl,
      sameAs: profile.entity.sameAs,
      jobTitle: profile.entity.role,
      description: profile.page.description,
      knowsAbout: [
        "Revenue leadership",
        "Go-to-market strategy",
        "General management",
        "Product-led growth",
        "AI-mediated customer journeys"
      ],
      alumniOf: profile.education.map((item) => ({
        "@type": "CollegeOrUniversity",
        name: item.institution,
        alternateName: item.institutionHebrew
      })),
      hasOccupation: occupation
    },
    {
      "@type": "ProfilePage",
      "@id": `${profile.canonicalHumanUrl}#profile`,
      url: profile.canonicalHumanUrl,
      name: profile.page.title,
      description: profile.page.description,
      inLanguage: "he-IL",
      dateModified: profile.dateModified,
      mainEntity: { "@id": profile.entity.id }
    },
    {
      "@type": "CreativeWork",
      "@id": profile.aiBuild.entityId,
      name: profile.aiBuild.structuredName,
      description: profile.aiBuild.structuredDescription,
      url: profile.aiBuild.url,
      creator: { "@id": profile.entity.id }
    }
  ]
};

const careerHtml = profile.career.map((item, index) => `
        <article class="career-card${index === 0 ? " career-featured" : ""}">
          <div class="career-meta"><span>${escapeHtml(item.period)}</span><span>${escapeHtml(item.companyHebrew)} ${ltr(item.company)}</span></div>
          <div class="career-body">
            <h3>${ltr(item.role)}</h3>
            <p>${escapeHtml(item.description)}</p>
          </div>
        </article>`).join("");

const educationHtml = profile.education.map((item, index) => `
        <article${index === 0 ? ' class="credential-lbs"' : ""}>
${index === 0 ? '          <img class="credential-photo" src="/assets/images/lbs-campus.webp" alt="הקמפוס של לונדון ביזנס סקול בריג\'נטס פארק" width="665" height="604" loading="lazy" decoding="async">\n' : ""}          <div${index === 0 ? ' class="credential-content"' : ""}>
${index === 0 ? '            <img class="credential-logo" src="/assets/logos/london-business-school.svg" alt="London Business School" width="768" height="768">\n' : ""}            <span>${ltr(item.degree)}</span>
            <h3>${escapeHtml(item.institutionHebrew)} ${ltr(item.institution)}</h3>
            <p>${escapeHtml(item.field)}, ${escapeHtml(item.period)}.</p>
          </div>
        </article>`).join("");

const focusHtml = profile.currentFocus.paragraphs
  .map((paragraph) => `        <p>${escapeHtml(paragraph)}</p>`)
  .join("\n");

const aiBuildHtml = profile.aiBuild.paragraphs
  .map((paragraph) => `        <p>${mixedHebrew(paragraph)}</p>`)
  .join("\n");

const html = `<!doctype html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(profile.page.title)}</title>
  <meta name="description" content="${escapeHtml(profile.page.description)}">
  <meta name="author" content="Etgar Bonar">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="${escapeHtml(profile.canonicalHumanUrl)}">
  <link rel="alternate" hreflang="he" href="${escapeHtml(profile.canonicalHumanUrl)}">
  <link rel="alternate" hreflang="en" href="${escapeHtml(profile.englishProfileUrl)}">
  <link rel="alternate" hreflang="x-default" href="${escapeHtml(profile.englishProfileUrl)}">
  <link rel="alternate" type="application/json" href="${escapeHtml(profile.machineUrl)}" title="פרופיל מובנה בעברית">
  <link rel="stylesheet" href="/styles.css?v=22">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="48x48" href="/assets/favicon-48.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
  <link rel="apple-touch-icon" href="/assets/icon-180.png">
  <meta property="og:type" content="profile">
  <meta property="og:locale" content="he_IL">
  <meta property="og:locale:alternate" content="en_US">
  <meta property="og:site_name" content="Etgar Bonar">
  <meta property="og:title" content="${escapeHtml(profile.page.title)}">
  <meta property="og:description" content="${escapeHtml(profile.page.description)}">
  <meta property="og:url" content="${escapeHtml(profile.canonicalHumanUrl)}">
  <meta property="og:image" content="https://etgarbonar.com/assets/social-card.png">
  <meta property="og:image:alt" content="אתגר בונר, Revenue and GTM Executive">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${escapeHtml(profile.page.title)}">
  <meta name="twitter:description" content="${escapeHtml(profile.page.description)}">
  <meta name="twitter:image" content="https://etgarbonar.com/assets/social-card.png">
  <script type="application/ld+json">
${jsonForHtml(structuredData)}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">מעבר לתוכן</a>
  <header class="site-header">
    <a class="brand" href="/he/" aria-label="אתגר בונר, דף הבית בעברית">
      <span class="brand-mark" aria-hidden="true"><img src="/assets/logo-256.png" alt="" width="38" height="38" decoding="async"></span>
      <span>אתגר בונר <span class="brand-he" lang="en" dir="ltr">Etgar Bonar</span></span>
    </a>
    <nav class="site-nav" aria-label="ניווט ראשי">
      <a class="nav-wide" href="#record">קריירה</a>
      <a href="#focus">המיקוד הנוכחי</a>
      <a class="nav-wide" href="#build">בניית ${ltr("AI")}</a>
      <a class="language-link" href="/" hreflang="en" lang="en" dir="ltr">English</a>
      <a class="nav-cta" href="#contact">יצירת קשר</a>
    </nav>
  </header>

  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-grid" aria-hidden="true"></div>
      <div class="hero-system" aria-hidden="true"></div>
      <div class="hero-copy">
        <p class="eyebrow light">${ltr(profile.page.eyebrow)}</p>
        <h1 id="hero-title">${escapeHtml(profile.page.headline)}<br><span>${escapeHtml(profile.page.headlineContinuation)}</span></h1>
        <p class="hero-summary">${escapeHtml(profile.page.summary)}</p>
        <p class="hero-thesis">${escapeHtml(profile.currentFocus.title)}</p>
        <div class="actions">
          <a class="button button-quiet" href="#record">${escapeHtml(profile.page.recordCta)}</a>
          <a class="button button-primary" href="/" hreflang="en">${escapeHtml(profile.page.englishCta)}</a>
        </div>
      </div>
      <aside class="hero-aside" aria-label="תקציר הפרופיל המקצועי">
        <div class="portrait-mark" aria-hidden="true"><img src="/assets/logo-256.png" alt="" width="112" height="112" decoding="async"></div>
        <p class="aside-kicker">מנהיגות מסחרית מקצה לקצה</p>
        <p>${escapeHtml(profile.page.scope)}</p>
        <a href="${escapeHtml(profile.entity.linkedin)}" rel="me">לפרופיל ב-${ltr("LinkedIn")} <span aria-hidden="true">↗</span></a>
      </aside>
    </section>

    <section class="brand-strip" aria-label="ניסיון מקצועי בחברות גלובליות מובילות">
      <p>ניסיון שנבנה בחברות</p>
      <ul>
        <li><img src="/assets/logos/amazon.svg" alt="אמזון, Amazon" width="603" height="182"></li>
        <li><img src="/assets/logos/taboola.svg" alt="טאבולה, Taboola" width="723" height="175"></li>
        <li><img src="/assets/logos/rapyd.svg" alt="ראפיד, Rapyd" width="1535" height="472"></li>
        <li><img src="/assets/logos/lokalise.svg" alt="לוקלייז, Lokalise" width="2810" height="600"></li>
        <li><img src="/assets/logos/johnson-and-johnson.svg" alt="ג'ונסון אנד ג'ונסון, Johnson &amp; Johnson" width="1000" height="181"></li>
      </ul>
    </section>

    <section class="record section" id="record" aria-labelledby="record-title">
      <div class="section-intro record-intro">
        <p class="eyebrow">הקריירה המקצועית</p>
        <h2 id="record-title">אחריות מסחרית רחבה, לא מסלול פונקציונלי אחד.</h2>
        <p>${escapeHtml(profile.page.careerIntro)}</p>
        <p class="record-language-note">${escapeHtml(profile.page.careerEnglishNote)}</p>
        <a class="text-link" href="/#record" hreflang="en">${escapeHtml(profile.page.careerEnglishCta)} <span aria-hidden="true">←</span></a>
      </div>
      <div class="career-list">${careerHtml}
      </div>
    </section>

    <section class="frontier-teaser section-dark" id="focus" aria-labelledby="focus-title">
      <div class="section-intro">
        <p class="eyebrow light">המיקוד הנוכחי</p>
        <h2 id="focus-title">${escapeHtml(profile.currentFocus.title)}</h2>
      </div>
      <div class="frontier-copy">
${focusHtml}
        <a class="text-link light-link" href="${escapeHtml(profile.currentFocus.pointOfViewUrl)}" hreflang="en">${escapeHtml(profile.currentFocus.pointOfViewLabel)} <span aria-hidden="true">←</span></a>
      </div>
    </section>

    <section class="build section" id="build" aria-labelledby="build-title">
      <div>
        <p class="eyebrow">${mixedHebrew(profile.aiBuild.eyebrow)}</p>
        <h2 id="build-title">${mixedHebrew(profile.aiBuild.title)}</h2>
      </div>
      <div class="build-copy">
${aiBuildHtml}
        <div class="inline-links">
          <a class="text-link" href="${escapeHtml(profile.aiBuild.url)}" hreflang="en">${mixedHebrew(profile.aiBuild.label)} <span aria-hidden="true">←</span></a>
          <a class="text-link" href="${escapeHtml(profile.aiBuild.faqUrl)}" hreflang="en">${mixedHebrew(profile.aiBuild.faqLabel)} <span aria-hidden="true">←</span></a>
        </div>
      </div>
    </section>

    <section class="credentials section" aria-labelledby="credentials-title">
      <div class="section-intro">
        <p class="eyebrow">השכלה</p>
        <h2 id="credentials-title">בסיס עסקי ומדעי.</h2>
      </div>
      <div class="credential-grid hebrew-credentials">${educationHtml}
      </div>
    </section>

    <section class="contact section-dark" id="contact" aria-labelledby="contact-title">
      <div>
        <p class="eyebrow light">יצירת קשר</p>
        <h2 id="contact-title">לבניית מערכת מסחרית שמתאימה לשינוי הבא.</h2>
      </div>
      <div class="actions contact-actions">
        <a class="button button-primary" href="mailto:${escapeHtml(profile.entity.email)}">אימייל לאתגר</a>
        <a class="button button-quiet" href="${escapeHtml(profile.entity.linkedin)}">חיבור ב-${ltr("LinkedIn")}</a>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <p>© 2026 אתגר בונר.</p>
    <p><a href="/" lang="en" dir="ltr">Full professional profile in English</a></p>
  </footer>
  <script src="/motion.js" defer></script>
  <script src="/hero-system.js?v=5" defer></script>
</body>
</html>
`;

if (process.argv.includes("--check")) {
  const current = fs.existsSync(outputPath) ? fs.readFileSync(outputPath, "utf8") : "";
  if (current !== html) {
    console.error("he/index.html is out of date. Run: node scripts/build-hebrew-profile.mjs");
    process.exit(1);
  }
  console.log("Hebrew profile output is current.");
} else {
  fs.writeFileSync(outputPath, html, "utf8");
  console.log(`Generated ${path.relative(root, outputPath)} from ${path.relative(root, sourcePath)}.`);
}
