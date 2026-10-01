import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "mirmachine_autonode.py"
SPEC = importlib.util.spec_from_file_location("mirmachine_autonode", SCRIPT)
AUTONODE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUTONODE)


def nodes(*names):
    return {AUTONODE.normalize_name(name): name for name in names}


class FindNearestMirMachineNodeTests(unittest.TestCase):
    def test_ncbi_lineage_bridges_to_nearest_mirmachine_node(self):
        cases = [
            (["Acanthomorphata", "Clupeocephala"], "Acanthomorpha"),
            (["Artiodactyla", "Laurasiatheria", "Boreoeutheria"], "Scrotifera"),
            (["Carnivora", "Laurasiatheria", "Boreoeutheria"], "Scrotifera"),
            (["Actinopterygii", "Gnathostomata"], "Osteichthyes"),
            (["Dasyuromorphia", "Metatheria", "Theria"], "Australidelphia"),
            (["Didelphimorphia", "Metatheria", "Theria"], "Marsupialia"),
            (["Tunicata", "Chordata"], "Olfactores"),
            (["Eulipotyphla", "Laurasiatheria", "Boreoeutheria"], "Boreoeutheria"),
        ]
        available = nodes(
            "Acanthomorpha",
            "Australidelphia",
            "Boreoeutheria",
            "Chordata",
            "Clupeocephala",
            "Gnathostomata",
            "Marsupialia",
            "Olfactores",
            "Osteichthyes",
            "Scrotifera",
            "Theria",
        )

        for lineage_names, expected in cases:
            with self.subTest(lineage=lineage_names):
                lineage = [{"name": name} for name in lineage_names]
                node, _ = AUTONODE.find_nearest_mirmachine_node(lineage, available)
                self.assertEqual(node, expected)

    def test_missing_bridge_target_falls_back_to_exact_ancestor(self):
        lineage = [{"name": "Acanthomorphata"}, {"name": "Clupeocephala"}]

        node, matched_taxon = AUTONODE.find_nearest_mirmachine_node(
            lineage, nodes("Clupeocephala")
        )

        self.assertEqual(node, "Clupeocephala")
        self.assertEqual(matched_taxon["name"], "Clupeocephala")


if __name__ == "__main__":
    unittest.main()
