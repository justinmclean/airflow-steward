<\!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

Invocation flags: no_adjust=false

Collected state summary:
- adopted: true
- active_target_ids: ["universal", "claude-code"]
- agent_targets:
    universal: present=true, magpie_count=12, dangling=[]
    claude-code: present=true, magpie_count=12, dangling=[]
    github: present=true, magpie_count=0, dangling=[]  ← directory exists but no symlinks wired
- families.opt_in_present: ["security", "pr-management"]
- families.opt_in_absent: []
- drift: checked=true, in_sync=true
