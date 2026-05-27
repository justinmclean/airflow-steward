# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# SPDX-License-Identifier: Apache-2.0
"""Pure helper functions for render.py — no file I/O, no global state."""

import calendar
import datetime as dt
import statistics


# ---------------------------------------------------------------------------
# YAML loader
# ---------------------------------------------------------------------------

try:
    import yaml  # type: ignore

    def yaml_load(text: str):
        return yaml.safe_load(text)

except ImportError:
    def yaml_load(text: str):
        return _minimal_yaml_load(text)


def _minimal_yaml_load(text: str):
    """Tiny YAML subset parser sufficient for default-config.yaml.

    Supports: nested block mappings, block sequences, inline flow lists,
    string scalars, integers, floats, booleans, null. No anchors.
    """
    lines = []
    for raw in text.splitlines():
        in_q = None
        out = []
        i = 0
        while i < len(raw):
            ch = raw[i]
            if in_q:
                out.append(ch)
                if ch == '\\' and i + 1 < len(raw):
                    out.append(raw[i + 1])
                    i += 2
                    continue
                if ch == in_q:
                    in_q = None
                i += 1
                continue
            if ch in ('"', "'"):
                in_q = ch
                out.append(ch)
                i += 1
                continue
            if ch == '#':
                break
            out.append(ch)
            i += 1
        line = ''.join(out).rstrip()
        if line.strip():
            lines.append(line)

    def indent_of(s):
        return len(s) - len(s.lstrip(' '))

    def scalar(s):
        s = s.strip()
        if not s:
            return None
        if s.lower() in ('null', '~'):
            return None
        if s.lower() == 'true':
            return True
        if s.lower() == 'false':
            return False
        if s.startswith('"') and s.endswith('"') and len(s) >= 2:
            return s[1:-1].encode().decode('unicode_escape')
        if s.startswith("'") and s.endswith("'") and len(s) >= 2:
            return s[1:-1]
        if s.startswith('[') and s.endswith(']'):
            inner = s[1:-1].strip()
            if not inner:
                return []
            return [scalar(x) for x in _split_flow_list(inner)]
        try:
            if '.' in s or 'e' in s or 'E' in s:
                return float(s)
            return int(s)
        except ValueError:
            return s

    def _split_flow_list(inner):
        parts = []
        cur = []
        in_q = None
        depth = 0
        for ch in inner:
            if in_q:
                cur.append(ch)
                if ch == in_q:
                    in_q = None
                continue
            if ch in ('"', "'"):
                in_q = ch
                cur.append(ch)
                continue
            if ch == '[':
                depth += 1
                cur.append(ch)
                continue
            if ch == ']':
                depth -= 1
                cur.append(ch)
                continue
            if ch == ',' and depth == 0:
                parts.append(''.join(cur).strip())
                cur = []
                continue
            cur.append(ch)
        if cur:
            parts.append(''.join(cur).strip())
        return parts

    def parse_block(idx, base_indent):
        if idx >= len(lines):
            return None, idx
        first = lines[idx]
        ind = indent_of(first)
        if ind < base_indent:
            return None, idx
        if first.lstrip().startswith('- '):
            return parse_seq(idx, ind)
        return parse_map(idx, ind)

    def parse_map(idx, base_indent):
        out = {}
        while idx < len(lines):
            line = lines[idx]
            ind = indent_of(line)
            if ind < base_indent:
                break
            if ind > base_indent:
                break
            stripped = line.strip()
            if stripped.startswith('- '):
                break
            if ':' not in stripped:
                idx += 1
                continue
            key, _, rest = _split_key_value(stripped)
            rest = rest.strip()
            idx += 1
            if rest == '' or rest is None:
                if idx < len(lines) and indent_of(lines[idx]) > base_indent:
                    child, idx = parse_block(idx, indent_of(lines[idx]))
                    out[key] = child
                else:
                    out[key] = None
            else:
                out[key] = scalar(rest)
        return out, idx

    def _split_key_value(stripped):
        in_q = None
        for i, ch in enumerate(stripped):
            if in_q:
                if ch == in_q:
                    in_q = None
                continue
            if ch in ('"', "'"):
                in_q = ch
                continue
            if ch == ':':
                key = stripped[:i].strip()
                rest = stripped[i + 1:]
                if (key.startswith('"') and key.endswith('"')) or (
                    key.startswith("'") and key.endswith("'")
                ):
                    key = key[1:-1]
                return key, ':', rest
        return stripped, None, ''

    def parse_seq(idx, base_indent):
        out = []
        while idx < len(lines):
            line = lines[idx]
            ind = indent_of(line)
            if ind < base_indent:
                break
            if ind > base_indent:
                break
            stripped = line.strip()
            if not stripped.startswith('- '):
                break
            after_dash = stripped[2:].rstrip()
            item_inner_indent = base_indent + 2
            idx += 1
            if after_dash == '':
                if idx < len(lines) and indent_of(lines[idx]) > base_indent:
                    child, idx = parse_block(idx, indent_of(lines[idx]))
                    out.append(child)
                else:
                    out.append(None)
                continue
            if ':' in after_dash and not (
                after_dash.startswith('"') or after_dash.startswith("'")
            ):
                key, _, rest = _split_key_value(after_dash)
                rest = rest.strip()
                item = {}
                if rest == '':
                    if idx < len(lines) and indent_of(lines[idx]) > item_inner_indent:
                        child, idx = parse_block(idx, indent_of(lines[idx]))
                        item[key] = child
                    else:
                        item[key] = None
                else:
                    item[key] = scalar(rest)
                while idx < len(lines):
                    nline = lines[idx]
                    nind = indent_of(nline)
                    if nind < item_inner_indent:
                        break
                    if nind > item_inner_indent:
                        break
                    nstripped = nline.strip()
                    if nstripped.startswith('- '):
                        break
                    if ':' not in nstripped:
                        idx += 1
                        continue
                    nkey, _, nrest = _split_key_value(nstripped)
                    nrest = nrest.strip()
                    idx += 1
                    if nrest == '':
                        if idx < len(lines) and indent_of(lines[idx]) > item_inner_indent:
                            child, idx = parse_block(idx, indent_of(lines[idx]))
                            item[nkey] = child
                        else:
                            item[nkey] = None
                    else:
                        item[nkey] = scalar(nrest)
                out.append(item)
            else:
                out.append(scalar(after_dash))
        return out, idx

    val, _ = parse_block(0, 0)
    return val


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def deep_merge(base, overlay):
    """Deep-merge overlay into base. Lists are REPLACED (not concatenated)."""
    if overlay is None:
        return base
    if not isinstance(base, dict) or not isinstance(overlay, dict):
        return overlay
    out = dict(base)
    for k, v in overlay.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


# ---------------------------------------------------------------------------
# Datetime helpers
# ---------------------------------------------------------------------------

def parse_dt(s):
    if not s:
        return None
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))


# ---------------------------------------------------------------------------
# Bucket abstraction
# ---------------------------------------------------------------------------

def month_of(d):
    return d.year, d.month


def quarter_of(d):
    return d.year, (d.month - 1) // 3 + 1


def month_label(y, m):
    return f"{y}-{m:02d}"


def quarter_label(y, q):
    return f"{y}-Q{q}"


def month_end(y, m):
    last_day = calendar.monthrange(y, m)[1]
    return dt.datetime(y, m, last_day, 23, 59, 59, tzinfo=dt.timezone.utc)


def quarter_end(y, q):
    last_month = q * 3
    last_day = calendar.monthrange(y, last_month)[1]
    return dt.datetime(y, last_month, last_day, 23, 59, 59, tzinfo=dt.timezone.utc)


def iter_months(y0, m0, y1, m1):
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        yield y, m
        m += 1
        if m == 13:
            m = 1
            y += 1


def iter_quarters(y0, q0, y1, q1):
    y, q = y0, q0
    while (y, q) <= (y1, q1):
        yield y, q
        q += 1
        if q == 5:
            q = 1
            y += 1


# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------

def mean_or_none(xs):
    return round(statistics.mean(xs), 2) if xs else None


# ---------------------------------------------------------------------------
# JavaScript serialisation helpers
# ---------------------------------------------------------------------------

def js_array(xs, fmt_null='null'):
    parts = []
    for x in xs:
        if x is None:
            parts.append(fmt_null)
        elif isinstance(x, float):
            parts.append(f"{x:.2f}" if not (x == int(x)) else f"{int(x)}")
        else:
            parts.append(str(x))
    return '[' + ', '.join(parts) + ']'


def js_quotes(xs):
    return '[' + ', '.join(f'"{x}"' for x in xs) + ']'


def milestone_x(milestone_date: str, buckets_mode: str = 'monthly') -> str:
    """Map a milestone date (YYYY-MM-DD) onto a bucket-axis label."""
    y = int(milestone_date[:4])
    mo = int(milestone_date[5:7])
    if buckets_mode == 'monthly':
        return f"{y}-{mo:02d}"
    return f"{y}-Q{(mo - 1) // 3 + 1}"


# ---------------------------------------------------------------------------
# Predicate evaluator
# ---------------------------------------------------------------------------

def eval_predicate(pred, ctx, scope_labels=frozenset()):
    """Evaluate a category predicate against a snapshot context.

    ctx keys:
        labels (set), is_open (bool), state_reason (str|None),
        pr_merged_by_snapshot (bool).
    scope_labels: the set of scope label strings from config.
    """
    if not isinstance(pred, dict):
        return False
    for key, val in pred.items():
        if key == 'any_of':
            if not any(eval_predicate(p, ctx, scope_labels) for p in val):
                return False
        elif key == 'all_of':
            if isinstance(val, list):
                if not all(eval_predicate(p, ctx, scope_labels) for p in val):
                    return False
            elif isinstance(val, dict):
                if not eval_predicate(val, ctx, scope_labels):
                    return False
            else:
                return False
        elif key == 'state':
            want_open = (val == 'open')
            if ctx['is_open'] != want_open:
                return False
        elif key == 'state_reason':
            if ctx['state_reason'] != val:
                return False
        elif key == 'any_label':
            if not any(lbl in ctx['labels'] for lbl in val):
                return False
        elif key == 'all_labels':
            if not all(lbl in ctx['labels'] for lbl in val):
                return False
        elif key == 'not_label':
            if val in ctx['labels']:
                return False
        elif key == 'not_any_label':
            if any(lbl in ctx['labels'] for lbl in val):
                return False
        elif key == 'no_scope_label':
            has_scope = bool(ctx['labels'] & scope_labels)
            if val and has_scope:
                return False
            if not val and not has_scope:
                return False
        elif key == 'has_scope_label':
            has_scope = bool(ctx['labels'] & scope_labels)
            if val and not has_scope:
                return False
            if not val and has_scope:
                return False
        elif key == 'pr_merged_by_snapshot':
            if val and not ctx['pr_merged_by_snapshot']:
                return False
            if not val and ctx['pr_merged_by_snapshot']:
                return False
        else:
            return False
    return True


# ---------------------------------------------------------------------------
# Bot-comment filter
# ---------------------------------------------------------------------------

def is_bot_body(body: str, prefixes: tuple = ()) -> bool:
    if not body:
        return False
    b = body.lstrip()
    for p in prefixes:
        if b.startswith(p):
            return True
    return False
