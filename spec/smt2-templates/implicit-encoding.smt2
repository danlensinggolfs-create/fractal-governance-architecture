; ============================================================================
; FGA T18 — implicit-encoding template (SPECIFICATION.md section 5)
;
; Transition relation T(a, a'): a' is a valid successor of a in the Merkle
; Governance Chain. The hash function H is left UNINTERPRETED in v0.1;
; instantiate it with a concrete theory (e.g. fixed-width bit-vectors) for
; executable checking.
;
; Query below: is a two-artifact chain with a self-parenting second artifact
; possible while remaining a valid successor? SAT would expose an encoding bug.
; ============================================================================

(set-logic QF_UFLIA)

; H(type, parent, payload) -> id   (abstract content addressing, axiom A2)
(declare-fun H (Int Int Int) Int)

; --- artifact a (the parent) -------------------------------------------------
(declare-fun t0 () Int)             ; artifact_type code
(declare-fun p0 () Int)             ; parent id
(declare-fun d0 () Int)             ; payload checksum

; --- artifact a' (the candidate successor) -----------------------------------
(declare-fun t1 () Int)
(declare-fun p1 () Int)
(declare-fun d1 () Int)

; a' is a valid successor of a  <=>  parent(a') = H(body(a))   (axiom A3)
(define-fun valid_successor () Bool
  (= p1 (H t0 p0 d0)))

(assert valid_successor)

; Property probe: can a' also be self-parenting? In a correct instantiation
; with collision resistance this must be UNSAT; with abstract H it may be SAT,
; which precisely marks where the cryptographic assumption is needed.
(assert (= p1 (H t1 p1 d1)))

(check-sat)
; (get-model)
