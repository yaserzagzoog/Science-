# تشغيل Claude Code عبر OmniRoute — دليل الإعداد
# Running Claude Code through OmniRoute — Setup Guide

**OmniRoute** بوابة (Gateway) مفتوحة المصدر برخصة MIT، تعمل **محليًا على جهازك**،
تجمع أكثر من 350 مزوّد نماذج خلف عنوان واحد، مع تبديل تلقائي عند نفاد الحصة،
وضغط للنصوص (Prompt compression) قبل إرسالها.

- المستودع: <https://github.com/diegosouzapw/OmniRoute>
- الموقع: <https://omniroute.online/>

الفكرة باختصار: بدل أن يتحدث Claude Code مباشرة إلى Anthropic، يتحدث إلى
`http://localhost:20128/v1`، و OmniRoute هو من يختار المزوّد الفعلي.

```
Claude Code  ──►  OmniRoute (على جهازك)  ──►  Anthropic / GPT / Gemini / مزوّدات مجانية
```

---

## ⚠️ اقرأ هذا أولًا — ثلاث نقاط مهمة

**1. هذا لا يخفّض تكلفة جلسات Claude Code السحابية (claude.ai/code).**
OmniRoute يعمل على جهازك فقط. الجلسة السحابية تعمل داخل حاوية مؤقتة على خوادم
Anthropic ولا تمرّ عبر جهازك. الفائدة تظهر عند تشغيل `claude` من **الطرفية على
جهازك**.

**2. عند تفعيله، شيفرتك وبرومبتاتك تذهب إلى مزوّدين آخرين، لا إلى Anthropic.**
هذا هو جوهر الفكرة — وهو أيضًا المقابل. المزوّدات المجانية تحديدًا قد تستخدم
بياناتك للتدريب. لا تُشغّله على مستودعات فيها أسرار عمل، مفاتيح، بيانات عملاء،
أو أي شيء لا تقبل أن يخرج من جهازك. OmniRoute نفسه محلي ولا يرسل بياناتك إلى
خوادمه — لكن المزوّد الذي يختاره في النهاية طرف ثالث.

> **ملاحظة على المفاتيح:** التثبيت يولّد ملفَّي `.env` — واحد في
> `~/.omniroute/.env` وآخر داخل مجلد الحزمة — ويُحمَّلان مع كل أمر (يظهر ذلك في
> أول سطر من مخرجات أي أمر). مفاتيحك تُخزَّن هناك مشفّرة، لكن لا تنسخ هذين
> الملفين إلى مستودع أو نسخة احتياطية عامة.

**3. رقم «90%» ادّعاء من الجهة المطوِّرة، ولم يُقَس في هذا المشروع.**
الضغط يعمل عبر إعادة صياغة البرومبت (RTK للمخرجات الطويلة، و Caveman الذي يحذف
الكلمات الزائدة). هذا ممتاز لمخرجات الأوامر والاختبارات، وخطِر في العمل الذي
يعتمد على الصياغة الدقيقة — مثل المعادلات، البراهين، والنصوص العربية الدقيقة.
المطوّر يذكر أن الكود وروابط URL و JSON تُحفظ كما هي، لكن باقي النص لا.

> **توصية للمشروع:** استخدمه للمهام العامة والاستكشاف، وأبقِ Anthropic المباشر
> لعمل الفيزياء والرياضيات في هذا المستودع (`fine-structure.html` وما شابه).

---

## الإعداد على جهازك

### 1) التثبيت

```bash
git clone https://github.com/yaserzagzoog/science-.git
cd science-
./scripts/setup-omniroute.sh
```

أو يدويًا:

```bash
npm install -g omniroute
```

**متطلّب النسخة:** الحزمة تعلن `node >=22.22.2 <23 || >=24.0.0 <27` (تم التحقق من
`npm view omniroute engines` — الإصدار المنشور وقت كتابة هذا الملف هو `3.8.49`).
إذا كنت على نسخة أقدم، بدّلها أولًا:

```bash
nvm install 24 && nvm use 24
```

### 2) تشغيل البوابة

```bash
omniroute        # اتركه يعمل في تبويب طرفية مستقل
```

- لوحة التحكم: <http://localhost:20128>
- الـ API: <http://localhost:20128/v1>

يعمل مباشرة بدون أي مفتاح. **تم التحقق فعليًا:** بعد التثبيت مباشرة، بدون أي
مفتاح أو تسجيل، أعاد `GET /v1/models` عدد **115 نموذجًا** (منها 38 اسمًا من نوع
`auto/*`)، من مزوّدات مجانية بلا مفاتيح مثل Felo و DuckDuckGo Gateway.

### 3) توليد بروفايلات Claude Code

> **مهم:** الاسم `auto` وحده **ليس** نموذجًا صالحًا في هذا الإصدار (تم التحقق —
> غير موجود في قائمة `/v1/models`). الأسماء الصحيحة تحمل شرطة مائلة:
> `auto/coding`, `auto/best-coding`, `auto/best-reasoning`, `auto/chat` …

الأمر `setup-claude` يكتب بروفايلات منفصلة في `~/.claude/profiles/<name>/`
كـ `CLAUDE_CONFIG_DIR` مستقل — أي أن **إعداد `claude` الأساسي عندك لا يُمَس**.
هذه أأمن طريقة للتجربة:

```bash
omniroute setup-claude --dry-run        # معاينة ما سيُكتب دون لمس القرص
omniroute setup-claude                  # الكتابة الفعلية
omniroute setup-claude --only auto,glm  # اقتصار على نماذج معيّنة
```

### 4) تشغيل Claude Code عبر البروفايل

```bash
omniroute launch --profile <name>
```

خيارات مفيدة: `--port` (افتراضيًا 20128)، `--remote <url>` لخادم بعيد،
و `--token` (وهو `ANTHROPIC_AUTH_TOKEN` الذي سيرسله Claude Code).

جرّب مهمة حقيقية من مهامك اليومية. راقب: هل جودة الردود مقبولة؟ هل تعمل
الأدوات (قراءة الملفات، التعديل، Bash) كما ينبغي؟

### 5) بديل: الإعداد اليدوي

`omniroute configure claude` يختار مزوّدًا ونموذجًا تفاعليًا ويكتب إعداد الأداة.
أو يدويًا عبر متغيّرات البيئة التي يقرأها Claude Code:

```bash
export ANTHROPIC_BASE_URL="http://localhost:20128/v1"
export ANTHROPIC_AUTH_TOKEN="<مفتاحك من Dashboard → Endpoints>"
export ANTHROPIC_MODEL="auto/coding"
```

### 6) الرجوع إلى Anthropic المباشر

إذا استخدمت البروفايلات (الخطوة 3) فلا يوجد ما تتراجع عنه — شغّل `claude`
عاديًا. أما إن صدّرت المتغيّرات يدويًا:

```bash
unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_MODEL
```

واحذف السطور من `~/.zshrc` أو `~/.bashrc` إن كنت أضفتها هناك.

---

## التحكّم في الضغط (Compression)

الضغط **مُفعّل افتراضيًا**. تحكّم فيه من لوحة التحكم (قسم Compression) أو من
الطرفية:

```bash
omniroute compression status                      # الإعداد الحالي
omniroute compression configure --engine rtk      # تغيير المحرّك
omniroute compression preview --file req.json     # قياس الأثر قبل الاعتماد
```

> **تصحيح:** المحرّكات الفعلية في الإصدار `3.8.49` هي `caveman` / `rtk` /
> `hybrid` / `none` — وليست `off/lite/standard/aggressive/ultra` كما قد توحي
> بعض صفحات التوثيق. تم التحقق من `omniroute compression configure --help`.

خيارات ضبط إضافية: `--caveman-aggressiveness <0.0–1.0>` و `--rtk-budget <n>`.

**نصيحة عملية:** ابدأ بـ `--engine rtk`. هو يضغط مخرجات الأوامر والاختبارات
والـ git — وهي أكبر مصدر لاستهلاك التوكنز في جلسات البرمجة — دون العبث بصياغة
برومبتك أنت. `caveman` هو الذي يحذف الكلمات من نصّك، و `hybrid` يجمع الاثنين.
استخدم `compression preview` لترى الفرق بنفسك بدل الاعتماد على الأرقام المعلنة.

---

## متى تستخدمه ومتى لا

| الحالة | الأنسب |
|---|---|
| استكشاف مستودع، قراءة كود، مهام روتينية | ✅ OmniRoute + مزوّد مجاني |
| نفاد حصتك في منتصف العمل | ✅ OmniRoute (تبديل تلقائي) |
| رياضيات، براهين، فيزياء دقيقة | ❌ Anthropic مباشرة |
| كود فيه أسرار أو مفاتيح أو بيانات عملاء | ❌ Anthropic مباشرة |
| نصوص عربية تحتاج صياغة دقيقة | ❌ أو على الأقل `--engine none` |
| جلسات claude.ai/code السحابية | لا ينطبق — لا يمرّ عبر جهازك |

---

## مشاكل شائعة

| المشكلة | الحل |
|---|---|
| `omniroute: command not found` | تأكد أن مجلد npm العام ضمن `PATH`: `npm bin -g` |
| Claude Code لا يستجيب بعد التهيئة | تأكد أن `omniroute` يعمل في تبويب آخر، ثم `omniroute doctor` |
| المنفذ 20128 مشغول | `omniroute serve --port 20200` وحدّث `ANTHROPIC_BASE_URL` |
| الردود ضعيفة أو ناقصة | `omniroute compression configure --engine rtk` (أو `none`)، أو ثبّت نموذجًا محددًا بدل `auto/*` |
| `unknown command 'run'` | لا يوجد أمر `run` في هذا الإصدار — استخدم `omniroute launch` |
| إيقاف الخادم | `omniroute stop` (و `omniroute restart` لإعادة التشغيل) |
| الأدوات (Tool use) لا تعمل | ليست كل النماذج المجانية تدعم استدعاء الأدوات — جرّب نموذجًا آخر |
| تريد التراجع كليًا | `unset ANTHROPIC_*` ثم `npm uninstall -g omniroute` |

---

## روابط

- OmniRoute (المستودع): <https://github.com/diegosouzapw/OmniRoute>
- OmniRoute (الموقع): <https://omniroute.online/>
- دليل الضغط: <https://github.com/diegosouzapw/OmniRoute/blob/main/docs/compression/COMPRESSION_GUIDE.md>
- دليل ربط الـ CLIs: <https://github.com/diegosouzapw/OmniRoute/blob/main/docs/guides/CLI-INTEGRATIONS.md>
- متغيّرات بيئة Claude Code: <https://code.claude.com/docs/en/settings>

المشاريع مفتوحة المصدر قد تتغير — اتبع README الأحدث دائمًا.
