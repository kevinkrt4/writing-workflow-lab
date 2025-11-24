# 🧭 Markdown Cheat Sheet

A quick reference guide for writing Markdown. Use this as a pocket manual when formatting text, notes, or web content.

---

## 📑 Headings

```md
# H1 Heading
## H2 Heading
### H3 Heading
#### H4 Heading
```

**Rendered:**
# H1 Heading
## H2 Heading
### H3 Heading
#### H4 Heading

---

## ✍️ Text Formatting

```md
*Italic* or _Italic_
**Bold** or __Bold__
***Bold and Italic***
`Inline code`
```

**Rendered:**
*Italic* or _Italic_  
**Bold** or __Bold__  
***Bold and Italic***  
`Inline code`

---

## 🧾 Paragraphs and Line Breaks

Separate paragraphs with a blank line:

```md
This is paragraph one.

This is paragraph two.
```

Add two spaces at the end of a line to force a line break:

```md
First line␠␠
Second line
```

---

## 📋 Lists

### Unordered List
```md
- Apples
- Bananas
  - Sub-item
```

**Rendered:**
- Apples
- Bananas
  - Sub-item

### Ordered List
```md
1. First item
2. Second item
   1. Nested item
```

**Rendered:**
1. First item
2. Second item
   1. Nested item

---

## 🔗 Links and Images

### Links
```md
[OpenAI](https://www.openai.com)
```

**Rendered:**
[OpenAI](https://www.openai.com)

### Images
```md
![Alt text](https://via.placeholder.com/100)
```

**Rendered:**
![Alt text](https://via.placeholder.com/100)

---

## 💬 Blockquotes

```md
> This is a quote.
>> Nested quote.
```

**Rendered:**
> This is a quote.  
>> Nested quote.

---

## 💻 Code Blocks

### Inline Code
````md
Use `print("Hello, World!")` to print.
````

**Rendered:** Use `print("Hello, World!")` to print.

### Code Block
````md
```python
print("Hello, World!")
```
````

**Rendered:**
```python
print("Hello, World!")
```

---

## ✅ Task Lists

```md
- [x] Completed task
- [ ] Pending task
- [ ] Another pending item
```

**Rendered:**
- [x] Completed task
- [ ] Pending task
- [ ] Another pending item

---

## 📊 Tables

```md
| Name | Role | Status |
|------|------|--------|
| Alice | Writer | Active |
| Bob | Editor | Inactive |
```

**Rendered:**
| Name | Role | Status |
|------|------|--------|
| Alice | Writer | Active |
| Bob | Editor | Inactive |

---

## 🧩 Horizontal Rule

```md
---
```

**Rendered:**
---

---

## 🪶 Escaping Special Characters

Use a backslash `\` before symbols to display them literally:
```md
\*Not italicized\*
```
**Rendered:** \*Not italicized\*

---

## 🧠 Quick Summary

| Action | Syntax | Example |
|--------|---------|----------|
| Heading | `#` to `####` | `## Section` |
| Bold | `**text**` | **Bold** |
| Italic | `*text*` | *Italic* |
| Link | `[text](url)` | [Example](https://example.com) |
| Image | `![alt](url)` | ![Sample](https://via.placeholder.com/50) |
| List | `- item` or `1. item` | `- apple` |
| Code | `` `code` `` | `print()` |
| Blockquote | `> quote` | > quote |
| Table | Pipes + hyphens | `| A | B |` |
| Task List | `- [x] done` | - [x] done |

---

**Tip:** In VS Code, press `⌘ Shift V` (Mac) or `Ctrl Shift V` (Windows/Linux) to preview Markdown rendering.


---

## ⚙️ VS Code Tip: Indentation for Lists

To ensure lists render correctly, use **two spaces** for each indent level (not tabs). Tabs can render inconsistently across Markdown viewers.

Example:
```md
- Task 1
  - Subtask 1.1
    - Subtask 1.1.1
```

**Rendered:**
- Task 1  
  - Subtask 1.1  
    - Subtask 1.1.1  

### Configure VS Code to Use Spaces Instead of Tabs
1. Open **Command Palette** → search for `Indentation`.
2. Choose **Convert Indentation to Spaces**.
3. In Settings, set:
   - `Editor: Insert Spaces` → **true**
   - `Editor: Tab Size` → **2**

This ensures that pressing the Tab key inserts two spaces, keeping your lists properly aligned across all Markdown renderers.
