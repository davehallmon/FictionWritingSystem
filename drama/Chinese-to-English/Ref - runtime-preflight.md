# Project Location and Safe Writes

## Locate the Project

Prefer the project path supplied by the user. When no project exists, an independent task may be completed directly in a user-specified directory. When project configuration is required, run:

```bash
python3 <core>/scripts/project_tool.py init <project> --title "项目名"
```

This documentation uses `python3` throughout. In a native Windows environment where that command is unavailable, use `py -3` or `python`. Suite scripts, including the Dashboard, run on macOS, Linux, WSL, and native Windows.

Always write creative documents to `剧集/<EP>/`. Read only the direct inputs required by the current task; do not scan the entire project for upstream material to reconstruct.

## Write Discipline

- Write the five Markdown creative documents directly. When modifying them, preserve unaffected content and stable visible IDs.
- Input directories, hidden runtime directories, production outputs, and credentials are not creative manuscript content; do not copy them into prompts.
- Write text through a temporary file followed by an atomic replacement. If an external edit occurs, reread the file before proceeding; never overwrite it silently.
- The Dashboard only displays and edits project files. It does not provide creative routing or production authorization.
- External production remains under `$short-drama-produce`, which previews the exact task and executes only after explicit confirmation.

For output language, stable IDs, and trust boundaries, see [Contract and Ownership](contract-and-ownership.md).
