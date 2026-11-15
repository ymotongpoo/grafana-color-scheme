"""Flavor structure and palette validation regressions (stdlib only)."""

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from dataclasses import replace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gcs import palette, svg, verify
from gcs.emit import chrome, iterm2, vscode, wezterm

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "chrome-manifests.json"

PRIMARY_AND_SECONDARY = {"orange", "yellow", "green", "blue", "purple"}


class PaletteTests(unittest.TestCase):
    def setUp(self):
        self.palette = palette.load(ROOT / "palette.toml")
        self.chrome = json.loads(FIXTURE.read_text())

    def changed_variant(self, name, flavor, **changes):
        variants = dict(self.palette.variants)
        variants[name, flavor] = replace(variants[name, flavor], **changes)
        return replace(self.palette, variants=variants)

    def load_modified(self, old, new):
        source = (ROOT / "palette.toml").read_text()
        self.assertIn(old, source)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "palette.toml"
            path.write_text(source.replace(old, new, 1))
            return palette.load(path)

    def test_default_and_explicit_flavors(self):
        self.assertEqual(self.palette.flavors, ["brand", "dim"])
        self.assertEqual([v.flavor for _, v in self.palette.each()], ["brand", "brand"])
        self.assertEqual([v.flavor for _, v in self.palette.each("dim")], ["dim", "dim"])
        self.assertEqual([v.id for _, v in self.palette.every()],
                         ["grafana-dark", "grafana-light", "grafana-dark-dim", "grafana-light-dim"])
        self.assertEqual(self.palette.variant("dark", "dim").label, "Grafana Dark Dim")
        with self.assertRaises(KeyError):
            self.palette.variant("dark", "unknown")

    def test_dark_brand_uses_brand_colors_verbatim(self):
        dark = self.palette.variant("dark")
        for token, hexv in dark.accents.items():
            with self.subTest(token=token):
                self.assertEqual(hexv, self.palette.brand_hex(token))
        self.assertEqual(dark.surfaces["base"], self.palette.brand_hex("neutral-5"))
        self.assertEqual(self.palette.variant("light").surfaces["base"],
                         self.palette.brand_hex("white"))

    def test_light_brand_accents_come_from_the_brand(self):
        light = self.palette.variant("light")
        ladders = self.palette.brand["ladders"]
        for token in ("orange", "yellow", "green", "blue", "purple"):
            with self.subTest(token=token):
                in_ladder = light.accents[token] in ladders[token].values()
                verbatim = light.accents[token] == self.palette.brand_hex(token)
                self.assertTrue(in_ladder or verbatim, light.accents[token])

    def test_primary_and_secondary_carry_the_frequent_roles(self):
        roles = self.palette.variant("dark").roles
        for name in ("keyword", "operator", "string", "function", "method",
                     "type", "class", "number", "constant"):
            with self.subTest(role=name):
                self.assertIn(roles[name].token, PRIMARY_AND_SECONDARY)
        self.assertEqual(roles["keyword"].token, "orange")

    def test_dim_tuning_does_not_leak_into_brand(self):
        tuned = self.load_modified('fg             = "#cccccc"', 'fg             = "#aabbcc"')
        dim, brand = tuned.variant("dark", "dim"), tuned.variant("dark")
        self.assertEqual(dim.rc("variable"), "#aabbcc")
        self.assertEqual(dim.ansi()[7], "#aabbcc")
        self.assertEqual(brand.rc("variable"), "#f4f4f4")
        self.assertEqual(wezterm.emit(tuned)["colors/grafana-dark.toml"],
                         wezterm.emit(self.palette)["colors/grafana-dark.toml"])

    def test_every_flavor_is_emitted(self):
        for files, pattern in ((wezterm.emit(self.palette), "colors/{}.toml"),
                               (iterm2.emit(self.palette), "{}.itermcolors"),
                               (vscode.emit(self.palette), "themes/{}-color-theme.json")):
            for _, v in self.palette.every():
                self.assertIn(pattern.format(v.id), files)
        labels = [t["label"] for t in json.loads(vscode.emit(self.palette)["package.json"])
                  ["contributes"]["themes"]]
        self.assertEqual(labels, ["Grafana Dark", "Grafana Light",
                                  "Grafana Dark Dim", "Grafana Light Dim"])

    def test_chrome_is_unchanged(self):
        files = chrome.emit(self.palette)
        self.assertEqual(sorted(files), ["grafana-dark/manifest.json", "grafana-light/manifest.json"])
        for name in ("dark", "light"):
            content = files[f"grafana-{name}/manifest.json"]
            self.assertEqual(hashlib.sha256(content.encode()).hexdigest(),
                             self.chrome[name]["chrome_sha256"])

    def test_unknown_role_reference_fails_to_load(self):
        with self.assertRaises(KeyError):
            self.load_modified('color = "fg"', 'color = "missing"')

    def test_missing_and_extra_ansi_slots_in_dim_are_rejected(self):
        table = dict(self.palette.variant("light", "dim").ansi())
        del table[10]
        table[16] = "#ffffff"
        altered = self.changed_variant("light", "dim", ansi_colors=table)
        messages = [str(problem) for problem in verify.check_ansi(altered)]
        self.assertEqual(len(messages), 1)
        self.assertIn("light/dim missing slots [10], extra slots [16]", messages[0])

    def test_validation_covers_dim_colors_roles_and_surfaces(self):
        dim = self.palette.variant("dark", "dim")
        bad_colors = self.changed_variant("dark", "dim", text={**dim.text, "faint": "oops"})
        self.assertTrue(verify.run(bad_colors))
        bad_role = replace(dim.role("comment"), style="unknown")
        bad_roles = self.changed_variant("dark", "dim", roles={**dim.roles, "comment": bad_role})
        self.assertTrue(verify.check_roles(bad_roles))
        bad_surfaces = self.changed_variant("dark", "dim", surfaces={**dim.surfaces, "crust": "#ffffff"})
        self.assertTrue(verify.check_ladders(bad_surfaces))

    def test_palette_holds_and_browser_policy_is_enforced(self):
        self.assertEqual(verify.run(self.palette), [])
        brand = self.palette.variant("dark")
        bad_browser = {**brand.browser, "on_key": brand.browser["key"]}
        altered = self.changed_variant("dark", "brand", browser=bad_browser)
        self.assertTrue(verify.check_contrast(altered))

    def test_ansi_boards_use_each_flavors_background(self):
        import xml.etree.ElementTree as ET
        for name in ("dark", "light"):
            root = ET.fromstring(svg.emit(self.palette)[f"ansi-{name}.svg"])
            backgrounds = [rect.attrib["fill"] for rect in root.findall("{*}rect")
                           if rect.attrib["width"] == root.attrib["width"]]
            self.assertEqual(backgrounds, [self.palette.variant(name, f).surfaces["base"]
                                           for f in self.palette.flavors])


if __name__ == "__main__":
    unittest.main()
