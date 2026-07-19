# External Milvus for full retrieval

Windows cannot use `milvus-lite` for the local file-backed mode. The MVP still runs through FAQ, error, course-note, and code retrieval, but document ingestion and full vector retrieval need an external Milvus service.

Run Milvus:

```powershell
docker compose -f docker-compose.milvus.yml up -d
```

Configure the app:

```powershell
STUCKTOSHIP_MILVUS_URI=http://127.0.0.1:19530
```

Then restart the API and upload documents through the existing document endpoint or CLI.

Run the API and Milvus together with the production template:

```powershell
$env:STUCKTOSHIP_API_KEYS="replace-with-a-long-random-key"
docker compose -f docker-compose.production.yml up -d --build
```

Every `/api/` request then needs one of:

```text
Authorization: Bearer replace-with-a-long-random-key
X-API-Key: replace-with-a-long-random-key
```

Stop Milvus:

```powershell
docker compose -f docker-compose.milvus.yml down
```
