<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

## Output format

Return ONLY valid JSON with this structure:

```json
{
  "category": "A" | "B" | "X" | "review" | "unknown",
  "selected_operand": "<SPDX id chosen for an OR expression, else empty>",
  "reason": "<short rationale>"
}
```

`category` is the ASF category the dependency resolves to **after** evaluating
any compound SPDX expression:

- `A` — permissive (allowed).
- `B` — weak reciprocal (allowed in binary/convenience-binary form only, not
  in source releases).
- `X` — forbidden.
- `review` — cannot be auto-decided and must be flagged for PMC review, for
  example a `WITH` exception whose effect on the product depends on usage.
- `unknown` — the license could not be resolved.

For an `A OR B`-style disjunction, classify by the **most permissive** operand
and put the chosen SPDX id in `selected_operand`. For an `AND` conjunction,
classify by the **most restrictive** operand. Leave `selected_operand` empty
when the expression is not a disjunction.

Do not include any text outside the JSON object.
