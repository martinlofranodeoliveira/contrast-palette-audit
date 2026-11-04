"""Add at least four meaningful engine regression tests for the README contract."""
import unittest
from contrast_palette_audit.engine import analyze

class TestContrastAudit(unittest.TestCase):
    def test_example_black_on_white(self):
        r = analyze({"pairs": [{"id": "body", "foreground": "#000", "background": "#fff"}]})
        self.assertTrue(r["valid"])
        self.assertEqual(r["pairs"][0]["ratio"], 21.0)
        self.assertEqual((r["pairs"][0]["aa"], r["pairs"][0]["aa_large"], r["pairs"][0]["aaa"], r["pairs"][0]["aaa_large"]), (True, True, True, True))
        self.assertEqual(r["summary"], {"total": 1, "aa_pass": 1, "aaa_pass": 1})

    def test_empty_batch_valid(self):
        r = analyze({"pairs": []})
        self.assertEqual(r, {"valid": True, "pairs": [], "summary": {"total": 0, "aa_pass": 0, "aaa_pass": 0}})

    def test_order_thresholds_shorthand_case(self):
        r = analyze({"pairs": [{"id": "b", "foreground": "#000000", "background": "#FFFFFF"}, {"id": "a", "foreground": "#777777", "background": "#ffffff"}]})
        self.assertEqual([p["id"] for p in r["pairs"]], ["b", "a"])
        self.assertEqual(r["pairs"][0]["ratio"], 21.0)
        self.assertFalse(r["pairs"][1]["aa"])
        self.assertTrue(r["pairs"][1]["aa_large"])
        self.assertFalse(r["pairs"][1]["aaa"])
        self.assertFalse(r["pairs"][1]["aaa_large"])
        self.assertFalse(r["valid"])
        self.assertEqual(r["summary"]["total"], 2)

    def test_pure_preserves_input(self):
        payload = {"pairs": [{"id": "x", "foreground": "#123", "background": "#abc"}]}
        snap = {"pairs": [{"id": "x", "foreground": "#123", "background": "#abc"}]}
        analyze(payload)
        self.assertEqual(payload, snap)

    def test_invalid_inputs(self):
        bad = [{}, {"pairs": {}}, {"pairs": [], "extra": 1}, {"pairs": [{"id": "", "foreground": "#000", "background": "#fff"}]}, {"pairs": [{"id": "a", "foreground": "#000", "background": "#fff"}, {"id": "a", "foreground": "#000", "background": "#fff"}]}, {"pairs": [{"id": "a", "foreground": "black", "background": "#fff"}]}, {"pairs": [{"id": "a", "foreground": "#0000", "background": "#fff"}]}, {"pairs": [{"id": "a", "foreground": "#000", "background": "#fff", "extra": 1}]}, {"pairs": [{"id": "a", "foreground": "#000"}]}]
        for p in bad:
            with self.assertRaises(ValueError) as cm:
                analyze(p)
            self.assertEqual(str(cm.exception), "INPUT_INVALID")

if __name__ == "__main__":
    unittest.main()
