#!/usr/bin/env bash
# Fetch the canonical production diagrams from docs.sui.io.
#
# These complement the annotated HTML recreations in the parent folder.
# Either format is a valid training signal for Claude Design. The
# recreations carry compliance annotations, and the originals carry
# pixel-perfect fidelity.
#
# Usage:
#   ./fetch-originals.sh
#
# If a 404 comes back, the docusaurus build hash has rotated. Re-fetch
# the URL from docs.sui.io directly (right-click → Copy image address)
# and update the variable below.

set -euo pipefail

cd "$(dirname "$0")"

# C4 Level 2 Architecture: data-serving stack
curl -fsSL \
  "https://docs.sui.io/assets/images/access-interfaces_accessing-data_v1-ac73a55a4128a0ab18137b0e097cbb95.svg" \
  -o access-interfaces_accessing-data_v1.svg
echo "✓ Fetched architecture_data-serving (as access-interfaces_accessing-data_v1.svg)"

# C4 Level 4 Sequence: transaction lifecycle
curl -fsSL \
  "https://docs.sui.io/assets/images/transaction-lifecycle_transactions_v1-dd22c5ca774fb65a8e83ce73fc95ef5c.png" \
  -o transaction-lifecycle_transactions_v1.png
echo "✓ Fetched sequence_txn-lifecycle (as transaction-lifecycle_transactions_v1.png)"

echo ""
echo "Done. Originals saved alongside this script."
echo "Source license: CC BY 4.0 (https://github.com/MystenLabs/sui/blob/main/docs/site/LICENSE)"
