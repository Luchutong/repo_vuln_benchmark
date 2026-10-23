# Superseded independent verdicts

These verdicts are retained for audit but are not used by the promotion gate.
Each subdirectory is one directory deeper than the `*/verdict.json` glob, so
`promote_verified.py` does not read it; the reason for supersession must be
recorded here and in WORK_LOG.md.

## phoenix_CVE-2022-42975_round1

- Reviewer verdict: all fields true except `location`, because the dossier's
  entry point was written as `check_origin/2` at `lib/phoenix/socket/transport.ex:605`.
  That function does not exist; line 605 is an `origin_allowed?` clause.
- The dossier was corrected to `check_origin/5` at line 342, then re-reviewed
  from scratch by a new independent reviewer in
  `runs/independent/phoenix_CVE-2022-42975_round2/`, which verified all nine
  fields (the file/line of the vulnerable wildcard clause never changed).
- The round1 verdict is NOT evidence that the vulnerability claim was wrong; it
  documented a metadata error in the dossier. No field of the round1 verdict was
  edited.

## protobuf_CVE-2022-1941_round1

- Reviewer verdict: all fields true except `location`, because the dossier
  qualified the parser as `WireFormatLite::ParseMessageSetItemImpl` and used the
  partial line range 1827-1877.
- The function is actually the free template
  `google::protobuf::internal::ParseMessageSetItemImpl` spanning 1821-1890
  (`WireFormatLite` ends at line 746). The dossier was corrected to the exact
  function qualification and full range, then re-reviewed from scratch by a new
  independent reviewer in `runs/independent/protobuf_CVE-2022-1941_round2/`.
- The vulnerable code excerpt itself was byte-identical to the source; the
  round1 objection was about the enclosing symbol and range, not the defect.
