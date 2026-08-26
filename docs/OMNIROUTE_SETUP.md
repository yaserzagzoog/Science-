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

يعمل مباشرة بدون أي مفتاح، لأن مزوّدات مجانية بلا مفاتيح (OpenCode Free و Felo)
مُهيّأة مسبقًا في وضع `auto`.

### 3) تجربة Claude Code دون تغيير أي إعداد

هذه أفضل طريقة للتجربة — لا تكتب شيئًا في ملفات الإعداد:

```bash
omniroute run claude --model auto --dry-run   # لمعاينة ما سيُشغَّل
omniroute run claude --model auto             # للتشغيل الفعلي
```

جرّب مهمة حقيقية من مهامك اليومية. راقب: هل جودة الردود مقبولة؟ هل تعمل
الأدوات (قراءة الملفات، التعديل، Bash) كما ينبغي؟

### 4) التثبيت الدائم (فقط بعد أن تقتنع بالخطوة 3)

```bash
omniroute configure claude     # اختيار تفاعلي للمزوّد والنموذج
```

أو يدويًا عبر متغيّرات البيئة التي يقرأها Claude Code:

```bash
export ANTHROPIC_BASE_URL="http://localhost:20128/v1"
export ANTHROPIC_AUTH_TOKEN="<مفتاحك من Dashboard → Endpoints>"
export ANTHROPIC_MODEL="auto"
```

### 5) الرجوع إلى Anthropic المباشر

```bash
unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_MODEL
```

واحذف السطور من `~/.zshrc` أو `~/.bashrc` إن كنت أضفتها هناك.

---

## التحكّم في الضغط (Compression)

الضغط **مُفعّل افتراضيًا**. الوضع الافتراضي هو `RTK → Caveman` مكدّسين.
تحكّم فيه من لوحة التحكم (قسم Compression) أو من الطرفية:

```bash
omniroute compression --help
```

الأوضاع المتاحة: `off` / `lite` / `standard` / `aggressive` / `ultra` / `RTK` /
`stacked`.

**نصيحة عملية:** ابدأ بـ `RTK` فقط. هو يضغط مخرجات الأوامر والاختبارات
والـ git — وهي أكبر مصدر لاستهلاك التوكنز في جلسات البرمجة — دون العبث بصياغة
برومبتك أنت. انتقل إلى `stacked` فقط إذا كانت الجودة ما تزال مقبولة.

---

## متى تستخدمه ومتى لا

| الحالة | الأنسب |
|---|---|
| استكشاف مستودع، قراءة كود، مهام روتينية | ✅ OmniRoute + مزوّد مجاني |
| نفاد حصتك في منتصف العمل | ✅ OmniRoute (تبديل تلقائي) |
| رياضيات، براهين، فيزياء دقيقة | ❌ Anthropic مباشرة |
| كود فيه أسرار أو مفاتيح أو بيانات عملاء | ❌ Anthropic مباشرة |
| نصوص عربية تحتاج صياغة دقيقة | ❌ أو على الأقل `compression off` |
| جلسات claude.ai/code السحابية | لا ينطبق — لا يمرّ عبر جهازك |

---

## مشاكل شائعة

| المشكلة | الحل |
|---|---|
| `omniroute: command not found` | تأكد أن مجلد npm العام ضمن `PATH`: `npm bin -g` |
| Claude Code لا يستجيب بعد التهيئة | تأكد أن `omniroute` يعمل في تبويب آخر، ثم `omniroute doctor` |
| المنفذ 20128 مشغول | `OMNIROUTE_PORT=20200 omniroute` وحدّث `ANTHROPIC_BASE_URL` |
| الردود ضعيفة أو ناقصة | خفّض الضغط إلى `RTK` أو `off`، أو ثبّت نموذجًا محددًا بدل `auto` |
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
