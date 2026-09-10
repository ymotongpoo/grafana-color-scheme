"""Flavor migration and palette validation regressions (stdlib only)."""

import hashlib
import json
from pathlib import Path
import plistlib
import sys
import tempfile
import tomllib
import unittest
from dataclasses import replace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gcs import palette, svg, verify
from gcs.emit import chrome, iterm2, wezterm

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "previous-defaults.json"


class PaletteTests(unittest.TestCase):
    def setUp(self):
        self.palette = palette.load(ROOT / "palette.toml")
        self.previous = json.loads(FIXTURE.read_text())

    def changed_variant(self, name, flavor, **changes):
        variants = dict(self.palette.variants)
        variants[name, flavor] = replace(variants[name, flavor], **changes)
        return replace(self.palette, variants=variants)

    def test_vivid_preserves_previous_terminal_defaults(self):
        schemes = wezterm.emit(self.palette)
        presets = iterm2.emit(self.palette)
        for name in ("dark", "light"):
            with self.subTest(name=name):
                scheme = tomllib.loads(schemes[f"colors/grafana-{name}-vivid.toml"])
                self.assertEqual(scheme["colors"], self.previous[name]["wezterm"])
                self.assertEqual(scheme["metadata"]["name"], f"Grafana {name.title()} Vivid")
                preset = plistlib.loads(presets[f"grafana-{name}-vivid.itermcolors"].encode())
                self.assertEqual(preset, self.previous[name]["iterm2"])

    def test_chrome_is_unchanged(self):
        for name in ("dark", "light"):
            content = chrome.emit(self.palette)[f"grafana-{name}/manifest.json"]
            self.assertEqual(hashlib.sha256(content.encode()).hexdigest(),
                             self.previous[name]["chrome_sha256"])

    def test_default_and_explicit_flavors(self):
        self.assertEqual([v.flavor for _, v in self.palette.each()], ["dim", "dim"])
        self.assertEqual([v.flavor for _, v in self.palette.each("vivid")], ["vivid", "vivid"])
        self.assertEqual(self.palette.variant("dark").surfaces["base"], "#241f1c")
        self.assertEqual(self.palette.variant("light").surfaces["base"], "#e8e1d9")
        with self.assertRaises(KeyError):
            self.palette.variant("dark", "unknown")

    def test_dim_tuning_does_not_leak_into_vivid(self):
        source = (ROOT / "palette.toml").read_text().replace('"#b9b1a9"', '"#aabbcc"', 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "palette.toml"
            path.write_text(source)
            tuned = palette.load(path)
        dim, vivid = tuned.variant("dark"), tuned.variant("dark", "vivid")
        self.assertEqual(dim.rc("variable"), "#aabbcc")
        self.assertEqual(dim.ansi()[7], "#aabbcc")
        self.assertEqual(vivid.rc("variable"), "#c9c9c9")
        self.assertEqual(wezterm.emit(tuned)["colors/grafana-dark-vivid.toml"],
                         wezterm.emit(self.palette)["colors/grafana-dark-vivid.toml"])

    def test_unknown_role_reference_fails_to_load(self):
        source = (ROOT / "palette.toml").read_text().replace('color = "fg"', 'color = "missing"')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "palette.toml"
            path.write_text(source)
            with self.assertRaises(KeyError):
                palette.load(path)

    def test_missing_and_extra_ansi_slots_in_vivid_are_rejected(self):
        table = dict(self.palette.variant("light", "vivid").ansi())
        del table[10]
        table[16] = "#ffffff"
        altered = self.changed_variant("light", "vivid", ansi_colors=table)
        messages = [str(problem) for problem in verify.check_ansi(altered)]
        self.assertEqual(len(messages), 1)
        self.assertIn("light/vivid missing slots [10], extra slots [16]", messages[0])

    def test_validation_covers_vivid_colors_roles_and_surfaces(self):
        vivid = self.palette.variant("dark", "vivid")
        bad_colors = self.changed_variant("dark", "vivid", text={**vivid.text, "faint": "oops"})
        self.assertTrue(verify.run(bad_colors))
        bad_role = replace(vivid.role("comment"), style="unknown")
        bad_roles = self.changed_variant("dark", "vivid", roles={**vivid.roles, "comment": bad_role})
        self.assertTrue(verify.check_roles(bad_roles))
        bad_surfaces = self.changed_variant("dark", "vivid", surfaces={**vivid.surfaces, "crust": "#ffffff"})
        self.assertTrue(verify.check_ladders(bad_surfaces))

    def test_low_contrast_reading_palette_and_browser_policy(self):
        self.assertEqual(verify.run(self.palette), [])
        vivid = self.palette.variant("dark", "vivid")
        bad_browser = {**vivid.browser, "on_key": vivid.browser["key"]}
        altered = self.changed_variant("dark", "vivid", browser=bad_browser)
        self.assertTrue(verify.check_contrast(altered))
        self.assertNotIn("slot8_min_on_base", self.palette.ansi_constraints)

    def test_ansi_boards_use_each_flavors_background(self):
        import xml.etree.ElementTree as ET
        for name in ("dark", "light"):
            root = ET.fromstring(svg.emit(self.palette)[f"ansi-{name}.svg"])
            backgrounds = [rect.attrib["fill"] for rect in root.findall("{*}rect")
                           if rect.attrib["width"] == root.attrib["width"]]
            self.assertEqual(backgrounds, [self.palette.variant(name, f).surfaces["base"]
                                           for f in ("dim", "vivid")])


if __name__ == "__main__":
    unittest.main()
