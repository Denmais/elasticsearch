import asyncio

from config import ELASTICSEARCH_INDEX
from search.client import create_elasticsearch_client
from search.index import ensure_index


async def main() -> None:
    client = create_elasticsearch_client()

    try:
        if not await client.ping():
            raise RuntimeError("Elasticsearch недоступен")

        created = await ensure_index(client)

        if created:
            print(f"Индекс создан: {ELASTICSEARCH_INDEX}")
        else:
            print(f"Индекс уже создан: {ELASTICSEARCH_INDEX}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())