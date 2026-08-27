; ============================================================================
; FGA T18 — stated-goal template (SPECIFICATION.md section 5)
;
; Purpose: counterexample search for a governance goal G over one artifact.
; Instantiate by replacing the GOAL PLACEHOLDER with a concrete, checkable
; predicate (axiom A6). The query asks: can a schema-valid artifact VIOLATE G?
;
;   SAT   => G is violable; (get-model) yields a concrete counterexample
;   UNSAT => G holds for every schema-valid artifact
; ============================================================================

(set-logic QF_LIA)

; --- Artifact abstraction ---------------------------------------------------
; Content addressing is reduced to integer ids. (A bit-vector/string encoding
; of SHA-256 is future work — see SPECIFICATION.md section 5.)
(declare-fun artifact_id () Int)
(declare-fun parent_id   () Int)
(declare-fun payload_sum () Int)   ; stand-in checksum of the canonical payload

; --- Schema constraints -----------------------------------------------------
(assert (>  artifact_id 0))        ; ids are positive
(assert (>= parent_id   0))        ; 0 encodes the null (genesis) parent
(assert (>= payload_sum 0))

; --- GOAL PLACEHOLDER -------------------------------------------------------
; Example goal G: "no artifact references itself as parent".
; We search for a COUNTEREXAMPLE, so we assert the NEGATION of G:
(assert (= artifact_id parent_id))          ; violates G
; To check your own goal, replace the line above with (assert (not <G>)).
; ----------------------------------------------------------------------------

(check-sat)
; (get-model)   ; uncomment to inspect the counterexample when SAT
