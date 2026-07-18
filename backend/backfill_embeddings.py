"""Resumable backfill for documents that do not yet have embeddings."""

import argparse

from app.db.session import SessionLocal, initialize_database
from app.services.embedding import EmbeddingService


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()

    initialize_database()
    session = SessionLocal()
    try:
        result = EmbeddingService(session).backfill_missing_embeddings(
            batch_size=args.batch_size
        )
        print(f"Embeddings generated: {result.embedded}")
        print("Embedding backfill completed successfully.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
