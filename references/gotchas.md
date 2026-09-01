# Key Gotchas

## Tag & annotation behavior

- `item_update` replaces tags (not incremental) when using the `tags` field inside `items`. Since each item gets its full fresh tag set in the same call, replacement is the desired behavior — but this means any pre-existing tags are discarded. See the authorization gate in SKILL.md before writing.
- Do **not** use `item_add_comment` for notes — it creates spatial comments requiring coordinates. For text notes use the `annotation` field via `item_update`.
- The `annotation` field is a single text block. Use the five-field labeled template (设计类型 / 结构 / 视觉 / 用途 / 参考价值, one field per line) from `references/templates.md` so every batch is consistent. Do **not** invent other field names or join the fields into one line.

## Naming & paths

- File paths in Eagle contain the item name, so renaming also updates the underlying file path.

## Connection

- The `eagle-mcp` server (WorkBuddy mcp.json uses `command: node` + `mcp-proxy.js`, i.e. a **stdio** MCP server; the proxy internally bridges to Eagle's HTTP/SSE endpoint at `localhost:41596`) requires Eagle to be running. If tools return connection errors, check Eagle is open first.

## Call shape (the only common failure mode)

- **Array params: pass plain JSON arrays, never wrap in `{item: …}`.** The WorkBuddy MCP wrapper does **no** transformation — it validates your `params` verbatim against the server's JSON schema. So `items` MUST be `["…"]` / `[{…}, {…}]`, and `ids`/`tags` MUST be `["…"]`. Wrapping like `{item: {...}}` or `{item: [...]}` violates `additionalProperties:false` / `type:array` and returns `"/items: must be array"` (or `"/ids: must be array"`). This is a **call-shape mistake, not a tool-chain bug**.

## Bulk-apply gotchas (learned operating at 100+ items)

- **The dry-run manifest's `oldName` field is review-only.** `scripts/build_dryrun.py` writes `oldName` into each entry so the user can see what changes, but `scripts/apply_eagle_batch.py` ignores it (Eagle derives the current name from the item id). The user edits the manifest to skip/fix entries; only the entries left in the file are applied.
- **Eagle's local REST API (`http://localhost:41595`) `item/update` CANNOT rename.** It accepts only a **single-item** body (`{"id":..., "name":..., "tags":[...], "annotation":...}` — NOT an `items` array) and, worse, it **silently ignores the `name` field** (only `tags`/`annotation` get written). Renaming + batching therefore REQUIRES the MCP `item_update` tool (via `mcp-proxy.js` → Eagle SSE), which supports the `items` array and does rename. Verify a rename actually stuck by reading the item back.
- **Bulk-driving the MCP without pasting huge JSON into the chat:** `Read` truncates any single line >2000 chars, so a 100-item payload file can't be inlined via Read→DeferExecuteTool. Instead, run the bundled `scripts/apply_eagle_batch.py`, which spawns `node <mcp-proxy.js>`, performs `initialize` → `notifications/initialized` → `tools/call(item_update, {items:[...]})` over JSON-RPC, and feeds the payload from a file. Usage: `python3 scripts/apply_eagle_batch.py --tool item_update --payload /path/to/payload.json [--batch 20]`. The payload file is `{ "items": [ { "id", "name", "tags", "annotation" }, ... ] }`. It auto-detects the proxy path (override with `--proxy`), chunks into batches, prints each batch's `isError` + result text, and warns when the confirmed count ≠ requested count. Alternatively, issue several `DeferExecuteTool` `item_update` calls of ~10–20 items each.
- **Never hand-paste a 50+ ID array into a `DeferExecuteTool` `item_get`/`item_update` call.** Transcribing long ID lists inline reliably drops entries — observed: a 50-ID array was pasted as 47, silently leaving 3 items unprocessed (the tool returns only the count it received, so the gap is invisible). Always drive bulk reads/writes through `scripts/apply_eagle_batch.py` reading IDs from a payload file, and re-read the items afterwards to confirm the returned count equals the requested count. This is the only reliable way to guarantee "no omissions" at scale.
- **`isUntagged` only checks tags, NOT folder membership.** Untagged assets can still live inside folders. When you `item_update`, **omit the `folders` key entirely** for every item unless you intend to move it — Eagle preserves existing folder membership when `folders` is absent. (Confirmed in practice: a meaningful share of "untagged" items were already inside folders; omitting `folders` kept them put.)

## Non-multimodal fallback (metadata-driven)

- Image visibility is guarded by the mandatory Step 0a check: if the current model cannot see images (e.g. Read returns `Content filtered` or explicitly says it cannot recognize the picture), Step 0a will **terminate** the whole flow immediately and prompt the user to switch to a multimodal model, so normally the batch flow is never entered.
- If you still want a fallback for non-multimodal environments, use the **metadata-driven** approach: pull each item's real `palettes` (dominant colors + ratios), `width`/`height` (→ landscape/portrait/square), and `url` (source) via `item_get` with `fullDetails:true`, then derive name/tags/annotation from those signals. Mark annotations as "inferred" so the basis is transparent.
