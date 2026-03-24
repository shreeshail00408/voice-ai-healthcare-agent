```mermaid
flowchart TD
  subgraph Client
    A[User Microphone] -->|Audio Stream| B[Frontend (Next.js) WebSocket/WebRTC]
    B -->|ws audio| C[Voice Gateway]
  end

  subgraph VoiceGateway[Voice Gateway Service]
    C --> D[STT (streaming)]
    D --> E[Language Detection]
    E --> F[Conversation Agent]
    F --> G[Tool Calls (Scheduler, DB)]
    G --> H[TTS (streaming)]
    H --> C
  end

  subgraph BackendServices[Services]
    F --> I[Redis (session memory)]
    G --> J[Postgres (patient data)]
    K[Celery] --> L[Outbound Campaigns]
    K --> G
  end

  C -. Metrics .-> M[Latency & Trace Logs]
  F -. Reasoning Traces .-> M

  style VoiceGateway fill:#f9f,stroke:#333,stroke-width:2px
  style BackendServices fill:#efe,stroke:#333,stroke-width:2px
```

## Notes
- The Voice Gateway is implemented as a FastAPI WebSocket service that streams audio to STT, performs language detection, calls the agent, and streams TTS back.
- Redis holds ephemeral session memory; PostgreSQL stores long-term patient records and appointments.
- Celery handles outbound campaigns and scheduled tasks.
