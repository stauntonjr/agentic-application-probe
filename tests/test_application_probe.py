import io
import json
import tempfile
import unittest
from pathlib import Path

from agentic_application_probe.cli import run, summarize_csv


class CsvSummaryTests(unittest.TestCase):
    def write_csv(self, directory: str, content: str) -> Path:
        path = Path(directory) / "input.csv"
        path.write_text(content, encoding="utf-8")
        return path

    def test_summary_is_deterministic_and_counts_missing_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, "name,city,score\nAda,London,10\nBob,,\n")

            summary = summarize_csv(path)

            self.assertEqual(
                {
                    "columns": ["name", "city", "score"],
                    "missing": {"name": 0, "city": 1, "score": 1},
                    "row_count": 2,
                },
                summary,
            )
            stdout = io.StringIO()
            self.assertEqual(0, run([str(path)], stdout=stdout, stderr=io.StringIO()))
            self.assertEqual(summary, json.loads(stdout.getvalue()))
            expected = json.dumps(summary, sort_keys=True, separators=(",", ":")) + "\n"
            self.assertEqual(expected, stdout.getvalue())

    def test_empty_input_fails_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, "")
            stdout = io.StringIO()
            stderr = io.StringIO()

            self.assertEqual(2, run([str(path)], stdout=stdout, stderr=stderr))

            self.assertEqual("", stdout.getvalue())
            self.assertEqual("csv-summary: CSV header is required\n", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())

    def test_duplicate_header_and_extra_fields_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            duplicate = self.write_csv(directory, "name,name\nAda,Lovelace\n")
            with self.assertRaisesRegex(ValueError, "unique"):
                summarize_csv(duplicate)

            extra = self.write_csv(directory, "name\nAda,extra\n")
            with self.assertRaisesRegex(ValueError, "more fields"):
                summarize_csv(extra)

    def test_missing_path_fails_without_traceback(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()

        self.assertEqual(2, run(["missing.csv"], stdout=stdout, stderr=stderr))

        self.assertEqual("", stdout.getvalue())
        self.assertIn("input is not a regular file", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
