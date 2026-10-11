"""Regression contract for observed QC-only ms-proteomics 1.2.0 draft.

Uses only the dependencies already installed by sdrf-templates' CI.
Integration with the full SDRF validator is tested separately in sdrf-pipelines.
"""

from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "ms-proteomics/1.1.0/ms-proteomics.yaml"
NEW = ROOT / "ms-proteomics/1.2.0/ms-proteomics.yaml"
EXAMPLE = ROOT / "ms-proteomics/1.2.0/ms-proteomics.sdrf.tsv"

QC_TERMS = {
    "comment[number of MS1 spectra]": "MS:4000059",
    "comment[number of MS2 spectra]": "MS:4000060",
    "comment[chromatography duration]": "MS:4000053",
}
REJECTED_OLD_PROPOSALS = {
    "comment[estimated precursor mass tolerance]",
    "comment[estimated fragment mass tolerance]",
    "comment[predicted modification]",
    "comment[predicted modification evidence]",
}


class MSProteomicsV120Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.old = yaml.safe_load(OLD.read_text(encoding="utf-8"))
        cls.new = yaml.safe_load(NEW.read_text(encoding="utf-8"))
        cls.old_columns = {c["name"]: c for c in cls.old["columns"]}
        cls.new_columns = {c["name"]: c for c in cls.new["columns"]}

    def test_version_and_parent_unchanged(self) -> None:
        self.assertEqual(self.old["version"], "1.1.0")
        self.assertEqual(self.new["version"], "1.2.0")
        for field in ("name", "extends", "layer", "usable_alone", "validators"):
            self.assertEqual(self.old.get(field), self.new.get(field), field)

    def test_all_existing_columns_are_unmodified(self) -> None:
        self.assertEqual(len(self.old_columns), len(self.old["columns"]))
        self.assertEqual(len(self.new_columns), len(self.new["columns"]))
        for name, definition in self.old_columns.items():
            with self.subTest(column=name):
                self.assertEqual(self.new_columns[name], definition)

    def test_only_three_observed_qc_columns_are_new(self) -> None:
        additions = set(self.new_columns) - set(self.old_columns)
        self.assertEqual(additions, set(QC_TERMS))
        self.assertFalse(REJECTED_OLD_PROPOSALS & set(self.new_columns))
        for name in additions:
            with self.subTest(column=name):
                self.assertEqual(self.new_columns[name].get("requirement"), "optional")

    def test_qc_cv_and_missing_policy(self) -> None:
        for name, accession in QC_TERMS.items():
            with self.subTest(column=name):
                column = self.new_columns[name]
                self.assertEqual(column["ontology_accession"], accession)
                self.assertTrue(column["allow_not_available"])
                self.assertFalse(column["allow_not_applicable"])
                self.assertEqual(len(column["validators"]), 1)
                v = column["validators"][0]
                self.assertEqual(v["validator_name"], "pattern")
                self.assertEqual(v["params"]["error_level"], "error")
                self.assertEqual(v["params"].get("case_sensitive"), True)
        for name in QC_TERMS:
            if name.endswith("spectra]"):
                self.assertEqual(self.new_columns[name]["type"], "integer")

    def _value_accepted(self, column: str, value: str) -> bool:
        spec = self.new_columns[column]
        if value == "not available":
            return spec["allow_not_available"]
        if value == "not applicable":
            return spec["allow_not_applicable"]
        if value == "":
            return True  # optional cells may remain empty
        return re.fullmatch(spec["validators"][0]["params"]["pattern"], value) is not None

    def test_counts_accept_zero_and_reject_invalid_numbers(self) -> None:
        good = ("0", "1", "13776", "999999999")
        bad = ("-1", "01", "1.0", "1e3", "NaN", "inf", "1 count", "not applicable")
        for name in list(QC_TERMS)[:2]:
            for value in good:
                with self.subTest(column=name, value=value):
                    self.assertTrue(self._value_accepted(name, value))
            for value in bad:
                with self.subTest(column=name, value=value):
                    self.assertFalse(self._value_accepted(name, value))
            self.assertTrue(self._value_accepted(name, "not available"))

    def test_duration_requires_explicit_seconds(self) -> None:
        name = "comment[chromatography duration]"
        good = ("0 s", "3600 s", "3600.5 s", "1e-05 s", "1E+05 s", "not available")
        bad = ("0", "3600", "-1 s", ".5 s", "01 s", "10 min", "nan s", "inf s", "not applicable")
        for value in good:
            with self.subTest(value=value):
                self.assertTrue(self._value_accepted(name, value))
        for value in bad:
            with self.subTest(value=value):
                self.assertFalse(self._value_accepted(name, value))

    def test_example_is_rectangular_unique_and_has_all_required_columns(self) -> None:
        self.assertTrue(EXAMPLE.is_file())
        with EXAMPLE.open(encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file, delimiter="\t")
            headers = reader.fieldnames or []
            rows = list(reader)
        self.assertEqual(len(headers), len(set(headers)))
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(None not in row for row in rows))
        self.assertTrue(all(all(value is not None for value in row.values()) for row in rows))
        base = yaml.safe_load((ROOT / "base/1.1.0/base.yaml").read_text(encoding="utf-8"))
        sample = yaml.safe_load((ROOT / "sample-metadata/1.0.0/sample-metadata.yaml").read_text(encoding="utf-8"))
        for template in (base, sample, self.new):
            for column in template["columns"]:
                if column.get("requirement") == "required":
                    self.assertIn(column["name"], headers)
                    for row in rows:
                        self.assertNotEqual(row[column["name"]], "")
        for row in rows:
            for name in QC_TERMS:
                self.assertTrue(self._value_accepted(name, row[name]))
        self.assertEqual(rows[0]["comment[chromatography duration]"], "3600.5 s")
        self.assertEqual(rows[1]["comment[number of MS1 spectra]"], "0")
        self.assertEqual(rows[1]["comment[chromatography duration]"], "not available")
        self.assertEqual(rows[2]["comment[chromatography duration]"], "0 s")


if __name__ == "__main__":
    unittest.main()
