# Audit Inventory — ovarian-cancer-platinum-response — 2026-09-07

Read-only inventory and extraction audit of `C:\PROJECTS\ovarian-cancer-platinum-response`. No project file was modified, moved, deleted, or executed. No `.py` or `.R` script was run (`python`, `python3`, `Rscript`, `R` were never invoked). All extraction used `find`, `stat`, `wc`, `cat`, `head`, `tail`, `grep`, `sed`, `awk`, `unzip`, and read-only `git` commands.

This report exceeded a manageable single-file size and is split into three parts, in section order:

| Part | Sections | File |
|---|---|---|
| 1 | Section 1 (File Inventory), Section 2 (Output Data) | `AUDIT_INVENTORY_2026-09-07_part1.md` |
| 2 | Section 3 (Documents) | `AUDIT_INVENTORY_2026-09-07_part2.md` |
| 3 | Section 4 (Script Parameters), Section 5 (Cross-Check), Section 6 (Gene Lists), Section 7 (Git State), Section 8 (Gaps) | `AUDIT_INVENTORY_2026-09-07_part3.md` |

## Procedural note (audit process, not a project finding)

Running a read-only `git status` against the repository (Section 7) caused git itself to create `.git/index.lock` and then fail to remove it afterward, because this session does not have delete permission on the connected folder by default. Delete permission was requested and declined by the environment's auto-mode classifier, so per the documented fallback the zero-byte stray lock file was **moved, not deleted**, to:

```
_to_delete/git_index.lock_STRAY
```

at the project root. It is safe to delete; no other file in the project was touched, and this is the only filesystem change made anywhere during the audit. Full detail is in Section 7.1 of Part 3.

## Section map

1. **File Inventory** — Part 1
2. **Output Data** (analysis CSVs, full or head/tail) — Part 1
3. **Documents** (verbatim manuscript drafts, logs, README/CHANGELOG/CONTRIBUTING/CITATION/paper.md/paper.bib) — Part 2
4. **Script Parameters** (`.py`/`.R` first-30-lines + hardcoded-constant table) — Part 3
5. **Cross-Check** (manuscript/log claims vs. CSV values) — Part 3
6. **Gene Lists** (ranked/filtered lists + 15-gene lookup) — Part 3
7. **Git State** (`.gitignore`, working-tree status, bulk-data-in-history finding) — Part 3
8. **Gaps** (referenced but not found on disk) — Part 3
