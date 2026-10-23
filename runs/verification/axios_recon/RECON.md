# axios/axios (repo_id 23088740) — Target-selection recon

Date: 2026-10-23. Environment: Node v24.16.0 (bundled undici 7.25.0), npm 11.13.0, git 2.43.0.
Network used only for fetching advisories / cloning / `npm install`; every reproduction below is
127.0.0.1-local and needs no external network.

## 0. Bottom line

**Recommended tag: `v1.19.0`**

| Field | Value |
|---|---|
| Tag object type | **lightweight** (`git cat-file -t v1.19.0` → `commit`, no `^{}` peeled ref) |
| Tag ref | `refs/tags/v1.19.0` → `311fcc5c8d989b7248f05d390bb83bfbfb009977` |
| Commit | `311fcc5c8d989b7248f05d390bb83bfbfb009977` |
| Tree | `e235490f75463ad553dca06d75427aa17c1ab647` |
| Commit date (committer) | `2026-07-22T19:26:22+02:00` |
| Subject | `chore(release): prepare release 1.19.0 (#11095)` |
| package.json version | 1.19.0 |
| Fixed release | `v1.20.0` (lightweight, `84a9f3b9a4f3244b8c8e818f557d64c7b964fb25`, tree `53995167a1c7575e34e6c5b38c9c164966bc5424`, `2026-08-19T17:53:46+02:00`, `chore(release): prepare release 1.20.0 (#11152)`) |

Why it qualifies:

* (a) Inside the affected range of **all 12** advisories in the CVE-2026-101898…101909 batch
  returned by OSV for `axios@1.19.0`, including all four lead candidates.
* (b) Stable release, tagged 2026-07-22 (well after 2022-10-23), and the newest stable tag
  strictly below the fix release (`v1.20.0` is the newest tag in the repo; `main`/`v1.x` HEAD is a
  **1.21.0 release-prep commit `e6b79d9c` but no `v1.21.0` tag exists yet**). No 1.19.x follow-up tag.
* (c) Fix commit `d19040b` is an ancestor of `v1.20.0` and of no other tag (`git tag --contains`
  returns only `v1.20.0`); `v1.20.0` is clean for the whole batch (OSV query for 1.20.0 → 0 vulns).
* (d) Real in-process local repro verified for **CVE-2026-101899, 101900, 101904, 101907**, plus
  101908 via a custom `env.fetch`; see §6. Two caveats on 101905/101908 are in §8.

## 1. Advisory verification (OSV / NVD / GitHub)

Fetched: `https://api.osv.dev/v1/vulns/<GHSA>`, `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=<CVE>`,
and the GitHub advisory HTML page (GitHub REST API was rate-limited: HTTP 403 for the shared egress IP).

### 1.1 The four lead candidates

| GHSA / CVE | OSV SEMVER range | NVD description range | GHSA page affected → patched | CWE (OSV / NVD) | Severity (OSV `database_specific`) | CVSS v4 |
|---|---|---|---|---|---|---|
| GHSA-vh66-26gq-q6x8 / CVE-2026-101908 | 1.7.0 → fixed 1.20.0 | "From 1.7.0 until 1.20.0" | `>=1.7.0` → `>=1.20.0` | CWE-1321 / CWE-1321 (GHSA page lists none) | MODERATE | 6.9 `AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:H/SA:N` |
| GHSA-44g4-m2mj-wpvx / CVE-2026-101899 | 1.15.0 → fixed 1.20.0 | "From 1.15.0 until 1.20.0" | `>=1.15.0` → `>=1.20.0` | CWE-693 / CWE-693 | MODERATE | 6.9 `…/SC:H/SI:N/SA:N` |
| GHSA-4hqw-qxg8-jxx2 / CVE-2026-101900 | 1.12.0 → fixed 1.20.0 | "From 1.12.0 until 1.20.0" | `>=1.12.0` → `>=1.20.0` | CWE-1321,693,74 / CWE-74,693,1321 | MODERATE | 6.9 `…/SC:L/SI:H/SA:N` |
| GHSA-j8rh-479h-cp32 / CVE-2026-101904 | 1.0.0 → fixed 1.20.0 | "From 1.0.0 until 1.20.0" | `>=1.0.0` → `>=1.20.0` | CWE-1321,74 / CWE-74,1321 | MODERATE | 6.9 `…/SC:L/SI:H/SA:N` |

All four reference the same fix: PR `#11141`, commit `d19040bda7a8be2f82c3c6e1a5bc03917daee39a`,
release `v1.20.0`. NVD `vulnStatus` is **"Awaiting Analysis"** for all four (CVSS/SSVC sourced from
`security-advisories@github.com`; SSVC exploitation = `poc`). NVD has **no CPE configurations** for
any of these CVEs, so NVD contributes no machine-readable range.

### 1.2 The two "rejected" siblings from the catalog — NOT withdrawn

| GHSA / CVE | OSV range | NVD | GHSA page | Verdict |
|---|---|---|---|---|
| GHSA-m8m8-qj5v-23w3 / CVE-2026-101905 | 1.15.2 → fixed 1.20.0 | status "Awaiting Analysis"; full description; CWE-441,1321; 7.6 HIGH; SSVC automatable=yes | live, "High 7.6", affected `>=1.15.2`, patched `>=1.20.0`, published Sep 16 2026 | **active advisory, not rejected** |
| GHSA-r4gj-5m52-g5wh / CVE-2026-101907 | 1.17.0 → fixed 1.20.0 | status "Awaiting Analysis"; full description; CWE-441,601; 7.0 HIGH | live, "High 7.0", affected `1.17.0`, patched `>=1.20.0`, published Sep 16 2026 | **active advisory, not rejected** |

Neither OSV record has a `withdrawn` field, and neither GitHub page carries a withdrawal notice.
**The catalog's "rejected" marking for CVE-2026-101907 and CVE-2026-101905 is wrong.** They are the
two *highest-severity* items in the batch (7.0 and 7.6, both High).

### 1.3 The full batch affecting v1.19.0 (OSV query for `axios@1.19.0`)

12 advisories, all fixed in 1.20.0 for the 1.x line (101902 and 101909 additionally carry 0.x ranges
fixed in 0.34.0):

CVE-2026-101898 (HTTP/2 DNS-lookup/proxy bypass, CWE-918, High, 1.13.0→1.20.0),
101899 (NO_PROXY CIDR ignored), 101900 (FormData getHeaders), 101901 (HTTP/2 unhandled `error` DoS,
CWE-400, High, 1.13.0→1.20.0), 101902 (inherited `Object.prototype.method`, 1.0.0→1.20.0),
101903 (fromDataURI ReDoS, CWE-1333, High, 1.16.1→1.20.0), 101904 (interceptor headers),
101905 (createConnection), 101906 (shouldBypassProxy O(N²) ReDoS, CWE-1333/400, High, 1.15.0→1.20.0),
101907 (maxRedirects 0), 101908 (fetchOptions), 101909 (toFormData options, 1.15.1→1.20.0).

OSV query for `axios@1.20.0` returns **0** vulnerabilities.

### 1.4 Recorded disagreements

1. **Catalog vs reality:** 101905/101907 are live, High-severity, non-withdrawn advisories (catalog
   said "rejected"). This also means v1.19.0 is in the affected range of two High-severity issues,
   not just Moderate ones.
2. **Publication dates:** GitHub advisory pages say **Sep 16, 2026**; OSV `published` is
   **2026-09-30T15:12–15:35Z**; NVD published **2026-09-28T18:17Z** for 101900/101904/101905/101907/101908
   but **2026-10-13T16:17Z** for 101899. OSV's `nvd_published_at` is `null` for 101899 even though NVD
   now has the record.
3. **Range notation:** GitHub pages expose only `>=introduced` with `>=1.20.0` patched (no upper
   bound); OSV encodes `introduced` + `fixed 1.20.0`; NVD text says "From X until 1.20.0". For
   101907 the GitHub affected field is the literal `1.17.0` (single version) while OSV/NVD mean
   `>=1.17.0`. Semantically consistent, textually different.
4. **CWE:** GHSA-vh66 page lists no CWE, OSV/NVD say CWE-1321. 101900/101904 have multi-CWE lists in
   different orders.
5. **NVD analysis state:** all six are "Awaiting Analysis"; NVD descriptions are copied from the
   GitHub advisory and NVD has no CPE ranges. OSV/GHSA is the only authoritative range source here.
6. **NVD wording vs code for 101899:** NVD says CIDR form is treated "as a textual hostname suffix";
   in v1.19.0 `shouldBypassProxy` does exact match / dot-suffix match only, so a CIDR entry like
   `10.0.0.0/8` simply never matches. Same security effect, imprecise wording.

## 2. Release tag enumeration (independent)

`git ls-remote --tags` → 243 refs, 147 unique tags; full clone into `/tmp/axios_recon/axios`
(default branch `v1.x`). Stable tags from 1.12.0 to 1.20.0:

| Tag | Tag type | Peeled commit | Commit date | Subject |
|---|---|---|---|---|
| v1.12.0 | annotated | 0d8ad6e1de | 2025-09-11T21:32:15+02:00 | chore(release): v1.12.0 (#7013) |
| v1.12.1 | annotated | 3cac78c2de | 2025-09-12T17:18:39+03:00 | chore(release): v1.12.1 (#7021) |
| v1.12.2 | annotated | e5a33366d7 | 2025-09-14T15:58:39+03:00 | chore(release): v1.12.2 (#7031) |
| v1.13.0 | annotated | 9ead04d8ab | 2025-10-27T18:07:18+02:00 | [Release] v1.13.0 (#7189) |
| v1.13.1 | annotated | 1ef8e7218b | 2025-10-28T20:54:35+02:00 | chore(release): v1.13.1 (#7194) |
| v1.13.2 | annotated | 08b84b52d5 | 2025-11-04T22:00:13+02:00 | chore(release): v1.13.2 (#7207) |
| v1.13.3 | annotated | ab06109b40 | 2026-01-20T19:47:13+02:00 | chore(release): v1.13.3 (#7335) |
| v1.13.4 | lightweight | 9336cf9a33 | 2026-01-27T20:13:03+02:00 | chore(release): prepare release 1.13.4 (#7353) |
| v1.13.5 | lightweight | 29f75425f0 | 2026-02-08T12:53:34+02:00 | chore(release): prepare release 1.13.5 (#7379) |
| v1.13.6 | lightweight | 7108c8877f | 2026-02-27T17:28:22+02:00 | chore(release): prepare release 1.13.6 (#7446) |
| v1.14.0 | lightweight | 46bee3dea7 | 2026-03-27T20:54:05+02:00 | chore(release): prepare release 1.14.0 (#10563) |
| v1.15.0 | lightweight | 772a4e54ec | 2026-04-07T18:03:51+02:00 | chore(release): prepare release 1.15.0 (#10671) |
| v1.15.1 | lightweight | ac42446be5 | 2026-04-19T18:51:43+02:00 | chore(release): prepare release 1.15.1 (#10767) |
| v1.15.2 | lightweight | 582934382e | 2026-04-21T19:45:22+02:00 | chore(release): prepare release 1.15.2 (#10789) |
| v1.16.0 | lightweight | df53d7dd99 | 2026-05-02T13:49:29+02:00 | chore(release): prepare release 1.16.0 (#10834) |
| v1.16.1 | lightweight | 1337d6b537 | 2026-05-13T18:11:40+02:00 | chore(release): prepare release 1.16.1 (#10877) |
| v1.17.0 | lightweight | 4306df21e8 | 2026-06-01T20:15:44+02:00 | chore: add fun 88 sponsorship (tag commit; package.json=1.17.0) |
| v1.18.0 | lightweight | 2d06f96e86 | 2026-06-12T08:38:08+02:00 | chore(release): prepare release 1.18.0 (#11003) |
| v1.18.1 | lightweight | a209bfb1e5 | 2026-06-21T19:14:40+02:00 | chore(release): prepare release 1.18.1 (#11027) |
| **v1.19.0** | **lightweight** | **311fcc5c8d** | **2026-07-22T19:26:22+02:00** | **chore(release): prepare release 1.19.0 (#11095)** |
| **v1.20.0** | **lightweight** | **84a9f3b9a4** | **2026-08-19T17:53:46+02:00** | **chore(release): prepare release 1.20.0 (#11152)** |

* `v1.20.0` exists and is the fixed release (contains the fix commit; OSV query for 1.20.0 → 0 vulns).
* No tag above 1.20.0 exists (`git tag --list 'v1.2*'` → … v1.20.0 only). Repo HEAD is
  `e6b79d9c chore(release): prepare release 1.21.0 (#11346)` on `v1.x`, untagged.
* Version-in-range check for v1.19.0: 1.19.0 ≥ all introduced versions (max introduced is 1.17.0)
  and < 1.20.0, so it is inside **all 12** ranges.

## 3–4. Vulnerable code at `v1.19.0` (311fcc5c)

Line numbers are from `git show v1.19.0:<path> | nl -ba`.

### 4.1 Fetch adapter prototype-pollution gadget — CVE-2026-101908 / GHSA-vh66 (`lib/adapters/fetch.js`)

```js
196   let { url, method, data, signal, cancelToken, timeout,
...
208     fetchOptions,
209     maxContentLength,
210     maxBodyLength,
211   } = resolveConfig(config);          // NOTE: no maxRedirects at all
...
423   const resolvedOptions = {
424     ...fetchOptions,
425     signal: composedSignal,
426     method: method.toUpperCase(),
427     headers: toByteStringHeaderObject(headers.normalize()),
428     body: data,
429     duplex: 'half',
430     credentials: isCredentialsSupported ? withCredentials : undefined,
431   };
433   request = isRequestSupported && new Request(url, resolvedOptions);
435   let response = await (isRequestSupported
436     ? _fetch(request, fetchOptions)        // <-- original object, inherited props reachable
437     : _fetch(url, resolvedOptions));
```

The sanitized `Request` is built from a spread, but the **original `fetchOptions` object** is passed
as fetch's second argument. If `fetchOptions` is a plain object and `Object.prototype.headers`
(or `method`/`cache`/`redirect`/`credentials`) has been polluted, a fetch implementation that reads
init properties sees the inherited values and overrides the sanitized Request.

### 4.2 FormData `getHeaders` inheritance — CVE-2026-101900 / GHSA-4hqw (`lib/helpers/resolveConfig.js`)

```js
65   if (utils.isFormData(data)) {
66     if (platform.hasStandardBrowserEnv || platform.hasStandardBrowserWebWorkerEnv || utils.isReactNative(data)) {
71       headers.setContentType(undefined);
72     } else if (utils.isFunction(data.getHeaders)) {        // <-- inherited read
73       // Node.js FormData (like form-data package)
74       setFormDataHeaders(headers, data.getHeaders(), own('formDataHeaderPolicy'));
75     }
76   }
```

`utils.isFormData` (`lib/utils.js:314-327`) rejects *plain* objects whose prototype is
`Object.prototype` (line 319) but accepts arrays / class instances once `Object.prototype` has been
polluted with `append`, `Symbol.toStringTag='FormData'`; `getHeaders` is then read through the
prototype chain and merged into the outbound headers.

### 4.3 Inherited headers after an interceptor — CVE-2026-101904 / GHSA-j8rh (`lib/core/dispatchRequest.js`)

```js
34 export default function dispatchRequest(config) {
35   throwIfCancellationRequested(config);
36
37   config.headers = AxiosHeaders.from(config.headers);   // <-- inherited read, no own-prop check
```

An interceptor that returns a fresh ordinary object (e.g. `({url, method}) => ({url, method})`)
drops the own `headers` property; if `Object.prototype.headers` is polluted, line 37 normalizes the
inherited object into real request headers. `lib/core/Axios.js:147`
(`config.method = (config.method || this.defaults.method || 'get').toLowerCase()`) is the analogous
inherited read for CVE-2026-101902.

### 4.4 NO_PROXY CIDR not implemented — CVE-2026-101899 / GHSA-44g4 (`lib/helpers/shouldBypassProxy.js`)

```js
274 export default function shouldBypassProxy(location) {
...
283   const noProxy = (process.env.no_proxy || process.env.NO_PROXY || '').toLowerCase();
...
296   const hostname = normalizeNoProxyHost(parsed.hostname.toLowerCase());
298   return noProxy.split(/[\s,]+/).some((entry) => {
...
307     let [entryHost, entryPort] = parseNoProxyEntry(entry);
309     entryHost = normalizeNoProxyHost(entryHost);
...
319     if (entryHost.charAt(0) === '*') { entryHost = entryHost.slice(1); }
323     if (entryHost.charAt(0) === '.') { return hostname.endsWith(entryHost); }
327     return hostname === entryHost || (isLoopback(hostname) && isLoopback(entryHost));
```

`git grep -i cidr v1.19.0 -- lib/` returns **nothing**: there is no CIDR parser/subnet match, so
`NO_PROXY=10.0.0.0/8` (or `127.0.0.0/8`) never matches; the env/`config.proxy` logic in
`lib/adapters/http.js:setProxy` (defined at line 249, called at 934) therefore proxies the request.

### 4.5 `maxRedirects: 0` ignored by fetch adapter — CVE-2026-101907 / GHSA-r4gj

The fetch adapter destructuring at `lib/adapters/fetch.js:196-211` never reads `maxRedirects`, and
`resolvedOptions` (423-431) never sets `redirect`. Node's fetch default is `redirect: 'follow'`, so a
302 is followed even when the caller asked for zero redirects.

### 4.6 `createConnection` gadget — CVE-2026-101905 / GHSA-m8m8 (`lib/adapters/http.js`)

```js
881   // Null-prototype to block prototype pollution gadgets on properties read
882   // directly by Node's http.request (e.g. insecureHTTPParser, lookup).
883   const options = Object.assign(Object.create(null), {
884     path, method, headers: toByteStringHeaderObject(headers),
885     agents: { http: httpAgent, https: httpsAgent },
886     auth, protocol, family,
891     beforeRedirect: dispatchBeforeRedirect,
892     beforeRedirects: Object.create(null),
893     http2Options,
894   });
```

There is no own `createConnection` property (the fix adds `createConnection: undefined` at
`v1.20.0:lib/adapters/http.js:965`). The same file already shows the intended defensive pattern:

```js
1045  // Always set an explicit own value so a polluted Object.prototype.insecureHTTPParser
1046  // cannot enable the lenient parser through Node's internal options copy
1048  options.insecureHTTPParser = Boolean(own('insecureHTTPParser'));
```

## 5. Fix commit `d19040b` (PR #11141)

* Full: `d19040bda7a8be2f82c3c6e1a5bc03917daee39a`, single parent `e0a02dd16671deabe2b809334d4c2ebede29a233`
  (squashed PR merge, not a two-parent merge commit), tree `0aac6e7a7c7aa39b006f2b40d1910f9105f4eb05`,
  author Jay `<jasonsaayman@gmail.com>`, `2026-08-12T18:27:45+02:00`, subject
  `fix: harden runtime option handling (#11141)`.
* Ancestry: `git merge-base --is-ancestor d19040b v1.20.0` → **true**; vs `v1.19.0` → **false**;
  vs `v1.18.1` → **false**. `git tag --contains d19040b` → **only `v1.20.0`**.
* Diffstat: 23 files, +1586/−149. Security-relevant files: `lib/adapters/fetch.js`, `lib/adapters/http.js`,
  `lib/core/Axios.js`, `lib/core/dispatchRequest.js`, `lib/helpers/resolveConfig.js`,
  `lib/helpers/shouldBypassProxy.js`, `lib/helpers/toFormData.js`, `lib/helpers/fromDataURI.js`,
  `lib/helpers/Http2Sessions.js`, `lib/utils.js`, plus tests and `PRE_RELEASE_CHANGELOG.md` /
  `PRE_RELEASE_DOCS.md`.

Hunk → advisory mapping (confirmed by the fix commit's own added tests and release notes):

| Hunk | Change | Advisory |
|---|---|---|
| `lib/adapters/fetch.js:439-451` | `safeFetchOptions = Object.assign(Object.create(null), fetchOptions)`, delete `body/headers/method/signal/duplex/credentials` | CVE-2026-101908 |
| `lib/adapters/fetch.js:453-475` + `:20` `DEFAULT_REQUEST_OPTIONS` | build `resolvedOptions` on a null-prototype object and pin fetch defaults | CVE-2026-101908 |
| `lib/adapters/fetch.js:478-484`, `:489` | `maxRedirects === 0` → `redirect:'manual'`; pass `safeFetchOptions` to fetch | CVE-2026-101907, CVE-2026-101908 |
| `lib/helpers/resolveConfig.js:66-76` | `getSafeProp(data,'getHeaders')` + `getHeaders.call(data)` | CVE-2026-101900 |
| `lib/core/dispatchRequest.js:39,43` | `utils.toSafeFlatObject(_config)`; `AxiosHeaders.from(utils.getSafeProp(config,'headers'))` | CVE-2026-101904 |
| `lib/core/Axios.js:147` | `utils.getSafeProp(config,'method')` / defaults | CVE-2026-101902 |
| `lib/adapters/http.js:965` | own `createConnection: undefined` in transport options | CVE-2026-101905 |
| `lib/helpers/shouldBypassProxy.js:259-479` | CIDR parsing (`parseCidrEntry`, `ipv4ToBytes`, `ipv6ToBytes`, `isInSubnet`), applied at `:461,472-479`; `trimTrailingDots` linear trim | CVE-2026-101899; CVE-2026-101906 (ReDoS) |
| `lib/adapters/http.js:480-510, 925-930, 965+` | `normalizeLookup`, HTTP/2 lookup propagation, `setProxy(... allowEnvProxy)` + reject proxied HTTP/2 | CVE-2026-101898 |
| `lib/helpers/Http2Sessions.js:106` | remove session on `error` | CVE-2026-101901 |
| `lib/helpers/fromDataURI.js:9` | tighten media-type regex (no extra `/`) | CVE-2026-101903 |
| `lib/helpers/toFormData.js:99-118` | options read via `utils.getSafeProp` | CVE-2026-101909 |
| `lib/utils.js:15-186, 1129` | `isUnsafeObjectKey`, `isPrototypeBoundary`, `isSafeAndFullyMutable`, rewritten `hasOwnInPrototypeChain`, new `toSafeFlatObject`; exported `getSafeProp`/`toSafeFlatObject` | shared primitive behind 101900/101902/101904/101908/101909 |

The commit's tests carry the mapping explicitly, e.g.
`tests/unit/helpers/resolveConfig.test.js` "should ignore FormData getHeaders inherited only from
Object.prototype", `tests/unit/prototypePollution.test.js` "should pass an own inert createConnection
option to transports" and "should ignore headers inherited after a request interceptor replaces
config", `tests/unit/adapters/fetch.test.js` "should ignore Request options inherited only from
Object.prototype" and "should expose an unfollowed redirect response in Node when maxRedirects is
zero", `tests/unit/helpers/shouldBypassProxy.test.js` IPv4/IPv6 CIDR tests.

## 6. Reproduction plan (local, no external network)

Setup used: `git archive <tag> | tar -x -C /tmp/axios_recon/v119|v120`, then
`npm install --ignore-scripts --no-audit --no-fund` in each (4 runtime deps). Test scripts live outside
the checkout in `/tmp/axios_recon/scripts/`, take the tag directory as `argv[2]`, and import
`<dir>/index.js` (ESM; Node 24 also allows `require(index.js)`). Each test starts 127.0.0.1 servers on
ephemeral ports and clears `*_PROXY` env except t4.

| # | Advisory | Injection / setup | v1.19.0 (RED) | v1.20.0 (GREEN) |
|---|---|---|---|---|
| t2 | CVE-2026-101900 | real `FormData` body, `Object.prototype.getHeaders = () => ({'x-poison':'t2'})`, `adapter:'fetch'` | server receives `x-poison: t2` | header absent |
| t3 | CVE-2026-101904 | `Object.prototype.headers = {'x-poison':'t3'}`; request interceptor returns `({url,method}) => ({url, method})` | server receives `x-poison: t3` | header absent |
| t4 | CVE-2026-101899 | `HTTP_PROXY=http://127.0.0.1:<P>`, `NO_PROXY=127.0.0.0/8`, request `http://127.0.0.1:<T>/`; local proxy and local target both record hits | proxy hit: body `PROXIED` (target hit 0) | direct hit: body `DIRECT` (proxy hit 0) |
| t5 | CVE-2026-101907 | `/start` → 302 `/secret`, `adapter:'fetch', maxRedirects:0` | follows: status 200, body `SECRET-BODY`, hits `['/start','/secret']` | status 302 (axios rejects non-2xx), hits `['/start']`, `/secret` never requested |
| t1b | CVE-2026-101908 | `Object.prototype.headers={'x-poison':'t1b'}`, `fetchOptions:{}`, custom `env:{fetch}` | custom fetch `init` is a plain object; `init.headers === {'x-poison':'t1b'}` | `init` has null prototype; `init.headers === undefined` |
| t1 | CVE-2026-101908 | same pollution, **built-in Node fetch** | `x-poison` reaches server | **still reaches server** — masked by undici, see §8 |
| t6 | CVE-2026-101905 | `Object.prototype.createConnection = fn` connecting to a local listener, request to `http://198.51.100.77/steal` with default transport | listener never hit; request times out | listener never hit; request times out |

Observed raw results (abridged):

```
t2 v1.19.0 {"status":200,"poisonSeen":true,"seen":[...,"x-poison":"t2",...]}
t2 v1.20.0 {"status":200,"poisonSeen":false,...}
t3 v1.19.0 {"status":200,"poisonSeen":true,...}
t3 v1.20.0 {"status":200,"poisonSeen":false,...}
t4 v1.19.0 {"status":200,"body":"PROXIED","proxyHits":1,"directHits":0}
t4 v1.20.0 {"status":200,"body":"DIRECT","proxyHits":0,"directHits":1}
t5 v1.19.0 {"status":200,"body":"SECRET-BODY","hits":["/start","/secret"]}
t5 v1.20.0 {"error":"Request failed with status code 302","hits":["/start"]}
t1b v1.19.0 {"status":200,"captured":{"protoIsNull":false,"initHeaders":{"x-poison":"t1b"}}}
t1b v1.20.0 {"status":200,"captured":{"protoIsNull":true}}
t6 v1.19.0 {"error":"timeout of 4000ms exceeded","attackerHits":0}
```

Expected red/green invariant per advisory:

* 101899 — proxy selection: vulnerable build sends the request to the configured proxy even though the
  destination is inside a `NO_PROXY` CIDR; fixed build connects directly. Observable = which local
  listener receives the request/body.
* 101900 — inherited `getHeaders()` must not be called and its headers must not be merged.
* 101904 — after an interceptor returns a replacement config, inherited `headers` must not be
  normalized into the request.
* 101907 — `maxRedirects: 0` must not follow a 302; observable = the `/secret` handler is never hit and
  the 3xx status is surfaced.
* 101908 — the second argument passed to fetch must not carry inherited `headers` (null-prototype
  init, `headers === undefined`), while the `Request` keeps the sanitized Axios headers.

For a dataset oracle, t2/t3/t4/t5 are the strongest (pure in-process, deterministic, no network).
t1b needs a custom fetch shim; t6 should not be used on Node 24.

## 7. Build / install feasibility

* **Correction to the brief:** axios is **not** dependency-free. `package.json` at both v1.19.0 and
  v1.20.0 declares 4 runtime dependencies: `follow-redirects ^1.16.0`, `form-data ^4.0.6`,
  `https-proxy-agent ^5.0.1`, `proxy-from-env ^2.1.0`. They must be present (npm registry install, or
  vendored) before the tag can run. After that, the repro itself needs no network.
* `npm install --ignore-scripts` works and is enough (avoids the `prepare: husky` hook). No build step
  is required for ESM use: `import('<tag>/index.js')` works (package `"type": "module"`), verified
  `VERSION` 1.19.0 / 1.20.0.
* CJS: `"main"` is `./dist/node/axios.cjs`, but `dist/` is **gitignored and not in the repo**. A raw
  checkout has no dist; `npm run build` (gulp + rollup, devDeps installed) or the published npm
  tarball is needed for a true `require('axios')` consumer. On Node 24 `require('<tag>/index.js')`
  works via require(ESM), so this is not a blocker locally.
* Fetch adapter: available and functional on Node 24 because `Request`/`Response`/`fetch` are globals;
  `adapter:'fetch'` works. `config.env.{fetch,Request,Response}` is the supported custom-fetch hook
  (`lib/adapters/fetch.js:618-639` at v1.19.0).
* v1.19.0 already has earlier hardening (NO_PROXY IPv4 canonicalization, own `insecureHTTPParser`,
  plain-object rejection in `isFormData`, `getSafeProp` helper), which is why the PoCs must use the
  specific paths in §4 rather than generic `__proto__` payloads.

## 8. Risks / judgment

1. **Most of the batch is gadget-class, not standalone.** 101900/101902/101904/101905/101908/101909
   require the application to already have a same-process `Object.prototype` pollution primitive.
   They are real header/transport-integrity escalations (authorization, cache, metadata-service
   access), but a repro must itself install the pollution, so "real-world severity" is a chained
   scenario. By contrast 101899 (proxy exclusion bypass) only needs an attacker-influenced URL plus
   a `NO_PROXY` CIDR, and 101907 (redirect SSRF/`maxRedirects: 0`) needs only an attacker-controlled
   redirect target — these are the cleanest security-relevant items.
2. **CVE-2026-101908 is masked by Node 24.16's own fetch.** With the built-in undici fetch, an
   `Object.prototype.headers` (and `Object.prototype.method`) pollution is applied even by
   `fetch(url)` with no init and even when the caller passes a `Request`: the server received the
   poisoned header on **both** v1.19.0 and v1.20.0. undici 7.25.0 appears to materialize an ordinary
   init object internally (a bare `fetch(url)` with no init is enough to trigger it), so the axios fix
   (null-prototype `safeFetchOptions`) is invisible at that boundary.
   The axios-level fix is observable only with a custom `env.fetch` that reads `init.headers`
   directly (this is exactly how the fix commit's own test is written). **Do not build the oracle for
   101908 on global fetch** — it will stay red at the fixed release.
3. **CVE-2026-101905 does not reproduce on Node 24.16 with the default transport.** Node's
   `ClientRequest` copies options into a null-prototype object (`_http_client.js:212`,
   `optsWithoutSignal` at `:252`), so inherited properties never reach `typeof
   options.createConnection`; in the normal path Node falls back to the default `Agent`, whose own
   `Agent.prototype.createConnection` shadows any polluted key. Both tags timed out with zero
   attacker hits. (The gadget needs a downstream consumer that flattens the axios options object into
   a normal-prototype object before reading `createConnection` — which is why the fix commit's test
   asserts the own inert `createConnection` property through a custom `transport`.) Treat this one as
   defense-in-depth/version-dependent, not a repro candidate on this Node.
4. **NVD is not usable as an oracle.** All six records are "Awaiting Analysis", with no CPE
   configurations and no ranges. Ranges/severity must come from OSV/GHSA.
5. **Catalog error to fix upstream:** CVE-2026-101907 and CVE-2026-101905 are live High-severity
   advisories fixed in 1.20.0, not rejected/withdrawn. If the dataset filters "rejected" siblings it
   is dropping the two strongest items in the batch.
6. **Tag freshness:** v1.19.0 is 3 months old at recon time and `v1.x` HEAD is already preparing
   1.21.0; if a `v1.21.0` tag appears later the "newest stable below fix" rule still selects v1.19.0
   (the fix boundary is 1.20.0), so the recommendation is stable.
7. **Provenance/artifacts:** raw git tag ≠ published npm tarball. If the audit needs built `dist/`
   output, either build the tag or pin the npm tarball; line numbers above are git-tree line numbers.

## Appendix — artifacts

* Clone: `/tmp/axios_recon/axios` (full clone, all tags).
* Extracted tags + deps: `/tmp/axios_recon/v119`, `/tmp/axios_recon/v120`.
* Repro scripts (outside clone): `/tmp/axios_recon/scripts/{t1_fetchopts,t1b_customfetch,t2_formdata,t3_interceptor,t4_noproxy,t5_maxredirect,t6_createconn,undici_probe,undici_probe2}.mjs`.
* Fetched advisory JSON: `/tmp/axios_recon/osv_*.json`, `/tmp/axios_recon/nvd_CVE-2026-*.json`, `/tmp/axios_recon/qv_1.19.0.json`, `/tmp/axios_recon/qv_1.20.0.json`.
* Run: `timeout 60 node /tmp/axios_recon/scripts/<test>.mjs /tmp/axios_recon/v119` (then `v120`).
