#!/usr/bin/env python
"""
Resolve the nearest available MirMachine node for a species using a local NCBI
Taxonomy dump.

Examples
--------
Download/cache taxonomy once and resolve a species:
    python mirmachine_autonode.py --species "Caenorhabditis elegans"

Print a ready-to-run MirMachine command:
    python mirmachine_autonode.py --species Scyliorhinus_torazame \
        --genome genome.fa --print-command

Use an already-known NCBI taxid:
    python mirmachine_autonode.py --taxid 6239
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tarfile
import unicodedata
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

TAXDUMP_URL = "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz"


def normalize_name(name: str) -> str:
    """Normalize names for matching NCBI names to MirMachine node labels."""
    name = name.replace("_", " ").strip()
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"\s+", " ", name)
    return name.casefold()


def dmp_fields(line: str) -> List[str]:
    """Parse an NCBI .dmp line."""
    return [field.strip() for field in line.rstrip("\n").split("|")][:-1]


def default_mirmachine_tree() -> Optional[Path]:
    """Return the installed MirMachine tree.newick path when available."""
    try:
        from mirmachine import meta  # type: ignore
    except Exception:
        return None
    return Path(os.path.dirname(meta.__file__)) / "tree.newick"


def download_taxdump(taxdir: Path, force: bool = False) -> None:
    """Download and extract names.dmp and nodes.dmp if they are missing."""
    taxdir.mkdir(parents=True, exist_ok=True)
    names_path = taxdir / "names.dmp"
    nodes_path = taxdir / "nodes.dmp"
    if names_path.exists() and nodes_path.exists() and not force:
        return

    archive_path = taxdir / "taxdump.tar.gz"
    if force or not archive_path.exists():
        print(f"Downloading {TAXDUMP_URL} -> {archive_path}", file=sys.stderr)
        urllib.request.urlretrieve(TAXDUMP_URL, archive_path)

    wanted = {"names.dmp", "nodes.dmp", "merged.dmp"}
    with tarfile.open(archive_path, "r:gz") as tar:
        for member in tar.getmembers():
            basename = Path(member.name).name
            if basename in wanted:
                member.name = basename
                tar.extract(member, taxdir)

    if not names_path.exists() or not nodes_path.exists():
        raise FileNotFoundError(
            f"Could not extract names.dmp and nodes.dmp from {archive_path}"
        )


def load_ncbi_taxonomy(
    taxdir: Path,
) -> Tuple[
    Dict[int, int],
    Dict[int, str],
    Dict[int, str],
    Dict[str, List[Tuple[int, str]]],
    Dict[int, int],
]:
    """
    Load parent/rank/name indexes from NCBI taxdump.

    Returns
    -------
    parent_by_taxid, rank_by_taxid, scientific_name_by_taxid,
    name_index, merged_taxid_map
    """
    parent_by_taxid: Dict[int, int] = {}
    rank_by_taxid: Dict[int, str] = {}
    scientific_name_by_taxid: Dict[int, str] = {}
    name_index: Dict[str, List[Tuple[int, str]]] = defaultdict(list)
    merged_taxid_map: Dict[int, int] = {}

    nodes_path = taxdir / "nodes.dmp"
    names_path = taxdir / "names.dmp"
    merged_path = taxdir / "merged.dmp"

    with nodes_path.open(encoding="utf-8") as handle:
        for line in handle:
            fields = dmp_fields(line)
            if len(fields) < 3:
                continue
            taxid = int(fields[0])
            parent = int(fields[1])
            rank = fields[2]
            parent_by_taxid[taxid] = parent
            rank_by_taxid[taxid] = rank

    with names_path.open(encoding="utf-8") as handle:
        for line in handle:
            fields = dmp_fields(line)
            if len(fields) < 4:
                continue
            taxid = int(fields[0])
            name_txt = fields[1]
            name_class = fields[3]
            norm = normalize_name(name_txt)
            name_index[norm].append((taxid, name_class))
            if name_class == "scientific name":
                scientific_name_by_taxid[taxid] = name_txt

    if merged_path.exists():
        with merged_path.open(encoding="utf-8") as handle:
            for line in handle:
                fields = dmp_fields(line)
                if len(fields) >= 2:
                    merged_taxid_map[int(fields[0])] = int(fields[1])

    return (
        parent_by_taxid,
        rank_by_taxid,
        scientific_name_by_taxid,
        name_index,
        merged_taxid_map,
    )


def resolve_name_to_taxid(
    species_name: str,
    name_index: Dict[str, List[Tuple[int, str]]],
) -> int:
    """Resolve a species/run name to one NCBI taxid."""
    norm = normalize_name(species_name)
    candidates = name_index.get(norm, [])
    if not candidates:
        raise ValueError(f"Species name not found in local NCBI taxonomy: {species_name!r}")

    scientific = [taxid for taxid, name_class in candidates if name_class == "scientific name"]
    if len(scientific) == 1:
        return scientific[0]
    if len(candidates) == 1:
        return candidates[0][0]

    # If duplicated by multiple non-scientific names, prefer the lowest taxid only when
    # all candidates point to exactly the same taxid. Otherwise the user should pass --taxid.
    unique_taxids = sorted({taxid for taxid, _ in candidates})
    if len(unique_taxids) == 1:
        return unique_taxids[0]

    preview = ", ".join(f"{taxid} ({klass})" for taxid, klass in candidates[:15])
    raise ValueError(
        f"Ambiguous NCBI name {species_name!r}. Use --taxid. Candidates: {preview}"
    )


def lineage_from_taxid(
    taxid: int,
    parent_by_taxid: Dict[int, int],
    rank_by_taxid: Dict[int, str],
    name_by_taxid: Dict[int, str],
    merged_taxid_map: Dict[int, int],
) -> List[dict]:
    """Return lineage from queried taxon to root."""
    taxid = merged_taxid_map.get(taxid, taxid)
    if taxid not in parent_by_taxid:
        raise ValueError(f"Taxid not found in local NCBI taxonomy: {taxid}")

    lineage: List[dict] = []
    seen = set()
    current = taxid
    while current not in seen:
        seen.add(current)
        lineage.append(
            {
                "taxid": current,
                "name": name_by_taxid.get(current, str(current)),
                "rank": rank_by_taxid.get(current, "no rank"),
            }
        )
        parent = parent_by_taxid.get(current)
        if parent is None or parent == current:
            break
        current = parent
    return lineage


def available_mirmachine_nodes(tree_path: Path) -> Dict[str, str]:
    """
    Read available MirMachine node labels from the bundled newick tree.

    This mirrors MirMachine.py behavior: internal node names are split on '_',
    'group' is ignored, leaves are ignored, and labels must look like taxon names.
    The installed MirMachine environment already depends on ``newick``; a small
    regex fallback is kept here so the resolver can still list internal labels
    in minimal environments.
    """
    labels = []

    try:
        import newick  # type: ignore
    except Exception:
        # Fallback: internal Newick labels occur immediately after a closing
        # parenthesis and before a delimiter/branch length. This is sufficient
        # for MirMachine's meta/tree.newick naming style.
        text = tree_path.read_text(encoding="utf-8")
        internal_names = re.findall(r"\)([^,():;]+)", text)
        for name in internal_names:
            for part in name.split("_"):
                part = part.strip()
                if len(part) <= 2 or part == "group":
                    continue
                if re.match(r"[A-Z][a-z]+", part):
                    labels.append(part)
    else:
        tree = newick.read(str(tree_path))
        for node in tree[0].walk():
            if node.name is None or node.is_leaf:
                continue
            for part in node.name.split("_"):
                part = part.strip()
                if len(part) <= 2 or part == "group":
                    continue
                if re.match(r"[A-Z][a-z]+", part):
                    labels.append(part)

    # normalized label -> canonical MirMachine spelling
    return {normalize_name(label): label for label in sorted(set(labels))}


def find_nearest_mirmachine_node(
    lineage: Iterable[dict],
    available_nodes: Dict[str, str],
) -> Tuple[str, dict]:
    """Return the first NCBI lineage name that is available as a MirMachine node."""
    for taxon in lineage:
        norm = normalize_name(taxon["name"])
        if norm in available_nodes:
            return available_nodes[norm], taxon
    raise ValueError("No NCBI lineage name matched any available MirMachine node.")


def format_mirmachine_command(args: argparse.Namespace, node: str, species_name: str) -> str:
    run_name = args.run_name or species_name.replace(" ", "_")
    parts = ["MirMachine.py", "--node", node, "--species", run_name]
    if args.genome:
        parts.extend(["--genome", args.genome])
    if args.model:
        parts.extend(["--model", args.model])
    if args.cpu:
        parts.extend(["--cpu", str(args.cpu)])
    if args.long:
        parts.append("--long")
    return " ".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve nearest MirMachine node from a species name or NCBI taxid."
    )
    query = parser.add_mutually_exclusive_group(required=True)
    query.add_argument("--species", help="Species/run name, e.g. 'Caenorhabditis elegans'.")
    query.add_argument("--taxid", type=int, help="NCBI Taxonomy identifier.")

    parser.add_argument(
        "--taxdir",
        default=str(Path.home() / ".cache" / "mirmachine" / "ncbi_taxonomy"),
        help="Directory containing or receiving names.dmp and nodes.dmp.",
    )
    parser.add_argument("--tree", help="Path to MirMachine meta/tree.newick.")
    parser.add_argument("--force-download", action="store_true", help="Redownload taxdump.")
    parser.add_argument("--no-download", action="store_true", help="Do not download missing taxdump files.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--lineage", action="store_true", help="Print full lineage.")

    # Optional command printer fields.
    parser.add_argument("--print-command", action="store_true", help="Print a MirMachine.py command.")
    parser.add_argument("--genome", help="Genome FASTA path for --print-command.")
    parser.add_argument("--run-name", help="Run/species name to use in MirMachine command.")
    parser.add_argument("--model", choices=["combined", "deutero", "proto"], help="Model for command output.")
    parser.add_argument("--cpu", type=int, help="CPU count for command output.")
    parser.add_argument("--long", action="store_true", help="Add --long to command output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    taxdir = Path(args.taxdir)

    if not args.no_download:
        download_taxdump(taxdir, force=args.force_download)
    elif not (taxdir / "names.dmp").exists() or not (taxdir / "nodes.dmp").exists():
        raise FileNotFoundError(
            f"Missing names.dmp/nodes.dmp in {taxdir}; rerun without --no-download."
        )

    tree_path = Path(args.tree) if args.tree else default_mirmachine_tree()
    if tree_path is None or not tree_path.exists():
        raise FileNotFoundError(
            "Could not find MirMachine meta/tree.newick. Install MirMachine or pass --tree."
        )

    (
        parent_by_taxid,
        rank_by_taxid,
        scientific_name_by_taxid,
        name_index,
        merged_taxid_map,
    ) = load_ncbi_taxonomy(taxdir)

    if args.taxid is not None:
        taxid = merged_taxid_map.get(args.taxid, args.taxid)
        query_name = scientific_name_by_taxid.get(taxid, str(taxid))
    else:
        query_name = args.species.replace("_", " ")
        taxid = resolve_name_to_taxid(query_name, name_index)

    lineage = lineage_from_taxid(
        taxid,
        parent_by_taxid,
        rank_by_taxid,
        scientific_name_by_taxid,
        merged_taxid_map,
    )
    nodes = available_mirmachine_nodes(tree_path)
    nearest_node, matched_taxon = find_nearest_mirmachine_node(lineage, nodes)

    result = {
        "query": args.species or args.taxid,
        "taxid": taxid,
        "scientific_name": scientific_name_by_taxid.get(taxid, query_name),
        "mirmachine_node": nearest_node,
        "matched_ncbi_taxon": matched_taxon,
        "tree": str(tree_path),
    }
    if args.lineage or args.json:
        result["lineage"] = lineage
    if args.print_command:
        result["command"] = format_mirmachine_command(
            args,
            nearest_node,
            result["scientific_name"],
        )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"species: {result['scientific_name']}")
        print(f"taxid: {taxid}")
        print(f"mirmachine_node: {nearest_node}")
        print(
            "matched_ncbi_taxon: "
            f"{matched_taxon['name']} [{matched_taxon['rank']}, taxid {matched_taxon['taxid']}]"
        )
        if args.lineage:
            print("lineage_nearest_to_root:")
            for taxon in lineage:
                print(f"  {taxon['name']}\t{taxon['rank']}\t{taxon['taxid']}")
        if args.print_command:
            print(f"command: {result['command']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
