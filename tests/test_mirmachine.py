import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


SCRIPT = Path(__file__).parents[1] / "scripts" / "MirMachine.py"
SPEC = importlib.util.spec_from_file_location("MirMachine", SCRIPT)
MIRMACHINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MIRMACHINE)


class MirMachineTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        directory = Path(self.tempdir.name)
        self.tree = directory / "tree.newick"
        self.families = directory / "families.tsv"
        self.losses = directory / "losses.tsv"
        self.yaml_path = directory / "run.yaml"

        self.tree.write_text("(((A,B)Grandchild)Child,C)Parent;", encoding="utf-8")
        self.families.write_text(
            "Parent\tMIR-P\nChild\tMIR-C\nGrandchild\tMIR-G\n",
            encoding="utf-8",
        )
        self.losses.write_text("Parent\tMIR-LOST\n", encoding="utf-8")

    def tearDown(self):
        self.tempdir.cleanup()

    def test_node_scope(self):
        with patch.object(MIRMACHINE, "tree_file", str(self.tree)):
            default_nodes = MIRMACHINE._resolve_nodes_for_query("Child")
            expanded_nodes = MIRMACHINE._resolve_nodes_for_query(
                "Child", include_descendants=True
            )

        self.assertEqual(set(default_nodes), {"Child", "Parent"})
        self.assertEqual(set(expanded_nodes), {"Child", "Grandchild", "Parent"})
        self.assertEqual(
            MIRMACHINE._collect_families_from_tsv(self.families, default_nodes),
            ["MIR-C", "MIR-P"],
        )

    def test_add_all_nodes_does_not_expand_scoring(self):
        arguments = {
            "--species": "example",
            "--genome": "genome.fa",
            "--node": "Parent",
            "--family": None,
            "--single-node-only": False,
            "--add-all-nodes": True,
        }

        with patch.object(MIRMACHINE, "arguments", arguments, create=True):
            with patch.multiple(
                MIRMACHINE,
                tree_file=str(self.tree),
                nodes_mirnas_file=str(self.families),
                losses_mirnas_file=str(self.losses),
            ):
                with patch.object(
                    MIRMACHINE, "_yaml_output_path", return_value=self.yaml_path
                ):
                    MIRMACHINE.create_yaml_file()

        payload = yaml.safe_load(self.yaml_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["mirnas"], ["MIR-C", "MIR-G", "MIR-P"])
        self.assertEqual(payload["score_mirnas"], ["MIR-P"])
        self.assertEqual(payload["losses"], ["MIR-LOST"])


if __name__ == "__main__":
    unittest.main()
