"""Resumable local-embedding backfill for documents without embeddings."""

import argparse
import sys
from uuid import UUID

from app.db.session import SessionLocal, initialize_database
from app.services.embedding import EmbeddingService


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill embeddings for documents without embeddings. "
                    embeddings. "
                    "WARNING: Without --workspace-id, this will process ALL workspaces, "
                    "which may be unintended in a multi-tenant system. "
                    "It is recommended to specify --workspace-id for safety."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Number of documents to process per batch",
    )
    parser.add_argument(
        "--workspace-id",
        type=str,
        help="UUID of the workspace to process. If omitted, all workspaces will be processed (use with caution).",
    )
    args = parser.parse_args()

    workspace_id: Optional[UUID] = None
    if args.workspace_id:
        try:
            workspace_id = UUID(args.workspace_id)
        except ValueError:
            print(f"Error: Invalid workspace ID '{args.workspace_id}'. Must be a valid UUID.")
            sys.exit(1)

    initialize_database()
    session = SessionLocal()
    try:
        embedding_service = EmbeddingService(session, workspace_id=workspace_id)
        result = embedding_service.backfill_missing_embeddings(
            batch_size=args.batch_size
        )
        print(f"Embeddings generated: {result.embedded}")
        print("Embedding backfill completed successfully.")
    finally:
        session.close()


if __name__ == "__main__":
    main()