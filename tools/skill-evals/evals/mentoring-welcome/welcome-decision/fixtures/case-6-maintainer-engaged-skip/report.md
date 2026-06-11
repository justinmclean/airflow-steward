Thread: PR #4703 — "Add support for async task callbacks"
ThreadType: pr
authorAssociation: FIRST_TIME_CONTRIBUTOR
Author: newcomer-pr-author
PriorWelcomePosted: false
MaintainerEngaged: true
OutOfScopeTopics: [security, CVE, deprecation, licensing, architecture]

Opening body:
"Adds async support for task callbacks so long-running callbacks do
not block the scheduler loop. Introduces a new `async_callback` param
on the BaseOperator."
