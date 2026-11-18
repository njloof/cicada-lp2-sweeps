"""Skeleton module must reproduce the campaign #21 ground-truth facts
(p57 PT=CT page; p56 solved page, null-F at CT index 47)."""
import unittest

import core.skeleton as S


class TestSkeleton(unittest.TestCase):
    def test_p57_counts(self):
        sk = S.skeleton(57)
        self.assertEqual(len(sk["dashes"]), 16)   # G2: 16 dashes
        cls = sorted(c for c, _ in sk["marks"])
        # 2 sentence ◆4 + book-end ◆23 + inline ◆13 (red section motif,
        # S7: p57 carries the 13-dot matrix inline)
        self.assertEqual(cls, ["13", "23", "4", "4"])

    def test_p56_letter_boundaries_match_21(self):
        # dash_positions() output from scripts/audit/skeleton_test.py run
        # (letter space, nulls={47}) — the V1 instrument's inputs:
        expected = {2, 11, 14, 19, 27, 33, 34, 38, 42, 51, 56, 57, 60,
                    65, 67, 73, 82, 84, 89, 93, 97}
        sk = S.skeleton(56)
        self.assertEqual(len(sk["dashes"]), 21)
        bounds, _ = S.letter_boundaries(sk, 56, nulls={47})
        self.assertEqual(bounds, expected)

    def test_p56_wraps_merge(self):
        # p57 ground truth: wraps split words WITHOUT dashes; cribs may
        # span wrap positions but never a dash.
        sk = S.skeleton(56)
        self.assertGreater(len(sk["wraps"]), 0)
        self.assertGreater(S.crib_placements("PILGRIM", 56, nulls={47},
                                             skel=sk), 0)

    def test_penalty_flags_straddle(self):
        # a single-word crib forced across a known dash boundary must be
        # flagged; the same crib placed inside a slot must not be.
        sk = S.skeleton(56)
        bounds, _ = S.letter_boundaries(sk, 56, nulls={47})
        b = sorted(bounds)[3]                 # mid-text boundary (o stays >=0)
        n = S._cum(56, {47})[-1]
        cand = ["X"] * n
        o = b - 3                             # WITHIN (6) straddles b
        cand[o:o + 6] = list("WITHIN")
        self.assertGreater(S.skeleton_penalty("".join(cand), 56,
                                              nulls={47}, skel=sk), 0.0)

    def test_pruning_works(self):
        # strict single-word pruning must actually shrink the space
        n = S._cum(56, ())[-1]
        free = n - len("PILGRIM") + 1
        self.assertLess(S.crib_placements("PILGRIM", 56, nulls={47}), free)
        # phrase cribs are exempt (no pruning, no false constraint)
        n56 = S._cum(56, {47})[-1]
        self.assertEqual(S.crib_placements("HASHESTO", 56, nulls={47}),
                         n56 - len("HASHESTO") + 1)

    def test_score_ranks_true_text(self):
        import core.validate as V
        pt57 = V.translit(V.flat(57)).upper()
        shuffled = "".join(sorted(pt57))
        self.assertGreater(S.score_text(pt57), S.score_text(shuffled))


if __name__ == "__main__":
    unittest.main()
