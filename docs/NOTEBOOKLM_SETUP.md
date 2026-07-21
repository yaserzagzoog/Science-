# ربط Claude Code مع NotebookLM — دليل الإعداد
# Linking Claude Code to NotebookLM — Setup Guide

هذا الدليل مبني على ملف TAHSHR.AI "دليل ربط Claude مع NotebookLM" (نسخة 2026).
الفكرة: **NotebookLM = الذاكرة والمصادر، وClaude = التفكير والتنفيذ والبناء.**

This repo is pre-wired so that Claude Code can talk to NotebookLM through an
MCP server. You only need to run the setup script once **on your own machine**
(the Google login step opens a browser, so it cannot be done in a cloud session).

---

## الطريقة الأولى: بدون MCP (للمبتدئين — لا تحتاج Terminal)

1. افتح [NotebookLM](https://notebooklm.google/) وأنشئ Notebook جديد باسم المشروع.
2. ارفع كل المصادر المهمة: ملفات PDF، روابط، نصوص اجتماعات، ملاحظات، محادثات Claude المهمة.
3. اطلب من NotebookLM تلخيص أهم القرارات والحقائق والتفاصيل.
4. انسخ الملخص وضعه في Claude عند بداية أي محادثة جديدة.
5. بعد كل جلسة مهمة مع Claude، اطلب منه تلخيص ما حصل وأضفه إلى NotebookLM بهذا البرومبت:

```text
Summarize this conversation as a project memory note.
Include:
1. Key decisions made
2. Important context
3. Open questions
4. Next actions
5. Facts Claude should remember next time
Write it in a clean format I can paste into NotebookLM.
```

---

## الطريقة الثانية: الربط المتقدم عبر MCP (مُجهَّز في هذا المستودع)

> **تنبيه أمان:** سيرفرات NotebookLM MCP الحالية مشاريع مجتمعية (Community-built)
> وغير رسمية. راجع الـ README والمشاكل المفتوحة قبل التثبيت، ولا تربط ملفات
> حساسة (جوازات، بطاقات، عقود، أسرار عمل). إذا كان المحتوى حساسًا استخدم حساب
> Google منفصلًا للتجارب.

### الخطوات على جهازك (مرة واحدة فقط)

```bash
# 1) استنسخ هذا المستودع وثبّت السيرفر
git clone https://github.com/yaserzagzoog/science-.git
cd science-
./scripts/setup-notebooklm-mcp.sh

# 2) سجّل الدخول إلى Google/NotebookLM (يفتح المتصفح — سجّل بحسابك وانتظر رسالة النجاح)
cd tools/notebooklm-mcp
uv run notebooklm login

# 3) اختبر تشغيل السيرفر
uv run python server.py     # أوقفه بـ Ctrl+C بعد التأكد أنه يعمل
```

### ربطه مع Claude Code

المستودع يحتوي على ملف `.mcp.json` في الجذر، لذلك عند فتح Claude Code داخل
مجلد المشروع سيكتشف السيرفر تلقائيًا (سيطلب موافقتك أول مرة).

أو أضفه يدويًا على مستوى جهازك:

```bash
claude mcp add notebooklm -- uv --directory <PROJECT_PATH>/tools/notebooklm-mcp run python server.py
claude mcp list
```

### ربطه مع Claude Desktop (اختياري)

أضف إلى ملف إعدادات Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "<UV_PATH>",
      "args": [
        "--directory",
        "<PROJECT_PATH>/tools/notebooklm-mcp",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

ثم أغلق Claude Desktop بالكامل وافتحه من جديد، وابحث عن أيقونة الأدوات (Hammer).

### اختبار الاتصال

داخل Claude Code أو Claude Desktop اكتب:

```text
List my NotebookLM notebooks
```

إذا ظهرت قائمة الـ notebooks فالربط يعمل. إذا لم تظهر، ارجع لخطوة تسجيل
الدخول وتشغيل السيرفر.

---

## كيف تستخدمه كذاكرة لا نهائية؟

قسّم الذاكرة إلى Notebooks منفصلة — لا ترمِ كل شيء في Notebook واحد:

| لكل مشروع | لكل عميل |
|---|---|
| Project Brief | Brand Voice |
| Decisions Log | Offers |
| Meeting Notes | Past Work |
| Research Sources | Client Preferences |
| Content Ideas | Open Tasks |

### برومبتات جاهزة

**استرجاع ذاكرة المشروع (بداية كل جلسة):**

```text
Use NotebookLM to search my project notebook for:
- previous decisions
- important constraints
- client preferences
- unresolved questions
Then summarize only the context I need before we continue working.
```

**تحويل بحث NotebookLM إلى خطة تنفيذ:**

```text
Query my NotebookLM notebook about [TOPIC].
Extract the most important findings, then turn them into:
1. A practical action plan
2. A checklist
3. Risks to watch
4. The next 3 tasks I should do.
```

**تحديث الذاكرة بعد كل جلسة:**

```text
Before we finish, create a NotebookLM memory update.
Include:
- what changed today
- final decisions
- exact wording of important rules
- files or sources to add
- next action list
Format it so I can paste it directly into the project notebook.
```

**مقارنة بين مصادر متعددة:**

```text
Search across my NotebookLM sources about [QUESTION].
Compare what the sources agree on and where they disagree.
Give me a grounded answer with source notes and a clear recommendation.
```

---

## ربط Gmail مع NotebookLM (عبر Claude)

NotebookLM لا يقبل Gmail كمصدر مباشر — لكن **Claude هو الجسر بينهما**، لأن حساب
Gmail مربوط بالفعل مع Claude كـ Connector. المسار هو:

```
Gmail  ──►  Claude (يقرأ ويلخّص)  ──►  NotebookLM (يحفظ كذاكرة)
```

### الطريقة المتاحة الآن (بدون أي إعداد إضافي)

1. اطلب من Claude البحث في بريدك وتلخيص ما يهمك:

```text
Search my Gmail for emails about [PROJECT/CLIENT] from the last month.
Summarize them as a NotebookLM memory note:
- key decisions and agreements
- dates, amounts, and commitments
- open questions and pending replies
- next actions
Format it so I can paste it directly into my project notebook.
```

2. انسخ الناتج وألصقه في NotebookLM كمصدر نصي (Paste text)، أو احفظه في
   Google Doc وأضفه كمصدر — NotebookLM يدعم مصادر Google Drive مباشرة.

### الطريقة الآلية (بعد تثبيت NotebookLM MCP على جهازك)

عندما يكون سيرفر MCP يعمل، يستطيع Claude تنفيذ الطرفين في أمر واحد:

```text
Search my Gmail for this week's emails about [TOPIC],
summarize the important ones as a memory note,
then add that note to my NotebookLM project notebook.
```

### أفكار عملية

- ملخص أسبوعي لرسائل عميل معيّن → Notebook العميل.
- حفظ الاتفاقات والأسعار من البريد في Decisions Log.
- تحويل رسائل الاجتماعات إلى Meeting Notes داخل NotebookLM.
- أرشفة الرسائل المهمة الموسومة بـ label معيّن (مثل "Notes") كذاكرة دائمة.

> **خصوصية:** بريدك قد يحتوي معلومات حساسة. راجع الملخص قبل رفعه إلى
> NotebookLM، ولا ترفع أرقام بطاقات أو بيانات شخصية لأطراف أخرى.

---

## مشاكل شائعة وحلول سريعة

| المشكلة | الحل |
|---|---|
| Claude لا يرى الـ notebooks | أعد تشغيل Claude بالكامل وتأكد من مسار السيرفر في `.mcp.json` |
| فشل تسجيل الدخول | نفّذ `uv run notebooklm login` من جديد وسجّل الدخول في المتصفح |
| السيرفر لا يبدأ | تأكد أن `uv sync` اكتمل وأنك داخل `tools/notebooklm-mcp` |
| النتائج غير دقيقة | نظّم NotebookLM: مصادر أقل وأوضح، أسماء ملفات مفهومة، وملخصات دورية |
| خوف من الخصوصية | استخدم الطريقة اليدوية بدون MCP أو حسابًا منفصلًا للتجارب |

---

## روابط مفيدة

- NotebookLM: <https://notebooklm.google/>
- MCP Intro: <https://modelcontextprotocol.io/docs/getting-started/intro>
- Anthropic MCP announcement: <https://www.anthropic.com/news/model-context-protocol>
- NotebookLM MCP server (community): <https://github.com/alfredang/notebooklm-mcp>
- Alternative NotebookLM Skill: <https://github.com/PleasePrompto/notebooklm-skill>

المشاريع مفتوحة المصدر قد تتغير — اتبع README الأحدث دائمًا.
