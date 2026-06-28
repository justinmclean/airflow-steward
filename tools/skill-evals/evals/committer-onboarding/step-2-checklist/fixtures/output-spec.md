# Step 2 output spec

The model must produce the correct checklist variant and a
welcome announcement draft, shaped by the resolved governance model.

## Fields present in all cases

- `welcome_draft_present`: boolean
- `welcome_no_unresolved_placeholders`: boolean

## `asf-pmc` model fields (default)

- `checklist_variant`: "new-committer" | "committer-to-pmc" | "direct-to-pmc"
- `has_whimsy_step`: boolean — Whimsy roster update present in checklist
- `whimsy_url_correct`: boolean
  - incubating: contains "roster/ppmc/<podling>"
  - TLP: references committee-info.txt or "roster/committee/<podling>"
- `whimsy_url_contains`: string — the substring the Whimsy URL must include
  (the PPMC vs. PMC discriminator: e.g. `roster/ppmc` for incubating,
  `roster/committee` for TLP)
- `has_github_step`: boolean — GitHub org invite present in checklist
- `github_step_held_when_login_unknown`: boolean — true when GitHub login
  was not provided and the skill asks for it rather than guessing
- `secretary_request_present`: boolean — secretary account-request step included

## `github-codeowners` model fields

- `governance_model`: "github-codeowners"
- `has_github_team_invite_step`: boolean — checklist includes the `gh api` team invite command
- `github_team_slug_correct`: boolean — team slug from config appears in the command
- `has_codeowners_pr_step`: boolean — checklist includes opening a CODEOWNERS PR (only when codeowners_file is not null)
- `has_whimsy_step`: boolean — must be false (no Whimsy for non-ASF governance)
- `secretary_request_present`: boolean — must be false

## `maintainer-roster` model fields

- `governance_model`: "maintainer-roster"
- `has_roster_file_update_step`: boolean — checklist includes updating the roster file
- `roster_pr_step_present`: boolean — checklist includes opening a PR for the roster update
- `has_whimsy_step`: boolean — must be false
- `has_github_team_invite_step`: boolean — must be false
- `secretary_request_present`: boolean — must be false
